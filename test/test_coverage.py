"""Tests to improve code coverage for uncovered lines."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
from mkdocs.exceptions import PluginError

from mkdocstrings_handlers.github.objects import (
    Input,
    PermissionLevel,
    Workflow,
    _get_member,
)
from mkdocstrings_handlers.github.rendering import (
    anchor_id,
    as_string,
    filter_parameters,
    format_action_signature,
)

if TYPE_CHECKING:
    from mkdocstrings_handlers.github import GitHubHandler


class TestRendering:
    """Test rendering module functions."""

    def test_as_string_with_bool_false(self):
        """Test as_string with boolean False value."""
        assert as_string(False) == "false"

    def test_as_string_with_bool_true(self):
        """Test as_string with boolean True value."""
        assert as_string(True) == "true"

    def test_as_string_with_int(self):
        """Test as_string with integer value."""
        assert as_string(42) == "42"

    def test_as_string_with_float(self):
        """Test as_string with float value."""
        assert as_string(3.14) == "3.14"

    def test_as_string_with_none(self):
        """Test as_string with None value."""
        assert as_string(None) == ""

    def test_as_string_with_string(self):
        """Test as_string with string value."""
        assert as_string("test") == "test"

    def test_as_string_with_unsupported_type(self):
        """Test as_string raises TypeError for unsupported types."""
        with pytest.raises(TypeError, match="Unsupported type"):
            as_string([1, 2, 3])  # type: ignore

    def test_filter_parameters_optional(self):
        """Test filter_parameters with optional filter."""
        params = [
            Input(name="required", required=True),
            Input(name="optional", required=False),
        ]
        filtered = filter_parameters(params, optional=True)
        assert len(filtered) == 1
        assert filtered[0].name == "optional"

    def test_filter_parameters_description(self):
        """Test filter_parameters with description filter."""
        params = [
            Input(name="with_desc", description="Has description"),
            Input(name="without_desc", description=""),
        ]
        # When description=True, it filters OUT parameters without description
        # So we keep only parameters WITH description
        filtered = filter_parameters(params, description=True)
        assert len(filtered) == 1
        assert filtered[0].name == "with_desc"

    def test_filter_parameters_default(self):
        """Test filter_parameters with default filter."""
        params = [
            Input(name="with_default", default="value"),
            Input(name="without_default", default=None),
        ]
        # When default=True, it filters OUT parameters without default
        # So we keep only parameters WITH default
        filtered = filter_parameters(params, default=True)
        assert len(filtered) == 1
        assert filtered[0].name == "with_default"

    def test_anchor_id(self):
        """Test anchor_id with spaces."""
        result = anchor_id("my name", "input", "parent id")
        assert result == "parent-id--input.my-name"

    def test_format_action_signature_non_repo(self):
        """Test format_action_signature when git_repo is not a Repo instance."""
        from mkdocstrings_handlers.github.config import GitHubOptions

        # Test with ref version when git_repo is not a Repo
        context = Mock()
        context.environment.globals = {"git_repo": "not_a_repo"}

        options = GitHubOptions(signature_version="ref")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == "owner/repo@unknown"

    def test_format_action_signature_exception_handling(self):
        """Test format_action_signature when accessing head.ref.name raises exception."""
        import git

        from mkdocstrings_handlers.github.config import GitHubOptions

        # Create a mock that is a Repo instance but raises exception when accessing head.ref.name
        context = Mock()

        # Create an actual Repo type mock with side effect
        mock_repo = Mock(spec=git.Repo)
        type(mock_repo.head.ref).name = Mock(side_effect=Exception("Test exception"))

        context.environment.globals = {"git_repo": mock_repo}

        options = GitHubOptions(signature_version="ref")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == "owner/repo@unknown"


class TestObjects:
    """Test objects module functions and classes."""

    def test_get_member_raises_key_error(self):
        """Test _get_member raises KeyError when key is missing and no default."""
        with pytest.raises(KeyError, match="Missing key"):
            _get_member({}, "missing_key", error_message="Missing key")

    def test_permission_level_from_label_invalid(self):
        """Test PermissionLevel.from_label raises ValueError for invalid label."""
        with pytest.raises(ValueError, match="No Permission with label"):
            PermissionLevel.from_label("invalid")

    def test_permission_level_gt_not_implemented(self):
        """Test PermissionLevel.__gt__ returns NotImplemented for non-PermissionLevel."""
        result = PermissionLevel.read.__gt__("string")
        assert result == NotImplemented

    def test_workflow_from_file_no_workflow_call(self, tmp_path):
        """Test Workflow.from_file returns None when workflow_call is not present."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  push:
    branches: [main]
"""
        )

        result = Workflow.from_file(workflow_file, "test.yml")
        assert result is None

    def test_workflow_invalid_permission_level_string(self, tmp_path):
        """Test Workflow.from_file raises ValueError for invalid permission string."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  workflow_call:
permissions: invalid-level
"""
        )

        with pytest.raises(ValueError, match="Unknown permission level"):
            Workflow.from_file(workflow_file, "test.yml")

    def test_workflow_invalid_permission_type(self, tmp_path):
        """Test Workflow.from_file raises ValueError for invalid permission type."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  workflow_call:
permissions: 123
"""
        )

        with pytest.raises(ValueError, match="permissions must be a string or a dictionary"):
            Workflow.from_file(workflow_file, "test.yml")

    def test_workflow_invalid_job_permission_type(self, tmp_path):
        """Test Workflow.from_file raises ValueError for invalid job permission type."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  workflow_call:
jobs:
  test:
    runs-on: ubuntu-latest
    permissions: 123
"""
        )

        with pytest.raises(ValueError, match="permissions must be a string or a dictionary"):
            Workflow.from_file(workflow_file, "test.yml")


class TestHandler:
    """Test handler module functions."""

    def test_get_releases_exception_handling(self):
        """Test get_releases handles exception when getting git tags fails."""
        from mkdocstrings_handlers.github.config import GitHubConfig
        from mkdocstrings_handlers.github.handler import GitHubHandler

        # Create a mock repo that raises exception when accessing tags
        mock_repo = Mock()
        mock_repo.tags = Mock(side_effect=Exception("Git error"))

        handler = GitHubHandler(config=GitHubConfig(), repo=mock_repo)

        # Should handle exception gracefully without raising
        handler.get_releases()
        assert handler.semver == ""
        assert handler.major == ""

    def test_get_releases_with_invalid_version_tag(self, tmp_path):
        """Test get_releases handles tags with invalid version format."""
        import git

        from mkdocstrings_handlers.github.config import GitHubConfig
        from mkdocstrings_handlers.github.handler import GitHubHandler

        # Create a temporary git repo with a commit
        repo = git.Repo.init(tmp_path)

        # Create a file and commit it so we have a valid HEAD
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        repo.index.add([str(test_file)])
        repo.index.commit("Initial commit")

        # Create tags with invalid version format (including semver-like tags with invalid versions)
        repo.create_tag("invalid-tag")
        repo.create_tag("another-invalid")
        repo.create_tag("v1.2.3")  # Valid semver
        repo.create_tag("v99.99.99")  # Valid semver

        handler = GitHubHandler(config=GitHubConfig(), repo=repo)
        handler.get_releases()

        # Should use the latest valid semver tag
        assert handler.semver == "v99.99.99"
        assert handler.major == ""

    def test_get_releases_with_tags_triggering_invalid_version(self):
        """Test get_releases handles tags that trigger InvalidVersion exception."""
        from mkdocstrings_handlers.github.config import GitHubConfig
        from mkdocstrings_handlers.github.handler import GitHubHandler

        # Create a mock repo with tags that will trigger InvalidVersion
        mock_tag1 = Mock()
        mock_tag1.name = "vinvalid"  # Matches major pattern but invalid version

        mock_tag2 = Mock()
        mock_tag2.name = "v1"  # Valid major tag

        mock_repo = Mock()
        mock_repo.tags = [mock_tag1, mock_tag2]

        handler = GitHubHandler(config=GitHubConfig(), repo=mock_repo)
        handler.get_releases()

        # Should gracefully handle the invalid version and use the valid one
        assert handler.major == "v1"

    def test_get_options_invalid(self, handler: GitHubHandler):
        """Test get_options raises PluginError for invalid options."""
        with pytest.raises(PluginError, match="Invalid options"):
            handler.get_options({"invalid_option": "value", "heading_level": "not_an_int"})

    def test_get_repository_name_no_remotes(self, tmp_path):
        """Test get_repository_name raises error when no valid remote is found."""
        import git

        from mkdocstrings_handlers.github.config import GitHubConfig
        from mkdocstrings_handlers.github.handler import GitHubHandler

        # Create a temporary git repo without any remotes
        repo = git.Repo.init(tmp_path)

        handler = GitHubHandler(config=GitHubConfig(), repo=repo)

        with pytest.raises(
            PluginError,
            match="Could not determine GitHub repository owner/name from any git remote URL",
        ):
            handler.get_repository_name()


class TestWorkflowPermissions:
    """Test workflow permission handling."""

    def test_workflow_job_permission_string(self, tmp_path):
        """Test Workflow with job-level permission strings."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  workflow_call:
jobs:
  test:
    runs-on: ubuntu-latest
    permissions: read-all
"""
        )

        workflow = Workflow.from_file(workflow_file, "test.yml")
        assert workflow is not None
        assert workflow.permission_read_all

    def test_workflow_job_permission_write_all(self, tmp_path):
        """Test Workflow with write-all permission."""
        workflow_file = tmp_path / "workflow.yml"
        workflow_file.write_text(
            """
name: Test Workflow
on:
  workflow_call:
permissions: write-all
"""
        )

        workflow = Workflow.from_file(workflow_file, "test.yml")
        assert workflow is not None
        assert workflow.permission_write_all
