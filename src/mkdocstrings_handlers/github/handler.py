"""The mkdocstrings handler for processing MATLAB code documentation."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar
from glob import glob
import os

import git
from mkdocstrings import (
    BaseHandler,
    get_logger,
)

from mkdocstrings_handlers.github.config import GitHubConfig
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
        self.global_options = config.options
        self.workflows: dict[Path, Workflow] = {}
        self.actions: dict[Path, Action] = {}

        working_tree_dir = Path(repo.working_tree_dir)
        workflows_dir = working_tree_dir / ".github" / "workflows"
        for workflow_file in list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")):
            workflow = Workflow.from_file(workflow_file)
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
            action = Action.from_file(action_file)
            if action is not None:
                self.actions[action_file] = action


    def collect(self, identifier, options):
        return None


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
