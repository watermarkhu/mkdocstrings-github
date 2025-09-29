"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

import os
import re
import subprocess
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

from github import Auth, Github
from mkdocstrings_handlers.github import rendering
from mkdocstrings_handlers.github.config import GitHubConfig, GitHubOptions
from mkdocstrings_handlers.github.objects import Action, Workflow

if TYPE_CHECKING:
    from collections.abc import MutableMapping

    from mkdocs.config.defaults import MkDocsConfig


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
        self.workflows: dict[Path, Workflow] = {}
        self.actions: dict[Path, Action] = {}
        self.major: str = ""
        self.semver: str = ""

        # Only run GitHub releases code if not running under pytest
        if (
            rendering.ENV_MAJOR_TAG not in os.environ or rendering.ENV_SEMVER_TAG not in os.environ
        ) and "pytest" not in sys.modules:
            # Use PyGitHub to find last GitHub releases with tags matching vX.X.X and vX

            gh_host = os.environ.get("GH_HOST", config.hostname)
            # Construct base_url for GitHub API.
            #
            # Expected formats for GH_HOST/config.hostname:
            #   - Full API URL (e.g., 'https://github.company.com/api/v3') [RECOMMENDED for GitHub Enterprise]
            #   - Hostname (e.g., 'github.com' or 'github.company.com')
            #   - API subdomain (e.g., 'api.github.com')
            #
            # If a full URL is provided, it is used as-is.
            # If the value contains '/api/', it is assumed to be a full API endpoint and used as-is (with protocol if missing).
            # Otherwise, the code falls back to public GitHub conventions.
            if gh_host.startswith(("http://", "https://")):
                base_url = gh_host
            elif "/api/" in gh_host:
                # If protocol is missing, default to https
                base_url = f"https://{gh_host}"
            elif gh_host.startswith("api."):
                base_url = f"https://{gh_host}"
            else:
                # Warn user about possible misconfiguration for GitHub Enterprise
                _logger.warning(
                    "The GH_HOST/config.hostname value '%s' does not appear to be a full API endpoint. "
                    "For GitHub Enterprise, you may need to specify the full API URL (e.g., 'https://github.company.com/api/v3').",
                    gh_host,
                )
                base_url = f"https://api.{gh_host}"

            if (token_key := "GH_TOKEN") in os.environ:
                gh = Github(base_url=base_url, auth=Auth.Token(os.environ[token_key]))
            elif (token_key := "GITHUB_TOKEN") in os.environ:
                gh = Github(base_url=base_url, auth=Auth.Token(os.environ[token_key]))
            else:
                try:
                    gh = Github(base_url=base_url, auth=Auth.NetrcAuth())
                except RuntimeError:
                    try:
                        token = subprocess.check_output(
                            ["gh", "auth", "token"], text=True, env=os.environ
                        ).strip()
                        if token:
                            gh = Github(base_url=base_url, auth=Auth.Token(token))
                        else:
                            raise RuntimeError("No token from gh auth token")
                    except Exception:
                        _logger.warning(
                            "Could not authenticate with GitHub to get releases. "
                            "Consider setting .netrc, environment variable GH_TOKEN, "
                            "or using GitHub CLI (`gh auth login`) to get GitHub releases.",
                        )
                        gh = Github(base_url=base_url)

            owner, repo_name = self.config.repo.split("/", 1)
            gh_repo = gh.get_repo(f"{owner}/{repo_name}")
            releases = list(gh_repo.get_releases())
            for release in releases:
                tag = release.tag_name
                if not self.semver and SEMVER_PATTERN.match(tag):
                    self.semver = tag
                if not self.major and MAJOR_PATTERN.match(tag):
                    self.major = tag
                if self.semver and self.major:
                    break

            if not self.semver or not self.major:
                if not self.semver and not self.major:
                    messages = ("'vX.X.X' and 'vX'", "'semver and major'")
                elif not self.semver:
                    messages = ("'vX.X.X'", "'semver'")
                else:  # not self.major
                    messages = ("'vX'", "'major'")
                _logger.warning(
                    "Could not find suitable GitHub releases for repo '%s'. "
                    "Make sure there are releases with tags matching %s, "
                    "if you wish to use option signature_version %s.",
                    self.config.repo,
                    messages[0],
                    messages[1],
                )

        if self.config.repo == ".":
            url = next(repo.remote("origin").urls)
            match = re.search(r"github.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", url)
            if match:
                self.config.repo = f"{match.group('owner')}/{match.group('repo')}"
            else:
                _logger.warning(
                    "Could not determine GitHub repository automatically from git remote URL '%s'. "
                    "Make sure the remote URL is a GitHub URL, "
                    "or set the 'repo' option in the configuration.",
                    url,
                )

        # Glob all workflow YAML files using pathlib
        working_tree_dir = Path(repo.working_tree_dir)
        workflows_dir = working_tree_dir / ".github" / "workflows"
        for workflow_file in list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")):
            id = str(workflow_file.relative_to(working_tree_dir))
            workflow = Workflow.from_file(workflow_file, id)
            if workflow is not None:
                self.workflows[workflow_file] = workflow

        # Glob all action.yaml and action.yml files, skipping .git folder entirely using pathlib
        def find_action_files(base: Path):
            for entry in base.iterdir():
                if entry.is_dir():
                    if entry.name == ".git":
                        continue
                    yield from find_action_files(entry)
                elif entry.is_file() and entry.name in ("action.yaml", "action.yml"):
                    yield entry

        for action_file in find_action_files(working_tree_dir):
            id = str(action_file.relative_to(working_tree_dir).parent)
            action = Action.from_file(action_file, id)
            if action is not None:
                self.actions[action_file] = action

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
        self.env.globals["semver_tag"] = self.semver
        self.env.globals["major_tag"] = self.major
        self.env.globals["git_repo"] = self.repo

    def collect(self, identifier: str, options: GitHubOptions) -> Workflow | Action:
        path = Path(self.repo.working_tree_dir) / identifier
        if path in self.workflows:
            return self.workflows[path]
        elif (action_path := path / "action.yml") in self.actions:
            return self.actions[action_path]
        elif (action_path := path / "action.yaml") in self.actions:
            return self.actions[action_path]
        else:
            raise CollectionError(f"Identifier '{identifier}' not found as a workflow or action.")

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
