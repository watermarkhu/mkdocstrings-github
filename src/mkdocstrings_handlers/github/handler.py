"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

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

from mkdocstrings_handlers.github import rendering
from mkdocstrings_handlers.github.config import GitHubConfig, GitHubOptions
from mkdocstrings_handlers.github.objects import Action, Workflow

if TYPE_CHECKING:
    from collections.abc import MutableMapping

    from mkdocs.config.defaults import MkDocsConfig


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
            return GitHubOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def update_env(self, config: Any) -> None:
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["format_action_signature"] = rendering.format_action_signature
        self.env.filters["order_parameters"] = rendering.order_parameters
        self.env.filters["filter_parameters"] = rendering.filter_parameters

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
        config=GitHubConfig.from_data(**handler_config),
        repo=repo,
        **kwargs,
    )
