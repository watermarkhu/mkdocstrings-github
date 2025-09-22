from dataclasses import dataclass, field
from enum import Enum
from os import PathLike
from typing import Any, Literal, Optional

from yaml import Loader, load


@dataclass
class Input:
    name: str
    description: str = ""
    required: bool = False
    type: Literal["boolean", "number", "string"] = "string"
    default: bool | float | int | str | None = None
    deprecationMessage: Optional[str] = None

    @staticmethod
    def from_data(
        name: str,
        description: str = "",
        required: bool = False,
        type: Literal["boolean", "number", "string"] = "string",
        default: bool | float | int | str | None = None,
        deprecationMessage: Optional[str] = None,
        **kwargs,
    ) -> "Input":
        return Input(name, description, required, type, default, deprecationMessage)


@dataclass
class Output:
    name: str
    description: str = ""

    @staticmethod
    def from_data(name: str, description: str = "", **kwargs) -> "Output":
        return Output(name, description)


@dataclass
class Secret:
    name: str
    description: str = ""
    required: bool = False

    @staticmethod
    def from_data(name: str, description: str = "", required: bool = False, **kwargs) -> "Secret":
        return Secret(name, description, required)


def _get_member(d: dict, key: str, error_message: str = "", default: Any = None) -> Any:
    if key not in d:
        if default is not None:
            return default
        raise KeyError(error_message)
    return d[key]


@dataclass
class Action:
    # https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax
    file: PathLike
    name: str
    description: str
    using: str
    author: str = ""
    inputs: list[Input] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)

    @staticmethod
    def from_file(file: PathLike) -> "Action":
        with open(file, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)

        action = Action(
            file=file,
            name=_get_member(data, "name", "Action must have a name"),
            description=_get_member(data, "description", "Action must have a description"),
            using=_get_member(data, "runs", "Action must have a 'runs' section").get("using", ""),
            author=_get_member(data, "author", default=""),
        )
        for key, value in data.get("inputs", {}).items():
            action.inputs.append(Input.from_data(key, **value))
        for key, value in data.get("outputs", {}).items():
            action.outputs.append(Output.from_data(key, **value))
        return action


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

    def __le__(self, other):
        if isinstance(other, PermissionLevel):
            return self.number <= other.number
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, PermissionLevel):
            return self.number < other.number
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, PermissionLevel):
            return self.number >= other.number
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PermissionLevel):
            return self.number > other.number
        return NotImplemented


@dataclass
class Workflow:
    # https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    file: PathLike
    name: str
    permissions: dict[str, PermissionLevel] = field(default_factory=dict)
    inputs: list[Input] = field(default_factory=list)
    secrets: list[Secret] = field(default_factory=list)
    outputs: list[Output] = field(default_factory=list)

    @staticmethod
    def from_file(file: PathLike) -> "Workflow | None":
        with open(file, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)

        if True not in data or "workflow_call" not in data[True]:
            return None
        call = data[True]["workflow_call"]

        workflow = Workflow(
            file=file,
            name=_get_member(data, "name", "Workflow must have a name"),
        )
        for key, value in call.get("inputs", {}).items():
            workflow.inputs.append(Input.from_data(key, **value))
        for key, value in call.get("outputs", {}).items():
            workflow.outputs.append(Output.from_data(key, **value))
        for key, value in call.get("secrets", {}).items():
            workflow.secrets.append(Secret.from_data(key, **value))

        for key, label in data.get("permisions", {}).items():
            workflow.permissions[key] = PermissionLevel.from_label(label)
        for job in data.get("jobs", {}).values():
            for key, label in job.get("permisions", {}).items():
                if key in workflow.permissions:
                    if permission := PermissionLevel.from_label(label) > workflow.permissions[key]:
                        workflow.permissions[key] = permission
                else:
                    workflow.permissions[key] = PermissionLevel.from_label(label)
        return workflow
