from __future__ import annotations

import pytest
from inline_snapshot import outsource

from mkdocstrings_handlers.github import GitHubHandler
from mkdocstrings_handlers.github.config import (
    PARAMETERS_ORDER,
    PARAMETERS_SECTION_STYLE,
    SIGNATURE_VERSION,
)
from test import snapshots
from test.helpers import key, render


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
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.action_show[key("action", final_options)]


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
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.action_show[key("action", final_options)]


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
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.action_show[key("action", final_options)]


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
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.action_show[key("action", final_options)]
