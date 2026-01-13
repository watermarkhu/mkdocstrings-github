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
    "identifier",
    [
        ".github/workflows/reusable-workflow.yml",
        ".github/workflows/read-write-workflow.yml",
        ".github/workflows/write-all-workflow.yml",
    ],
)
def test_end_to_end_workflow_permissions(
    session_handler: GitHubHandler,
    identifier: str,
) -> None:
    final_options = {
        "identifier": identifier,
        "show_signature": True,
        "signature_show_permissions": True,
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


@pytest.mark.parametrize("parameters_groups", [True, False])
@pytest.mark.parametrize("parameters_group_title_row", [True, False])
@pytest.mark.parametrize("parameters_section_style", PARAMETERS_SECTION_STYLE.__args__)
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_parameters_grouping(
    session_handler: GitHubHandler,
    identifier: str,
    parameters_section_style: PARAMETERS_SECTION_STYLE,
    parameters_groups: bool,
    parameters_group_title_row: bool,
) -> None:
    final_options = {
        "show_inputs": True,
        "show_outputs": True,
        "show_secrets": True,
        "parameters_section_style": parameters_section_style,
        "parameters_groups": parameters_groups,
        "parameters_group_title_row": parameters_group_title_row,
    }
    html = render(session_handler, identifier, final_options)
    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]


@pytest.mark.parametrize("workflow_chart", [True, False])
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_flowchart(
    session_handler: GitHubHandler,
    identifier: str,
    workflow_chart: bool,
) -> None:
    final_options = {
        "workflow_chart": workflow_chart,
    }
    html = render(session_handler, identifier, final_options)

    # Check that mermaid flowchart is present when enabled
    if workflow_chart:
        assert '<pre class="mermaid">' in html
        assert "flowchart TB" in html
        assert "subgraph" in html
    else:
        assert '<pre class="mermaid">' not in html

    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]


@pytest.mark.parametrize("workflow_chart_step_direction", ["TB", "LR"])
@pytest.mark.parametrize("identifier", [".github/workflows/reusable-workflow.yml"])
def test_end_to_end_workflow_flowchart_step_direction(
    session_handler: GitHubHandler,
    identifier: str,
    workflow_chart_step_direction: str,
) -> None:
    final_options = {
        "workflow_chart": True,
        "workflow_chart_step_direction": workflow_chart_step_direction,
    }
    html = render(session_handler, identifier, final_options)

    # Check that mermaid flowchart is present and contains the correct direction
    assert '<pre class="mermaid">' in html
    assert f"direction {workflow_chart_step_direction}" in html
    assert "flowchart TB" in html
    assert "subgraph" in html

    assert outsource(html, suffix=".html") == snapshots.workflow_show[tuple(final_options.items())]
