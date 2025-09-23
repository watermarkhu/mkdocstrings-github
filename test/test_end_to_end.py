"""End-to-end tests for every combination of MATLAB options."""

from __future__ import annotations

import json
import re
from typing import Any

import bs4
import pytest
from inline_snapshot import outsource, register_format_alias

from mkdocstrings_handlers.github import GitHubHandler
from mkdocstrings_handlers.github.config import (
    PARAMETERS_ORDER,
    PARAMETERS_SECTION_STYLE,
    SIGNATURE_VERSION,
)
from test import snapshots

# Can be declared in conftest.py
register_format_alias(".html", ".txt")


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


def _render(handler: GitHubHandler, identifier: str, final_options: dict[str, Any]) -> str:
    final_options.pop("handler", None)
    final_options.pop("session_handler", None)
    handler_options = final_options.copy()

    # Some default options to make snapshots easier to review.
    handler_options.setdefault("heading_level", 1)
    handler_options.setdefault("signature_version_string", "latest")
    handler_options.setdefault("show_heading", False)
    handler_options.setdefault("show_description", False)
    handler_options.setdefault("show_signature", False)
    handler_options.setdefault("show_inputs", False)
    handler_options.setdefault("show_outputs", False)
    handler_options.setdefault("show_secrets", False)
    handler_options.setdefault("show_permissions", False)

    options = handler.get_options(handler_options)
    data = handler.collect(identifier, options)

    html = handler.render(data, options)

    return _render_options(final_options) + _normalize_html(html)


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "", True),
        (True, "Custom heading", True),
        (False, "", False),
    ],
)
@pytest.mark.parametrize("identifier", ["."])
def test_end_to_end_action_general(
    session_handler: GitHubHandler,
    identifier: str,
    inputs: tuple[bool, str, bool],
) -> None:
    final_options = {
        "show_description": inputs[0],
        "description": inputs[1],
        "show_source": inputs[2],
    }
    html = _render(session_handler, identifier, final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.action_show[snapshot_key]


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "", 1, False, False, "", False),
        (True, "Custom heading", 2, False, False, "Custom toc label", False),
        (True, "", 3, True, False, "", True),
        (False, "", 1, False, True, "", False),
        (False, "", 1, False, False, "", False),
    ],
)
@pytest.mark.parametrize("identifier", ["."])
def test_end_to_end_action_headings(
    session_handler: GitHubHandler,
    identifier: str,
    inputs: tuple[bool, str, int, bool, bool, str, bool],
) -> None:
    final_options = {
        "show_heading": inputs[0],
        "heading": inputs[1],
        "heading_level": inputs[2],
        "show_action_branding": inputs[3],
        "show_toc_entry": inputs[4],
        "toc_label": inputs[5],
        "show_action_branding_toc": inputs[6],
    }
    html = _render(session_handler, identifier, final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.action_show[snapshot_key]


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "major", ""),
        (True, "semver", ""),
        (True, "string", "latest"),
        (False, "string", ""),
    ],
)
@pytest.mark.parametrize("identifier", ["."])
def test_end_to_end_action_signature(
    session_handler: GitHubHandler,
    identifier: str,
    inputs: tuple[bool, SIGNATURE_VERSION, str],
) -> None:
    final_options = {
        "show_signature": inputs[0],
        "signature_version": inputs[1],
        "signature_version_string": inputs[2],
    }
    html = _render(session_handler, identifier, final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.action_show[snapshot_key]


@pytest.mark.parametrize(
    "show",
    [
        (True, False, True),
        (True, True, False),
        (False, False, False),
    ],
)
@pytest.mark.parametrize("parameters_order", PARAMETERS_ORDER.__args__)
@pytest.mark.parametrize("parameters_section_style", PARAMETERS_SECTION_STYLE.__args__)
@pytest.mark.parametrize("identifier", ["."])
def test_end_to_end_action_parameters(
    session_handler: GitHubHandler,
    identifier: str,
    parameters_order: PARAMETERS_ORDER,
    parameters_section_style: PARAMETERS_SECTION_STYLE,
    show: tuple[bool, bool, bool],
) -> None:
    final_options = {
        "show_inputs": show[0],
        "show_inputs_only_required": show[1],
        "show_outputs": show[2],
        "parameters_order": parameters_order,
        "parameters_section_style": parameters_section_style,
    }
    html = _render(session_handler, identifier, final_options)
    snapshot_key = tuple(sorted(final_options.items()))
    assert outsource(html, suffix=".html") == snapshots.action_show[snapshot_key]
