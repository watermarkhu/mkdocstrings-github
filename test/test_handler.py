"""Tests for the `handler` module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from mkdocstrings import CollectionError

from mkdocstrings_handlers.github import GitHubHandler

if TYPE_CHECKING:
    pass


@pytest.mark.parametrize(
    ("identifier", "name"),
    [
        (".github/workflows/reusable-workflow.yml", "Reusable Workflow with workflow_call"),
        (".github/workflows/hybrid-workflow.yml", "Hybrid Workflow - Call and Dispatch"),
    ],
)
def test_collect_workflow(handler: GitHubHandler, identifier: str, name: str) -> None:
    """Assert workflows can be collected by their filename."""
    item = handler.collect(identifier, {})
    assert item is not None, f"Workflow '{identifier}' should be collected."
    assert item.name == name, f"Collected workflow '{identifier}' should have the correct name."


@pytest.mark.parametrize(
    ("identifier", "name"),
    [
        (".", "Root Level Action"),
        ("actions/minimal-action", "Minimal Action"),
        ("actions/complex-action", "Complex Action with Advanced Features"),
        ("actions/simple-action", "Simple Action"),
        ("actions/javascript-action", "JavaScript Action"),
        ("actions/docker-action", "Docker-based Action"),
        ("nested/actions/deep-action", "Deep Nested Action"),
    ],
)
def test_collect_action(handler: GitHubHandler, identifier: str, name: str) -> None:
    """Assert actions can be collected by their filename."""
    item = handler.collect(identifier, {})
    assert item is not None, f"Action '{identifier}' should be collected."
    assert item.name == name, f"Collected action '{identifier}' should have the correct name."


def test_collect_missing_identifier(handler: GitHubHandler) -> None:
    """Assert error is raised for missing identifiers."""
    with pytest.raises(
        CollectionError, match="Identifier 'missing.yml' is not a valid workflow file."
    ):
        handler.collect("missing.yml", {})

    with pytest.raises(
        CollectionError,
        match="Identifier 'README.md' is not a valid workflow file or action directory.",
    ):
        handler.collect("README.md", {})

    with pytest.raises(
        CollectionError,
        match="Identifier 'actions' is not a valid workflow file or action directory.",
    ):
        handler.collect("actions", {})


@pytest.mark.without_repo
@pytest.mark.github_actions
def test_collect_repo_github_actions(handler: GitHubHandler) -> None:
    """Assert error is raised when no repo is configured."""
    assert handler.get_repository_name() == "watermarkhu/mkdocstrings-github", (
        "Could not get repository from env"
    )


@pytest.mark.without_repo
def test_collect_repo_git(handler: GitHubHandler) -> None:
    """Assert error is raised when no repo is configured."""
    assert handler.get_repository_name() == "watermarkhu/mkdocstrings-github-fixture"
