from __future__ import annotations

import os
from collections import OrderedDict
from typing import TYPE_CHECKING, Sequence

from jinja2 import pass_context

from mkdocstrings_handlers.github.config import PARAMETERS_ORDER, GitHubOptions
from mkdocstrings_handlers.github.objects import Input, Output, Secret

if TYPE_CHECKING:
    from git import Repo
    from jinja2.runtime import Context


ENV_MAJOR_TAG = "MKDOCSTRINGS_GITHUB_MAJOR_TAG"
ENV_SEMVER_TAG = "MKDOCSTRINGS_GITHUB_SEMVER_TAG"


@pass_context
def format_action_signature(context: Context, id: str, repo: str, options: GitHubOptions) -> str:
    name = repo if id == "." else f"{repo}/{id}"
    match options.signature_version:
        case "ref":
            try:
                git_repo = context.environment.globals["git_repo"]
                if isinstance(git_repo, Repo):
                    version = git_repo.head.ref.name
                else:
                    version = "unknown"
            except Exception:
                version = "unknown"
        case "major":
            version = os.environ.get(ENV_MAJOR_TAG, context.environment.globals["major_tag"])
        case "semver":
            version = os.environ.get(ENV_SEMVER_TAG, context.environment.globals["semver_tag"])
        case "string":
            version = options.signature_version_string

    return f"{name}@{version}"


def group_parameters(
    parameters: Sequence[Input | Output | Secret],
    do_group: bool,
) -> OrderedDict[str, list[Input | Output | Secret]]:
    grouped: OrderedDict[str, list[Input | Output | Secret]] = OrderedDict()
    if not do_group:
        grouped[""] = list(parameters)
        return grouped
    for parameter in parameters:
        group = getattr(parameter, "group", "")
        if group not in grouped:
            grouped[group] = []
        grouped[group].append(parameter)
    return grouped


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


def anchor_id(name: str, prefix: str, parent_id: str) -> str:
    anchor = f"{parent_id}--{prefix}.{name}"
    return anchor.replace(" ", "-")


def as_string(value: bool | str | int | float | None) -> str:
    match value:
        case bool():
            return "true" if value else "false"
        case str():
            return value
        case int() | float():
            return str(value)
        case None:
            return ""
        case _:
            raise TypeError(f"Unsupported type: {type(value)}")
