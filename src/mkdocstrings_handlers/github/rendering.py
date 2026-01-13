from __future__ import annotations

import os
from collections import OrderedDict
from typing import TYPE_CHECKING, Sequence

from jinja2 import pass_context

from mkdocstrings_handlers.github.config import PARAMETERS_ORDER, STEP_DIRECTION, GitHubOptions
from mkdocstrings_handlers.github.objects import Input, Output, Secret, Workflow

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


def generate_mermaid_flowchart(workflow: Workflow, direction: STEP_DIRECTION = "TB") -> str:
    """Generate a Mermaid flowchart for a reusable workflow.

    Args:
        workflow: The workflow object containing jobs and steps.
        direction: The direction of steps within jobs (TB for top-to-bottom, LR for left-to-right).

    Returns:
        A Mermaid flowchart diagram as a string.
    """
    if not workflow.jobs:
        return ""

    lines = ["flowchart TB"]

    # Track all nodes for dependency linking
    job_start_nodes = {}
    job_end_nodes = {}

    for job in workflow.jobs.values():
        job_id_safe = job.mermaid_id

        # Check if job calls another workflow (has any steps with workflow set)
        if job.uses is not None:
            # Job that calls a workflow - render as a single subroutine node
            lines.append(f'    {job_id_safe}[["{job.name}"]]')
            job_start_nodes[job.id] = job_id_safe
            job_end_nodes[job.id] = job_id_safe
            continue

        # Regular job - render as a subgraph with steps

        lines.append(f'    subgraph {job_id_safe}["{job.name}"]')
        lines.append(f"        direction {direction}")

        if job.steps:
            # Filter steps that have a name
            named_steps = [(idx, step) for idx, step in enumerate(job.steps) if step.name]

            if named_steps:
                prev_step_id = None

                for idx, step in named_steps:
                    step_id = f"{job_id_safe}_step_{idx}"
                    step_name = step.name

                    # Escape special characters in step names
                    step_name_escaped = (
                        step_name.replace('"', "&quot;").replace("[", "&#91;").replace("]", "&#93;")
                    )

                    # Determine node style based on step type
                    if step.uses:
                        # Action uses get rounded rectangle
                        lines.append(f'        {step_id}("{step_name_escaped}")')
                    else:
                        # Regular run steps get standard rectangle
                        lines.append(f'        {step_id}["{step_name_escaped}"]')

                    # Link to previous step
                    if prev_step_id:
                        lines.append(f"        {prev_step_id} --> {step_id}")

                    prev_step_id = step_id

                # Track first and last step nodes for job dependencies
                first_step_idx, _ = named_steps[0]
                last_step_idx, _ = named_steps[-1]
                first_step_id = f"{job_id_safe}_step_{first_step_idx}"
                last_step_id = f"{job_id_safe}_step_{last_step_idx}"
                job_start_nodes[job.id] = first_step_id
                job_end_nodes[job.id] = last_step_id
            else:
                # Job with no named steps - create a single placeholder node
                placeholder_id = f"{job_id_safe}_placeholder"
                lines.append(f"        {placeholder_id}[No named steps defined]")
                job_start_nodes[job.id] = placeholder_id
                job_end_nodes[job.id] = placeholder_id
        else:
            # Job with no steps - create a single node
            placeholder_id = f"{job_id_safe}_placeholder"
            lines.append(f"        {placeholder_id}[No steps defined]")
            job_start_nodes[job.id] = placeholder_id
            job_end_nodes[job.id] = placeholder_id

        lines.append("    end")

    # Add job dependencies
    for job in workflow.jobs.values():
        for needed_job_id in job.needs:
            needed_job = workflow.jobs[needed_job_id]
            lines.append(f"    {needed_job.mermaid_id} -.-> {job.mermaid_id}")

    return "\n".join(lines)
