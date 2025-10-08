# Signatures options

??? info "Example action/workflow"

    ??? preview "compsite action `action.yaml`"

        ```yaml title="action.yaml"
        --8<-- "action.yaml"
        ```

    ??? preview "reusable workflow `.github/workflows/example_workflow.yml`"

        ```yaml title=".github/workflows/example_workflow.yml"
        --8<-- ".github/workflows/example_workflow.yml"
        ```

::: mkdocstrings_handlers.github.config.GitHubOptions.show_signature
    handler: python

??? preview

    === "`show_signature: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                show_signature: true

    === "`show_signature: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_signature: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_show_secrets
    handler: python

??? preview

    === "`signature_show_secrets: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_secrets: false

    === "`signature_show_secrets: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_secrets: true

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_show_permissions
    handler: python

??? preview

    === "`signature_show_permissions: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_permissions: true

    === "`signature_show_permissions: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_permissions: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_version
    handler: python

!!! info

    To automatically grab the latest `major` or `semver` release, *mkdocstrings-github* uses local git tags matching the patterns `vX` (major) and `vX.Y.Z` (semver). Make sure your repository has appropriate tags if you wish to use these versioning options.

    When building your documentation in GitHub Actions, make sure that the checkout will have access to the git tags associated with the action/workflow versions. This is best done by specifying a checkout filter:

    ```yaml title="Example checkout"
    ...
    - name: checkout
      uses: actions/checkout@v5
      with:
        filter: tree:0
    ...
    - name: build step
      run: mkdocs build 
    ```
    -  

??? preview

    === "`signature_version: ref`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: my_current_branch

    === "`signature_version: major`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: v1

    === "`signature_version: semver`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: v1.2.3

    === "`signature_version: string`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: a_custom_version

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_version_string
    handler: python

??? preview

    === "`signature_version_string: latest`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: latest

    === "`signature_version_string: foobar`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: foobar
