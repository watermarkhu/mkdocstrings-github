"""Configuration for the pytest test suite."""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest
from inline_snapshot import register_format_alias

from test import helpers

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from markdown.core import Markdown
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocstrings import MkdocstringsPlugin

    from mkdocstrings_handlers.github import GitHubHandler


register_format_alias(".html", ".txt")


# --------------------------------------------
# Function-scoped fixtures.
# --------------------------------------------
@pytest.fixture
def mkdocs_conf(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest fixture.
        tmp_path: Pytest fixture.

    Yields:
        MkDocs config.
    """
    with helpers.mkdocs_conf(request, tmp_path) as mkdocs_conf:
        yield mkdocs_conf


@pytest.fixture
def plugin(mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        mkdocstrings plugin instance.
    """
    return helpers.plugin(mkdocs_conf)


@pytest.fixture
def ext_markdown(mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        A Markdown instance.
    """
    return helpers.ext_markdown(mkdocs_conf)


@pytest.fixture
def handler(
    plugin: MkdocstringsPlugin, ext_markdown: Markdown, request: pytest.FixtureRequest
) -> Iterator[GitHubHandler]:
    """Return a handler instance.

    Parameters:
        plugin: Pytest fixture (see conftest.py).

    Returns:
        A handler instance.
    """
    marker = request.node.get_closest_marker("github_actions")
    if marker is not None:
        os.environ["GITHUB_ACTIONS"] = "true"
        os.environ["GITHUB_REPOSITORY"] = "watermarkhu/mkdocstrings-github"
        try:
            handler = helpers.handler(plugin, ext_markdown)
            yield handler
        finally:
            os.environ.pop("GITHUB_REPOSITORY", None)
            os.environ.pop("GITHUB_ACTIONS", None)
    else:
        github_repo = os.environ.pop("GITHUB_REPOSITORY", None)
        try:
            handler = helpers.handler(plugin, ext_markdown)
            yield handler
        finally:
            if github_repo is not None:
                os.environ["GITHUB_REPOSITORY"] = github_repo


# --------------------------------------------
# Session-scoped fixtures.
# --------------------------------------------
@pytest.fixture(scope="session")
def session_mkdocs_conf(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest fixture.
        tmp_path: Pytest fixture.

    Yields:
        MkDocs config.
    """
    with helpers.mkdocs_conf(request, tmp_path_factory.mktemp("project")) as mkdocs_conf:
        yield mkdocs_conf


@pytest.fixture(scope="session")
def session_plugin(session_mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        mkdocstrings plugin instance.
    """
    return helpers.plugin(session_mkdocs_conf)


@pytest.fixture(scope="session")
def session_ext_markdown(session_mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: Pytest fixture (see conftest.py).

    Returns:
        A Markdown instance.
    """
    return helpers.ext_markdown(session_mkdocs_conf)


@pytest.fixture(scope="session")
def session_handler(
    session_plugin: MkdocstringsPlugin, session_ext_markdown: Markdown
) -> Iterator[GitHubHandler]:
    """Return a handler instance.

    Parameters:
        plugin: Pytest fixture (see conftest.py).

    Returns:
        A handler instance.
    """
    handler = helpers.handler(session_plugin, session_ext_markdown)
    yield handler
