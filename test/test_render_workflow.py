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
from test.helpers import render


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "", True),
        (True, "Custom heading", True),
        (False, "", False),
    ],
)
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_general(
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
    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "", 1, False, ""),
        (True, "Custom heading", 2, False, "Custom toc label"),
        (False, "", 3, True, ""),
    ],
)
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_headings(
    session_handler: GitHubHandler,
    identifier: str,
    inputs: tuple[bool, str, int, bool, str],
) -> None:
    final_options = {
        "show_heading": inputs[0],
        "heading": inputs[1],
        "heading_level": inputs[2],
        "show_toc_entry": inputs[3],
        "toc_label": inputs[4],
    }
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]


@pytest.mark.parametrize(
    "inputs",
    [
        (True, "major", "", True, True),
        (True, "semver", "", True, False),
        (True, "string", "latest", False, True),
        (False, "string", "", False, False),
    ],
)
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_signature(
    session_handler: GitHubHandler,
    identifier: str,
    inputs: tuple[bool, SIGNATURE_VERSION, str, bool, bool],
) -> None:
    final_options = {
        "show_signature": inputs[0],
        "signature_version": inputs[1],
        "signature_version_string": inputs[2],
        "signature_show_secrets": inputs[3],
        "signature_show_permissions": inputs[4],
    }
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]


@pytest.mark.parametrize(
    "show",
    [
        (True, False, True, True),
        (True, True, False, False),
        (False, False, False, False),
    ],
)
@pytest.mark.parametrize("parameters_order", PARAMETERS_ORDER.__args__)
@pytest.mark.parametrize("parameters_section_style", PARAMETERS_SECTION_STYLE.__args__)
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_parameters(
    session_handler: GitHubHandler,
    identifier: str,
    parameters_order: PARAMETERS_ORDER,
    parameters_section_style: PARAMETERS_SECTION_STYLE,
    show: tuple[bool, bool, bool, bool],
) -> None:
    final_options = {
        "show_inputs": show[0],
        "show_inputs_only_required": show[1],
        "show_outputs": show[2],
        "show_secrets": show[3],
        "parameters_order": parameters_order,
        "parameters_section_style": parameters_section_style,
    }
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]
