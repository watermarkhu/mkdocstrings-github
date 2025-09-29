# Parameters options

??? info "Example action/workflow"

    ??? preview "compsite action `action.yaml`"

        ```yaml title="action.yaml"
        --8<-- "action.yaml"
        ```

    ??? preview "reusable workflow `.github/workflows/example_workflow.yml`"

        ```yaml title=".github/workflows/example_workflow.yml"
        --8<-- ".github/workflows/example_workflow.yml"
        ```

::: mkdocstrings_handlers.github.config.GitHubOptions.show_inputs
    handler: python

??? preview

    === "`show_inputs: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_inputs: true

    === "`show_inputs: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_inputs: false

::: mkdocstrings_handlers.github.config.GitHubOptions.show_inputs_only_required
    handler: python

??? preview

    === "`show_inputs_only_required: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_inputs_only_required: false

    === "`show_inputs_only_required: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_inputs_only_required: true

::: mkdocstrings_handlers.github.config.GitHubOptions.show_outputs
    handler: python

??? preview

    === "`show_outputs: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_outputs: false

    === "`show_outputs: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_outputs: true

::: mkdocstrings_handlers.github.config.GitHubOptions.show_secrets
    handler: python

??? preview

    === "`show_secrets: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_secrets: true

    === "`show_secrets: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_secrets: false

::: mkdocstrings_handlers.github.config.GitHubOptions.show_secrets_only_required
    handler: python

??? preview

    === "`show_secrets_only_required: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_secrets_only_required: false

    === "`show_secrets_only_required: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_secrets_only_required: true

::: mkdocstrings_handlers.github.config.GitHubOptions.parameters_order
    handler: python

??? preview

    === "`parameters_order: 'source'`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                parameters_order: 'source'

    === "`parameters_order: 'alphabetical'`"

        ::: .github/workflows/example_workflow.yml
            options:
                parameters_order: 'alphabetical'

::: mkdocstrings_handlers.github.config.GitHubOptions.parameters_section_style
    handler: python

??? preview

    === "`parameters_section_style: 'table'`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                parameters_section_style: 'table'

    === "`parameters_section_style: 'list'`"

        ::: .github/workflows/example_workflow.yml
            options:
                parameters_section_style: 'list'

::: mkdocstrings_handlers.github.config.GitHubOptions.parameters_anchors
    handler: python


!!! tip "Cross linking parameters"

    It is possible to cross-link parameters within the yaml descriptions by a markdown link in the format `[text](#<domain>.<name>)`. 

    E.g. the input `my_input` can be linked with `[text](#inputs.my_input)` the secret `MY_SECRET` is linked with `[text](#secrets.MY_SECRET)`.

??? preview

    === "`parameters_anchors: true`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                parameters_anchors: true

    === "`parameters_anchors: false`"

        ::: .github/workflows/example_workflow.yml
            options:
                parameters_anchors: false