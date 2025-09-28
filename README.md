<!-- --8<-- [start:header] -->

<h1 align="center">mkdocstrings-github</h1>

<p align="center">A GitHub Actions handler for <a href="https://github.com/mkdocstrings/mkdocstrings"><i>mkdocstrings</i></a>.</p>

<p align="center"><img width=300px src="logo.png"></p>

[![Qualify](https://github.com/watermarkhu/mkdocstrings-github/actions/workflows/qualify.yaml/badge.svg?branch=main)](https://github.com/watermarkhu/mkdocstrings-github/actions/workflows/qualify.yaml)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://watermarkhu.nl/mkdocstrings-github)
[![pypi version](https://img.shields.io/pypi/v/mkdocstrings-github.svg)](https://pypi.org/project/mkdocstrings-github/)

<!-- --8<-- [end:header] -->
<!-- --8<-- [start:install] -->
You can install the GitHub handler by specifying it as a dependency:

```toml title="pyproject.toml"
# PEP 621 dependencies declaration
# adapt to your dependencies manager
[project]
dependencies = [
    "mkdocstrings-github>=0.X.Y",
]
```
<!-- --8<-- [end:install] -->

<!-- --8<-- [start:footer] -->

## Features

- 📝 **Automatic Example Signature**: Displays an example call signature alongside the description. The version shown can be the latest release, latest major, current reference, or any custom string.
- ✨ **Enhanced Markdown Descriptions**: All description elements are parsed using a markdown parser, enabling comprehensive formatting and rich documentation capabilities.
- 🧩 **Individual Parameter Hyperlinks**: Each action or workflow parameter—including inputs, outputs, and secrets—receives a unique HTML id, facilitating direct linking to specific parameter documentation.
- 🔒 **Automated Permission Aggregation**: For reusable workflows, if permissions are specified at the job level rather than the workflow level, the required final permissions are automatically determined and displayed in the signature.
- 🔗 **Parameter cross-linking**: Link to other parameters of the action or workflow via a simple Markdown syntax.

<!-- --8<-- [end:footer] -->
