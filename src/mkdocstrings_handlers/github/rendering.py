from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from jinja2 import pass_context

from mkdocstrings_handlers.github.config import PARAMETERS_ORDER, GitHubOptions
from mkdocstrings_handlers.github.objects import Input, Output, Secret

if TYPE_CHECKING:
    from jinja2.runtime import Context


@pass_context
def format_action_signature(context: Context, id: str, repo: str, options: GitHubOptions) -> str:
    name = repo if id == "." else f"{repo}/{id}"
    match options.signature_version:
        case "major":
            version = "vMajor"
        case "semver":
            version = "vMajor.minor.patch"
        case "string":
            version = options.signature_version_string

    return f"{name}@{version}"


def order_parameters(
    parameters: Sequence[Input | Output | Secret], parameters_order: PARAMETERS_ORDER
):
    if parameters_order == "alphabetical":
        return sorted(parameters, key=lambda x: x.name)
    else:
        return parameters


def filter_parameters(
    parameters: Sequence[Input | Output | Secret],
    required: bool = False,
    optional: bool = False,
    description: bool = False,
    default: bool = False,
):
    filtered = []
    for parameter in parameters:
        filter = False
        if required and not getattr(parameter, "required", False):
            filter = True
        if optional and getattr(parameter, "required", False):
            filter = True
        if description and not getattr(parameter, "description", ""):
            filter = True
        if default and not getattr(parameter, "default", None):
            filter = True
        if not filter:
            filtered.append(parameter)
    return filtered
