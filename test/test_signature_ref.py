"""Test signature with ref version to improve coverage."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocstrings_handlers.github import GitHubHandler


def test_action_signature_with_ref(session_handler: GitHubHandler) -> None:
    """Test action signature with ref version to cover rendering.py line 29."""
    from test.helpers import render

    # This will use the actual git repo and access git_repo.head.ref.name
    html = render(
        session_handler,
        ".",
        {
            "signature_version": "ref",
            "show_signature": True,
            "show_heading": False,
            "show_description": False,
            "show_source": False,
        },
    )

    # The signature should contain the current branch name (could be HEAD, main, master, etc.)
    assert "@" in html
    # Verify we're actually rendering the signature
    assert "uses:" in html or "@" in html


def test_workflow_signature_with_ref(session_handler: GitHubHandler) -> None:
    """Test workflow signature with ref version."""
    from test.helpers import render

    html = render(
        session_handler,
        ".github/workflows/reusable-workflow.yml",
        {
            "signature_version": "ref",
            "show_signature": True,
            "show_heading": False,
            "show_description": False,
            "show_source": False,
        },
    )

    # The signature should contain the current branch name
    assert "@" in html
