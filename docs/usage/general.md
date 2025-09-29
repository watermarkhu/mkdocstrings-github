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
                toc_label: "f"