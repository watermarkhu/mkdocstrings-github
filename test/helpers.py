"""Configuration for the pytest test suite."""

from __future__ import annotations

import json
import re
from collections import ChainMap
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any

import bs4
from markdown.core import Markdown
from mkdocs.config.defaults import MkDocsConfig

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    import pytest
    from mkdocstrings import MkdocstringsPlugin

    from mkdocstrings_handlers.github import GitHubHandler


@contextmanager
def mkdocs_conf(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[MkDocsConfig]:
    """Yield a MkDocs configuration object.

    Parameters:
        request: Pytest request fixture.
        tmp_path: Temporary path.

    Yields:
        MkDocs config.
    """
    while hasattr(request, "_parent_request") and hasattr(
        request._parent_request, "_parent_request"
    ):
        request = request._parent_request  # type: ignore
    mkdocstring_config = {"default_handler": "github"}
    marker = request.node.get_closest_marker("without_handler")
    if marker is None:
        mkdocstring_config["handlers"] = {
            "github": {"repo": "watermarkhu/mkdocstrings-github-fixture"}
        }

    conf = MkDocsConfig()
    conf_dict = {
        "site_name": "foo",
        "site_url": "https://example.org/",
        "site_dir": str(tmp_path),
        "plugins": [{"mkdocstrings": mkdocstring_config}],
        **getattr(request, "param", {}),
    }
    # Re-create it manually as a workaround for https://github.com/mkdocs/mkdocs/issues/2289
    mdx_configs: dict[str, Any] = dict(ChainMap(*conf_dict.get("markdown_extensions", [])))

    conf.load_dict(conf_dict)
    conf.config_file_path = str((Path(__file__).parent / "fixture" / "mkdocs.yml").resolve())
    conf.docs_dir = str((Path(__file__).parent / "docs").resolve())

    errors = conf.validate()
    assert errors == ([], []), f"Configuration errors: {errors}"

    conf["mdx_configs"] = mdx_configs
    conf["markdown_extensions"].insert(0, "toc")  # Guaranteed to be added by MkDocs.

    conf = conf["plugins"]["mkdocstrings"].on_config(conf)
    conf = conf["plugins"]["autorefs"].on_config(conf)
    yield conf
    conf["plugins"]["mkdocstrings"].on_post_build(conf)


def plugin(mkdocs_conf: MkDocsConfig) -> MkdocstringsPlugin:
    """Return a plugin instance.

    Parameters:
        mkdocs_conf: MkDocs configuration.

    Returns:
        mkdocstrings plugin instance.
    """
    return mkdocs_conf["plugins"]["mkdocstrings"]


def ext_markdown(mkdocs_conf: MkDocsConfig) -> Markdown:
    """Return a Markdown instance with MkdocstringsExtension.

    Parameters:
        mkdocs_conf: MkDocs configuration.

    Returns:
        A Markdown instance.
    """
    return Markdown(
        extensions=mkdocs_conf["markdown_extensions"], extension_configs=mkdocs_conf["mdx_configs"]
    )


def handler(plugin: MkdocstringsPlugin, ext_markdown: Markdown) -> GitHubHandler:
    """Return a handler instance.

    Parameters:
        plugin: Plugin instance.

    Returns:
        A handler instance.
    """
    handler: GitHubHandler = plugin.handlers.get_handler(  # ty: ignore[invalid-assignment]
        "github"
    )
    handler.major = "v1"
    handler.semver = "v1.2.3"
    handler._update_env(ext_markdown)
    return handler


def _normalize_html(html: str) -> str:
    soup = bs4.BeautifulSoup(html, features="html.parser")
    html = soup.prettify()
    html = re.sub(r"\b(0x)[a-f0-9]+\b", r"\1...", html)
    html = re.sub(r"^(Build Date UTC ?:).+", r"\1...", html, flags=re.MULTILINE)
    html = re.sub(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", r"...", html)
    html = re.sub(r'(?<=id="cell-id=)\w+(?=")', r"...", html)
    return html


def _render_options(options: dict[str, Any]) -> str:
    return f"<!--\n{json.dumps(options, indent=2, sort_keys=True)}\n-->\n\n"


def render(handler: GitHubHandler, identifier: str, final_options: dict[str, Any]) -> str:
    final_options.pop("handler", None)
    final_options.pop("session_handler", None)
    handler_options = final_options.copy()

    # Some default options to make snapshots easier to review.
    handler_options.setdefault("heading_level", 1)
    handler_options.setdefault("signature_version", "string")
    handler_options.setdefault("signature_version_string", "latest")
    handler_options.setdefault("show_heading", False)
    handler_options.setdefault("show_description", False)
    handler_options.setdefault("show_source", False)
    handler_options.setdefault("show_signature", False)
    handler_options.setdefault("show_inputs", False)
    handler_options.setdefault("show_outputs", False)
    handler_options.setdefault("show_secrets", False)
    handler_options.setdefault("show_permissions", False)

    options = handler.get_options(handler_options)
    data = handler.collect(identifier, options)

    html = handler.render(data, options)

    return _render_options(final_options) + _normalize_html(html)
