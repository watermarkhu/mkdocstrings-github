"""API-based tag and commit SHA resolution for GitHub.

When a `GITHUB_TOKEN` environment variable is set, git tags do not need to be checked
out locally: the most recent tag and the commit SHA of any tag can be resolved through
the GitHub API. This requires the optional `PyGithub` dependency, installable with
`pip install mkdocstrings-github[api]`.
"""

from __future__ import annotations

import importlib
import os
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from mkdocstrings import get_logger

if TYPE_CHECKING:
    from git import Repo

_Github: Any = None
try:
    _Github = importlib.import_module("github").Github
except ImportError:  # pragma: no cover - exercised via monkeypatching in tests
    pass


ENV_GITHUB_TOKEN = "GITHUB_TOKEN"
ENV_GITHUB_TOKEN_ALT = "GH_TOKEN"

logger = get_logger(__name__)


def github_token() -> str | None:
    """Return the GitHub token from the environment, if any."""
    return os.environ.get(ENV_GITHUB_TOKEN) or os.environ.get(ENV_GITHUB_TOKEN_ALT) or None


def resolve_provider() -> str | None:
    """Return `github` when a token is available, or `None` otherwise."""
    if os.environ.get("GITHUB_ACTIONS") == "true" or github_token():
        return "github"
    return None


def repository_host(repo: Repo) -> str:
    """Return the repository host (e.g. `github.com`) from the git remotes."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return _actions_host()
    for remote in repo.remotes:
        for url in remote.urls:
            host = _parse_git_url_host(url)
            if host:
                return host
    return "github.com"


def _actions_host() -> str:
    """Return the GitHub server host from the Actions environment, or `github.com`.

    On GitHub Enterprise Server, the workflow runs against a different instance
    (e.g. `https://ghes.example.com`), so the server URL must be used instead of
    hardcoding `github.com`.
    """
    for var in ("GITHUB_SERVER_URL", "GITHUB_API_URL"):
        host = _parse_git_url_host(os.environ.get(var) or "")
        if host:
            return host if host != "api.github.com" else "github.com"
    return "github.com"


def _parse_git_url_host(url: str) -> str | None:
    """Parse a git URL and return the hostname.

    Handles both HTTPS URLs (https://host/path) and SSH URLs (git@host:path).
    Returns None if the URL cannot be parsed.
    """
    # Try parsing as HTTPS URL first
    if url.startswith(("http://", "https://")):
        try:
            parsed = urlparse(url)
            if parsed.hostname:
                return parsed.hostname
        except Exception:
            return None

    # Try parsing as SSH-style URL (git@host:path or user@host:path)
    if "@" in url and ":" in url:
        try:
            # Extract the part between @ and :
            at_index = url.index("@")
            colon_index = url.index(":", at_index)
            host = url[at_index + 1 : colon_index]
            # Basic validation: host should not be empty and should not contain invalid characters
            if host and not any(c in host for c in [" ", "\n", "\r", "\t"]):
                return host
        except Exception:
            return None

    return None


def _github_client(token: str, host: str) -> Any:
    if _Github is None:
        logger.warning(
            "A GITHUB_TOKEN is set, but 'PyGithub' is not installed. "
            "Install it with 'pip install mkdocstrings-github[api]' to resolve tags via the API."
        )
        return None

    if host in ("", "github.com"):
        return _Github(token)
    return _Github(token, base_url=f"https://{host}/api/v3")


def resolve_signature(
    token: str, repo_name: str, host: str, version_id: str
) -> tuple[str, str] | None:
    """Resolve a version id to a `(tag, commit_sha)` pair through the GitHub API.

    A `version_id` of `latest` (or empty) resolves to the most recently created tag
    based on commit date, matching the behavior of `rendering.get_latest_tag`.
    Returns `None` if the resolution fails, in which case callers should fall back
    to the local git repository.
    """
    client = _github_client(token, host)
    if client is None:
        return None
    try:
        repo = client.get_repo(repo_name)
        if version_id in ("", "latest"):
            # Select the most recently created tag based on commit date
            latest_tag = None
            latest_date = 0
            for tag in repo.get_tags():
                # Get the commit date for this tag
                try:
                    commit = tag.commit
                    # Use the committer date (equivalent to committed_date in GitPython)
                    commit_date = commit.commit.committer.date.timestamp()
                    if commit_date > latest_date:
                        latest_date = commit_date
                        latest_tag = tag
                except Exception:
                    # Skip tags that we can't get date for
                    continue
            if latest_tag is None:
                return None
            return latest_tag.name, latest_tag.commit.sha
        ref = repo.get_git_ref(f"tags/{version_id}")
        if ref.object.type == "tag":
            return version_id, repo.get_git_tag(ref.object.sha).object.sha
        return version_id, ref.object.sha
    except Exception:
        return None


def get_all_tags(token: str, repo_name: str, host: str) -> list[str] | None:
    """Return all tag names through the GitHub API, or `None` if unavailable."""
    client = _github_client(token, host)
    if client is None:
        return None
    try:
        return [tag.name for tag in client.get_repo(repo_name).get_tags()]
    except Exception:
        return None
