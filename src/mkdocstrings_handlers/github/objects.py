import re
from dataclasses import dataclass, field
from enum import Enum
from os import PathLike
from typing import Any, Literal, Optional

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

yaml = YAML()


GROUP_PATTERN = r"#\s*group:\s*(.+)$"


def group_from_map(map: CommentedMap) -> str:
    """Extract group string from a comment line if it matches the group pattern."""
    if map.ca.comment:
        for comment in map.ca.comment:
            if comment is not None:
                group_matches = re.finditer(GROUP_PATTERN, comment.value)
                group_string = next((m.group(1).strip() for m in group_matches), "")
                if group_string:
                    return group_string
    return ""


@dataclass
class Input:
    name: str
    description: str = ""
    required: bool = False
    type: Literal["boolean", "number", "string"] = "string"
    default: bool | float | int | str | None = None
    deprecationMessage: Optional[str] = None
    group: str = ""


@dataclass
class Output:
    name: str
    description: str = ""
    value: str = ""
    group: str = ""


@dataclass
class Secret:
    name: str
    description: str = ""
    required: bool = False
    group: str = ""


def _get_member(d: dict, key: str, error_message: str = "", default: Any = None) -> Any:
    if key not in d:
        if default is not None:
            return default
        raise KeyError(error_message)
    return d[key]


def _read_file(file: PathLike) -> tuple[str, dict]:
    with open(file, "r", encoding="utf-8") as f:
        source = f.read()
        f.seek(0)
        data = yaml.load(f)
    return source, data


@dataclass
class Action:
    # https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax
    file: PathLike
    source: str
    id: str
    name: str
    description: str
    using: str
    author: str = ""
    inputs: list[Input] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
    branding: dict = field(default_factory=dict)
    template: Literal["action.html.jinja"] = "action.html.jinja"

    @staticmethod
    def from_file(file: PathLike, id: str) -> "Action":
        source, data = _read_file(file)

        action = Action(
            file=file,
            source=source,
            id=id,
            name=_get_member(data, "name", "Action must have a name"),
            description=_get_member(data, "description", "Action must have a description"),
            using=_get_member(data, "runs", "Action must have a 'runs' section").get("using", ""),
            author=_get_member(data, "author", default=""),
            branding=_get_member(data, "branding", default={}),
        )
        for key, value in data.get("inputs", {}).items():
            action.inputs.append(Input(name=key, **value, group=group_from_map(value)))
        for key, value in data.get("outputs", {}).items():
            action.outputs.append(Output(name=key, **value, group=group_from_map(value)))
        return action


# https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idpermissions
PERMISSION_SCOPES: list[str] = [
    "actions",
    "attestations",
    "checks",
    "contents",
    "deployments",
    "discussions",
    "id-token",
    "issues",
    "models",
    "packages",
    "pages",
    "pull-requests",
    "security-events",
    "statuses",
]


class PermissionLevel(Enum):
    none = ("none", 0)
    read = ("read", 1)
    write = ("write", 2)

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def number(self) -> int:
        return self.value[1]

    @staticmethod
    def from_label(label: str) -> "PermissionLevel":
        for perm in PermissionLevel:
            if perm.label == label:
                return perm
        raise ValueError(f"No Permission with label '{label}'")

    def __gt__(self, other):
        if isinstance(other, PermissionLevel):
            return self.number > other.number
        return NotImplemented


@dataclass
class Workflow:
    # https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    file: PathLike
    source: str
    id: str
    name: str
    description: str
    permissions: dict[str, PermissionLevel] = field(default_factory=dict)
    inputs: list[Input] = field(default_factory=list)
    secrets: list[Secret] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)
    template: Literal["workflow.html.jinja"] = "workflow.html.jinja"

    @property
    def permission_read_all(self) -> bool:
        return all(
            scope in self.permissions and self.permissions[scope] == PermissionLevel.read
            for scope in PERMISSION_SCOPES
        )

    @property
    def permission_write_all(self) -> bool:
        return all(
            scope in self.permissions and self.permissions[scope] == PermissionLevel.write
            for scope in PERMISSION_SCOPES
        )

    @staticmethod
    def from_file(file: PathLike, id: str) -> "Workflow | None":
        source, data = _read_file(file)

        if "on" not in data or "workflow_call" not in data["on"]:
            return None

        workflow = Workflow(
            file=file,
            source=source,
            id=id,
            name=_get_member(data, "name", "Workflow must have a name"),
            description=_get_member(data, "description", default=""),
        )

        call = data["on"]["workflow_call"]
        if call:
            for key, value in call.get("inputs", {}).items():
                workflow.inputs.append(Input(name=key, **value, group=group_from_map(value)))
            for key, value in call.get("outputs", {}).items():
                workflow.outputs.append(Output(name=key, **value, group=group_from_map(value)))
            for key, value in call.get("secrets", {}).items():
                workflow.secrets.append(Secret(name=key, **value, group=group_from_map(value)))

        def set_all_permissions(level: str):
            if level == "read-all":
                for key in PERMISSION_SCOPES:
                    workflow.permissions[key] = PermissionLevel.read
            elif level == "write-all":
                for key in PERMISSION_SCOPES:
                    workflow.permissions[key] = PermissionLevel.write
            else:
                raise ValueError(f"Unknown permission level '{level}'")

        if isinstance(permissions := data.get("permissions", {}), str):
            set_all_permissions(permissions)
        elif isinstance(permissions, dict):
            for key, label in permissions.items():
                workflow.permissions[key] = PermissionLevel.from_label(label)
        else:
            raise ValueError("permissions must be a string or a dictionary")
        for job in data.get("jobs", {}).values():
            if isinstance(permissions := job.get("permissions", {}), str):
                set_all_permissions(permissions)
            elif isinstance(permissions, dict):
                for key, label in job.get("permissions", {}).items():
                    if key in workflow.permissions:
                        permission = PermissionLevel.from_label(label)
                        if permission > workflow.permissions[key]:
                            workflow.permissions[key] = permission
                    else:
                        workflow.permissions[key] = PermissionLevel.from_label(label)
            else:
                raise ValueError("permissions must be a string or a dictionary")

        return workflow
