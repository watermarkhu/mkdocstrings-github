---
hide:
- feedback
---

--8<-- "README.md:header"

<p align="center"><img width=300px src="img/logo.png"></p>

--8<-- "README.md:footer"

!!! note

    Currently, only the [Material for MkDocs](https://github.com/squidfunk/mkdocs-material) theme is supported.

???+ example

    The following `action.yaml` file

    ??? quote "action.yaml"

        ```yaml
        --8<-- "action.yaml"
        ```
    
    will be shown in the documentation as:

    <div class="result" markdown>
    ::: .
        options:
            show_outputs: true
            signature_version: string
            signature_version_string: v5
            signature_repository: actions/checkout
            show_source: false
    </div>
