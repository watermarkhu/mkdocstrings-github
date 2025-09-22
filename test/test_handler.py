"""Tests for the `handler` module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from mkdocstrings import CollectionError

from mkdocstrings_handlers.github import GitHubHandler, GitHubOptions

if TYPE_CHECKING:
    pass


def test_collect_missing_identifier(handler: GitHubHandler) -> None:
    """Assert error is raised for missing identifiers."""
    with pytest.raises(CollectionError):
        handler.collect("nonexistent_github_function", GitHubOptions())
