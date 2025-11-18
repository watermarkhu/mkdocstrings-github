# General options

??? info "Example action/workflow"

    ??? preview "compsite action `action.yaml`"

        ```yaml title="action.yaml"
        --8<-- "action.yaml"
        ```

    ??? preview "reusable workflow `.github/workflows/example_workflow.yml`"

        ```yaml title=".github/workflows/example_workflow.yml"
        --8<-- ".github/workflows/example_workflow.yml"
        ```


::: mkdocstrings_handlers.github.config.GitHubOptions.show_description
    handler: python

??? preview

    === "`show_description: true`"

        ::: .
            options:
                show_description: true

    === "`show_description: false`"

        ::: .
            options:
                show_description: false

::: mkdocstrings_handlers.github.config.GitHubOptions.description
    handler: python

??? preview

    === "`description: ''`"

        ::: .

    === "`description: 'A custom description'`"

        ::: .
            options:
               description: 'A custom description'

::: mkdocstrings_handlers.github.config.GitHubOptions.show_source
    handler: python

??? preview

    === "`show_source: true`"

        ::: .
            options:
                show_source: true

    === "`show_source: false`"

        ::: .
            options:
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.workflow_flow_chart
    handler: python

This options leverages the [mkdocs-mermaid2](https://mkdocs-mermaid2.readthedocs.io) plugin to render the flow chart with [Mermaid.js](https://mermaid.js.org/). To use the default Material theme options, add the following to be set in your `mkdocs.yml`:

```yaml title="mkdocs.yml"
markdown_extensions:
  ...
  - pymdownx.superfences:
        # make exceptions to highlighting of code:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:mermaid2.fence_mermaid_custom
```

Alternatively, see how to customize the theme options [here](https://mkdocs-mermaid2.readthedocs.io/en/latest/#other-themes).

??? preview

    === "`workflow_flow_chart: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                workflow_flow_chart: true

    === "`workflow_flow_chart: false`"

        ::: .github/workflows/example_workflow.yml
            options:
                workflow_flow_chart: false
