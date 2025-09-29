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

    To automatically grab the latest `major` or `semver` release, *mkdocstrings-github* needs to access GitHub to get the releases. Authentication is set by either the environment variable `GH_TOKEN`, or via [`.netrc`](https://pygithub.readthedocs.io/en/stable/examples/Authentication.html#netrc-authentication). If both aren't available, a final attempt is made via the GitHub CLI with [`gh auth token`](https://cli.github.com/manual/gh_auth_token). 

    When building your documentation in GitHub Actions, make sure that the build step has the environment variable `GH_TOKEN` set.

    ```yaml title="Example build step"
    ...
    - name: build step
      env:
        GH_TOKEN: ${{ github.token }}
      run: | 
        mkdocs build 
    ```

!!! info

    For GitHub Enterprise instances, you can set either the [`hostname`][mkdocstrings_handlers.github.config.GitHubConfig.hostname] configuration option or the `GH_HOST` environment variable to your GitHub hostname.

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
