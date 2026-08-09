"""Tests for API-based GitHub tag and SHA resolution."""

from __future__ import annotations

from unittest.mock import MagicMock

import git
import pytest

from mkdocstrings_handlers.github import remote
from mkdocstrings_handlers.github.config import GitHubOptions
from mkdocstrings_handlers.github.rendering import format_action_signature


def _github_client_fixture(monkeypatch: pytest.MonkeyPatch, repo: MagicMock) -> MagicMock:
    client = MagicMock()
    client.get_repo.return_value = repo
    monkeypatch.setattr(remote, "_github_client", lambda token, host: client)
    return client


class TestTokenDetection:
    def test_github_token_from_env(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "sekret")
        assert remote.github_token() == "sekret"

    def test_gh_token_alt_env(self, monkeypatch):
        monkeypatch.setenv("GH_TOKEN", "sekret")
        assert remote.github_token() == "sekret"

    def test_github_token_takes_precedence_over_gh(self, monkeypatch):
        monkeypatch.setenv("GH_TOKEN", "alt")
        monkeypatch.setenv("GITHUB_TOKEN", "preferred")
        assert remote.github_token() == "preferred"

    def test_no_token(self):
        assert remote.github_token() is None

    def test_provider_github_actions(self, monkeypatch):
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        assert remote.resolve_provider() == "github"

    def test_provider_with_token(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "tok")
        assert remote.resolve_provider() == "github"

    def test_provider_none(self):
        assert remote.resolve_provider() is None


class TestRepositoryHost:
    def test_host_from_github_remote(self, tmp_path):
        repo = git.Repo.init(tmp_path)
        repo.create_remote("origin", "git@github.com:owner/repo.git")
        assert remote.repository_host(repo) == "github.com"

    def test_host_github_actions_overrides_remote(self, tmp_path, monkeypatch):
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        repo = git.Repo.init(tmp_path)
        repo.create_remote("origin", "git@custom-github.example.com:owner/repo.git")
        assert remote.repository_host(repo) == "github.com"

    def test_host_default_when_no_remotes(self, tmp_path):
        repo = git.Repo.init(tmp_path)
        assert remote.repository_host(repo) == "github.com"


class TestGithubClient:
    def test_github_client_uses_default_base_url(self, monkeypatch):
        fake_github = MagicMock()
        monkeypatch.setattr(remote, "_Github", fake_github)
        remote._github_client("tok", "github.com")
        fake_github.assert_called_once_with("tok")

    def test_github_client_uses_ghes_base_url(self, monkeypatch):
        fake_github = MagicMock()
        monkeypatch.setattr(remote, "_Github", fake_github)
        remote._github_client("tok", "github.example.com")
        fake_github.assert_called_once_with("tok", base_url="https://github.example.com/api/v3")

    def test_github_client_warns_when_package_missing(self, monkeypatch, caplog):
        monkeypatch.setattr(remote, "_Github", None)
        assert remote._github_client("tok", "github.com") is None
        assert "not installed" in caplog.text
        assert "mkdocstrings-github[api]" in caplog.text


class TestResolveSignature:
    def test_lightweight_tag(self, monkeypatch):
        ref = MagicMock()
        ref.object.type = "commit"
        ref.object.sha = "a" * 40
        repo = MagicMock()
        repo.get_git_ref.return_value = ref
        _github_client_fixture(monkeypatch, repo)

        assert remote.resolve_signature("tok", "owner/repo", "github.com", "v1.0.0") == (
            "v1.0.0",
            "a" * 40,
        )
        repo.get_git_ref.assert_called_once_with("tags/v1.0.0")

    def test_annotated_tag_is_peeled(self, monkeypatch):
        ref = MagicMock()
        ref.object.type = "tag"
        ref.object.sha = "tag-object-sha"
        tag = MagicMock()
        tag.object.sha = "b" * 40
        repo = MagicMock()
        repo.get_git_ref.return_value = ref
        repo.get_git_tag.return_value = tag
        _github_client_fixture(monkeypatch, repo)

        assert remote.resolve_signature("tok", "o/r", "github.com", "v2.0.0") == (
            "v2.0.0",
            "b" * 40,
        )
        repo.get_git_tag.assert_called_once_with("tag-object-sha")
        repo.get_git_ref.assert_called_once_with("tags/v2.0.0")

    def test_latest_uses_most_recent_tag(self, monkeypatch):
        # Create older tag with timestamp 1000
        older = MagicMock()
        older.name = "v1.0.0"
        older.commit.sha = "b" * 40
        older.commit.commit.committer.date.timestamp.return_value = 1000

        # Create newer tag with timestamp 2000
        newer = MagicMock()
        newer.name = "v2.0.0"
        newer.commit.sha = "c" * 40
        newer.commit.commit.committer.date.timestamp.return_value = 2000

        repo = MagicMock()
        # Put older tag first in list to verify selection is by timestamp, not position
        repo.get_tags.return_value = [older, newer]
        _github_client_fixture(monkeypatch, repo)

        assert remote.resolve_signature("token", "owner/repo", "github.com", "latest") == (
            "v2.0.0",
            "c" * 40,
        )

    def test_latest_empty_version_id(self, monkeypatch):
        first = MagicMock()
        first.name = "v0.7.0"
        first.commit.sha = "d" * 40
        first.commit.commit.committer.date.timestamp.return_value = 1500
        repo = MagicMock()
        repo.get_tags.return_value = [first]
        _github_client_fixture(monkeypatch, repo)

        assert remote.resolve_signature("tok", "owner/repo", "github.com", "") == (
            "v0.7.0",
            "d" * 40,
        )

    def test_latest_no_tags_returns_none(self, monkeypatch):
        repo = MagicMock()
        repo.get_tags.return_value = []
        _github_client_fixture(monkeypatch, repo)

        assert remote.resolve_signature("tok", "owner/repo", "github.com", "latest") is None

    def test_api_error_returns_none(self, monkeypatch):
        client = MagicMock()
        client.get_repo.side_effect = Exception("boom")
        monkeypatch.setattr(remote, "_github_client", lambda token, host: client)

        assert remote.resolve_signature("tok", "owner/repo", "github.com", "v1.0.0") is None

    def test_missing_package_returns_none(self, monkeypatch):
        monkeypatch.setattr(remote, "_github_client", lambda token, host: None)

        assert remote.resolve_signature("tok", "owner/repo", "github.com", "v1.0.0") is None


def _tag(name: str, sha: str) -> MagicMock:
    tag = MagicMock()
    tag.name = name
    tag.commit.sha = sha
    return tag


class TestGetAllTags:
    def test_returns_tag_names(self, monkeypatch):
        repo = MagicMock()
        repo.get_tags.return_value = [_tag("v1.0.0", "a"), _tag("v1.1.0", "b")]
        _github_client_fixture(monkeypatch, repo)

        assert remote.get_all_tags("tok", "owner/repo", "github.com") == ["v1.0.0", "v1.1.0"]

    def test_api_error_returns_none(self, monkeypatch):
        client = MagicMock()
        client.get_repo.side_effect = Exception("boom")
        monkeypatch.setattr(remote, "_github_client", lambda token, host: client)

        assert remote.get_all_tags("tok", "owner/repo", "github.com") is None

    def test_missing_package_returns_none(self, monkeypatch):
        monkeypatch.setattr(remote, "_github_client", lambda token, host: None)

        assert remote.get_all_tags("tok", "owner/repo", "github.com") is None


class TestFormatActionSignatureApi:
    def test_sha_resolves_via_api(self, monkeypatch):
        ref = MagicMock()
        ref.object.type = "commit"
        ref.object.sha = "e" * 40
        repo_mock = MagicMock()
        repo_mock.get_git_ref.return_value = ref
        _github_client_fixture(monkeypatch, repo_mock)

        context = MagicMock()
        context.environment.globals = {
            "resolve_sha": lambda tag: ("v1.2.3", "e" * 40),
            "repository_name": "owner/repo",
            "repository_host": "github.com",
            "git_repo": "not_a_repo",
        }
        options = GitHubOptions(signature_version="sha", signature_version_id="v1.2.3")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == f"owner/repo@{'e' * 40} # v1.2.3"

    def test_sha_latest_resolves_via_api(self, monkeypatch):
        first = MagicMock()
        first.name = "v2.1.0"
        first.commit.sha = "f" * 40
        first.commit.commit.committer.date.timestamp.return_value = 3000
        repo_mock = MagicMock()
        repo_mock.get_tags.return_value = [first]
        _github_client_fixture(monkeypatch, repo_mock)

        context = MagicMock()
        context.environment.globals = {
            "resolve_sha": lambda tag: ("v2.1.0", "f" * 40),
            "repository_name": "owner/repo",
            "repository_host": "github.com",
            "git_repo": "not_a_repo",
        }
        options = GitHubOptions(signature_version="sha")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == f"owner/repo@{'f' * 40} # v2.1.0"

    def test_sha_api_error_falls_back_to_local(self, tmp_path, monkeypatch):
        repo_local = git.Repo.init(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        repo_local.index.add([str(test_file)])
        commit = repo_local.index.commit("Initial commit")
        repo_local.create_tag("v9.9.9")

        client = MagicMock()
        client.get_repo.side_effect = Exception("boom")
        monkeypatch.setattr(remote, "_github_client", lambda token, host: client)

        context = MagicMock()
        context.environment.globals = {
            "github_token": "tok",
            "repository_name": "owner/repo",
            "repository_host": "github.com",
            "git_repo": repo_local,
        }
        options = GitHubOptions(signature_version="sha", signature_version_id="v9.9.9")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == f"owner/repo@{commit.hexsha} # v9.9.9"

    def test_sha_without_token_uses_local_git(self, tmp_path):
        repo_local = git.Repo.init(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        repo_local.index.add([str(test_file)])
        commit = repo_local.index.commit("Initial commit")
        repo_local.create_tag("v1.0.0")

        context = MagicMock()
        context.environment.globals = {
            "git_repo": repo_local,
        }
        options = GitHubOptions(signature_version="sha", signature_version_id="v1.0.0")
        result = format_action_signature(context, ".", "owner/repo", options)
        assert result == f"owner/repo@{commit.hexsha} # v1.0.0"


class TestGetReleases:
    def test_uses_api_when_token_present(self, handler, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "tok")
        monkeypatch.setattr(
            remote,
            "get_all_tags",
            lambda token, repo_name, host: ["v2.0.0", "v1.0.0", "v1", "not-a-version"],
        )
        handler.get_releases()
        assert handler.semver == "v2.0.0"
        assert handler.major == "v1"

    def test_api_failure_falls_back_to_local(self, handler, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "tok")
        monkeypatch.setattr(
            remote,
            "get_all_tags",
            lambda token, repo_name, host: None,
        )
        handler.get_releases()
        assert isinstance(handler.semver, str)
        assert isinstance(handler.major, str)
