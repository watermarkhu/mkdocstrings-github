"""API-based tag and commit SHA resolution for GitHub.

When a `GITHUB_TOKEN` environment variable is set, git tags do not need to be checked
out locally: the most recent tag and the commit SHA of any tag can be resolved through
the GitHub API. This requires the optional `PyGithub` dependency, installable with
`pip install mkdocstrings-github[api]`.
"""

from __future__ import annotations

import importlib
import os
import re
from typing import TYPE_CHECKING, Any

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

_REMOTE_RE = re.compile(r"(?P<host>[\w\.-]+)[/:](?P<owner>[^/]+)/(?P<repo>[^/.]+?)(?:\.git)?$")


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
        return "github.com"
    for remote in repo.remotes:
        for url in remote.urls:
            match = _REMOTE_RE.search(url)
            if match:
                return match.group("host")
    return "github.com"


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

    A `version_id` of `latest` (or empty) resolves to the most recent tag returned by the
    GitHub tags listing. Returns `None` if the resolution fails, in which case callers
    should fall back to the local git repository.
    """
    client = _github_client(token, host)
    if client is None:
        return None
    try:
        repo = client.get_repo(repo_name)
        if version_id in ("", "latest"):
            for tag in repo.get_tags():
                return tag.name, tag.commit.sha
            return None
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
