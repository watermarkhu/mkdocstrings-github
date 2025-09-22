"""Configuration and options dataclasses."""

from __future__ import annotations

import re
import sys
from dataclasses import field
from typing import Annotated, Any, Literal

from mkdocstrings import get_logger

# YORE: EOL 3.10: Replace block with line 2.
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


logger = get_logger(__name__)


try:
    # When Pydantic is available, use it to validate options (done automatically).
    # Users can therefore opt into validation by installing Pydantic in development/CI.
    # When building the docs to deploy them, Pydantic is not required anymore.

    # When building our own docs, Pydantic is always installed (see `docs` group in `pyproject.toml`)
    # to allow automatic generation of a JSON Schema. The JSON Schema is then referenced by mkdocstrings,
    # which is itself referenced by mkdocs-material's schema system. For example in VSCode:
    #
    # "yaml.schemas": {
    #     "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    # }
    import pydantic

    if getattr(pydantic, "__version__", "1.").startswith("1."):
        raise ImportError  # noqa: TRY301

    from inspect import cleandoc

    from pydantic import Field as BaseField
    from pydantic.dataclasses import dataclass

    _base_url = "https://watermarkhu.nl/mkdocstrings-github/latest/usage/"

    def Field(  # noqa: N802, D103
        *args: Any,
        description: str,
        group: Literal["general", "parameters", "signatures"] | None = None,
        parent: str | None = None,
        **kwargs: Any,
    ) -> None:
        def _add_markdown_description(schema: dict[str, Any]) -> None:
            url = f"{_base_url}/{f'configuration/{group}/' if group else ''}#{parent or schema['title']}"
            schema["markdownDescription"] = f"[DOCUMENTATION]({url})\n\n{schema['description']}"

        return BaseField(
            *args,
            description=cleandoc(description),
            field_title_generator=lambda name, _: name,
            json_schema_extra=_add_markdown_description,
            **kwargs,
        )
except ImportError:
    from dataclasses import dataclass

    def Field(*args: Any, **kwargs: Any) -> None:
        pass


SIGNATURE_VERSION = Literal["major", "semver", "string"]
PARAMETERS_ORDER = Literal["alphabetical", "source"]
PARAMETERS_SECTION_STYLE = Literal["table", "list"]


@dataclass(frozen=True, kw_only=True)
class GitHubOptions:
    """Input options for the GitHub handler."""

    # General options
    show_description: Annotated[
        bool,
        Field(
            group="general",
            description="Whether to show the description in the documentation.",
        ),
    ] = True
    show_source: Annotated[
        bool,
        Field(
            group="general",
            description="Whether to show the source link in the documentation.",
        ),
    ] = False

    # Signature options
    show_signature: Annotated[
        bool,
        Field(
            group="signatures",
            description="Whether to show the signature in the documentation.",
        ),
    ] = True

    separate_signature: Annotated[
        bool,
        Field(
            group="signatures",
            description="""Whether to put the whole signature in a code block below the heading.""",
        ),
    ] = False

    signature_show_secrets: Annotated[
        bool,
        Field(
            group="signatures",
            description="Whether to show secrets in the signature.",
        ),
    ] = False

    signature_version: Annotated[
        SIGNATURE_VERSION,
        Field(
            group="signatures",
            description="The versioning scheme to use for the signature.",
        ),
    ] = "major"

    signature_version_string: Annotated[
        str,
        Field(
            group="signatures",
            description="The version string to use if `signature_version` is set to `string`.",
        ),
    ] = "latest"

    # Parameter options
    parameters_order: Annotated[
        PARAMETERS_ORDER,
        Field(
            group="parameters",
            description="""The parameters ordering to use.

            - `alphabetical`: order by the parameters names,
            - `source`: order parameters as they appear in the source file.
            """,
        ),
    ] = "alphabetical"

    parameters_section_style: Annotated[
        PARAMETERS_SECTION_STYLE,
        Field(
            group="parameters",
            description="The style used to render docstring sections.",
        ),
    ] = "table"

    parameters_anchors: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to add anchors to parameters in the documentation.",
        ),
    ] = True

    show_required_inputs: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to show required inputs in the documentation.",
        ),
    ] = True
    show_optional_inputs: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to show optional inputs in the documentation.",
        ),
    ] = False
    show_outputs: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to show outputs in the documentation.",
        ),
    ] = False
    show_secrets: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to show secrets in the documentation.",
        ),
    ] = True
    show_permissions: Annotated[
        bool,
        Field(
            group="parameters",
            description="Whether to show permissions in the documentation.",
        ),
    ] = False

    @classmethod
    def from_data(cls, **data: Any) -> Self:
        """Create an instance from a dictionary."""
        return cls(**data)


@dataclass(frozen=True, kw_only=True)
class GitHubConfig:
    """Configuration options for the GitHub handler."""

    repo: Annotated[
        str,
        Field(
            description="The GitHub repository in the format 'owner/repo'.",
            parent="repo",
            pattern=re.compile(r"^[\w.-]+/[\w.-]+$"),
        ),
    ] = field(default_factory=lambda: ".")
    options: Annotated[
        GitHubOptions,
        Field(
            description="Options for the GitHub handler.",
            parent="options",
        ),
    ] = field(default_factory=GitHubOptions)

    @classmethod
    def from_data(cls, **data: Any) -> Self:
        """Create an instance from a dictionary."""
        return cls(**data)
