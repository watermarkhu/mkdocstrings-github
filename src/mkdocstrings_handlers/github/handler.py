"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Mapping

import git
from mkdocs.exceptions import PluginError
from mkdocstrings import (
    BaseHandler,
    CollectionError,
    HandlerOptions,
    get_logger,
)
from packaging.version import InvalidVersion, Version

from mkdocstrings_handlers.github import rendering
from mkdocstrings_handlers.github.config import GitHubConfig, GitHubOptions
from mkdocstrings_handlers.github.objects import Action, Workflow

if TYPE_CHECKING:
    from collections.abc import MutableMapping

    from mkdocs.config.defaults import MkDocsConfig


NOT_TESTING = "pytest" not in sys.modules
SEMVER_PATTERN = re.compile(r"^v(\d+\.\d+\.\d+)$")
MAJOR_PATTERN = re.compile(r"^v(\d+)$")


_logger = get_logger(__name__)


class GitHubHandler(BaseHandler):
    """The `GitHubHandler` class is a handler for processing GitHub code documentation."""

    name: ClassVar[str] = "github"
    """The GitHub handler class."""

    domain: ClassVar[str] = "gh"  # to match Sphinx's default domain
    """The cross-documentation domain/language for this handler."""

    enable_inventory: ClassVar[bool] = True
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""

    fallback_theme: ClassVar[str] = "material"
    """The fallback theme."""

    def __init__(
        self,
        config: GitHubConfig,
        repo: git.Repo,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the handler with the given configuration.

        Args:
            config: The handler configuration.
            base_dir: The base directory of the project.
            **kwargs: Arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)
        self.config = config
        self.repo = repo
        self.global_options = config.options.__dict__
        self.major: str = ""
        self.semver: str = ""

        # Determine owner and repo name
        if not self.config.repo:
            self.get_repo()

        if NOT_TESTING and (
            rendering.ENV_MAJOR_TAG not in os.environ or rendering.ENV_SEMVER_TAG not in os.environ
        ):
            self.get_releases()

    def get_repo(self) -> None:
        # Get repo from environment variable or git remotes.
        if (
            NOT_TESTING
            and os.environ.get("GITHUB_ACTIONS") == "true"
            and (repo := os.environ.get("GITHUB_REPOSITORY"))
        ):
            self.config.repo = repo
        else:
            # Try each remote to find a valid GitHub owner/repo
            owner = None
            repo_name = None
            for remote in self.repo.remotes:
                for url in remote.urls:
                    match = re.search(
                        r"(?P<host>[\w\.-]+)[/:](?P<owner>[^/]+)/(?P<repo>[^/.]+?)(?:\.git)?$",
                        url,
                    )
                    if match:
                        owner = match.group("owner")
                        repo_name = match.group("repo")
                        break
                if owner and repo_name:
                    break
            if not (owner and repo_name):
                raise PluginError(
                    f"Could not determine GitHub repository owner/name from config.repo='{self.config.repo}' or any git remote URL."
                )
            self.config.repo = f"{owner}/{repo_name}"

    def get_releases(self) -> None:
        # Get all tags from the local git repository.
        try:
            tags = [tag.name for tag in self.repo.tags]
        except Exception as e:
            _logger.warning(f"Could not get git tags from repository: {e}")
            return

        # Separate semver, major, and other tags
        semver_tags = []
        major_tags = []
        other_tags = []
        for tag in tags:
            if SEMVER_PATTERN.match(tag):
                semver_tags.append(tag)
            elif MAJOR_PATTERN.match(tag):
                major_tags.append(tag)
            else:
                other_tags.append(tag)

        # Sort tags using packaging.version.Version
        def version_key(tag):
            try:
                return Version(tag.lstrip("v"))
            except InvalidVersion:
                return Version("0.0.0")

        semver_tags_sorted = sorted(semver_tags, key=version_key, reverse=True)
        major_tags_sorted = sorted(major_tags, key=version_key, reverse=True)
        other_tags_sorted = sorted(other_tags, reverse=True)

        if semver_tags_sorted:
            self.semver = semver_tags_sorted[0]
            _logger.info(f"Using git tag '{self.semver}' for semver.")
        else:
            _logger.warning("No semver tags found in repository.")

        if major_tags_sorted:
            self.major = major_tags_sorted[0]
            _logger.info(f"Using git tag '{self.major}' for major.")
        else:
            _logger.warning("No major tags found in repository.")

        if other_tags_sorted:
            _logger.debug(f"Other git tags found: {', '.join(other_tags_sorted)}")

    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        """Get combined default, global and local options.

        Arguments:
            local_options: The local options.

        Returns:
            The combined options.
        """

        options = {**self.global_options, **local_options}
        try:
            return GitHubOptions(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def update_env(self, config: Any) -> None:
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["format_action_signature"] = rendering.format_action_signature
        self.env.filters["order_parameters"] = rendering.order_parameters
        self.env.filters["filter_parameters"] = rendering.filter_parameters
        self.env.filters["anchor_id"] = rendering.anchor_id
        self.env.filters["as_string"] = rendering.as_string
        self.env.globals["semver_tag"] = self.semver
        self.env.globals["major_tag"] = self.major
        self.env.globals["git_repo"] = self.repo

    def collect(self, identifier: str, options: GitHubOptions) -> Workflow | Action:
        path = Path(self.repo.working_tree_dir) / identifier

        if path.suffix in (".yml", ".yaml"):
            if not path.is_file():
                raise CollectionError(f"Identifier '{identifier}' is not a valid workflow file.")
            data = Workflow.from_file(path, id=identifier)
        elif not path.is_dir():
            raise CollectionError(
                f"Identifier '{identifier}' is not a valid workflow file or action directory."
            )
        elif (action_path := path / "action.yml").is_file():
            data = Action.from_file(action_path, id=identifier)
        elif (action_path := path / "action.yaml").is_file():
            data = Action.from_file(action_path, id=identifier)
        else:
            raise CollectionError(
                f"Identifier '{identifier}' is not a valid workflow file or action directory."
            )
        return data

    def render(self, data: Workflow | Action, options: GitHubOptions) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The collected data to render.
            options: The handler's configuration options.

        Returns:
            The rendered template as HTML.
        """
        template = self.env.get_template(data.template)
        html = template.render(options=options, data=data, config=self.config)
        return html


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> GitHubHandler:
    """
    Create and return a GitHubHandler object with the specified configuration.

    Parameters:
        handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        GitHubHandler: An instance of GitHubHandler configured with the provided parameters.
    """
    config_file = Path(tool_config.config_file_path)
    repo = git.Repo(path=config_file.parent, search_parent_directories=True)

    return GitHubHandler(
        config=GitHubConfig(**handler_config),
        repo=repo,
        **kwargs,
    )
