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
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`show_signature: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                show_signature: false
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_repository
    handler: python

!!! tip 

    By default the current repository name is automatically grabbed from either the GitHub Actions environment or the git remotes. 
    This option only serves to *customize* the shown repository in the signature. 

??? preview

    === "`signature_repository: username/repo`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_repository: 'username/repo'
                show_inputs: false
                show_secrets: false
                show_source: false
                
    === "`signature_repository: organization/repository`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                signature_repository: organization/repository
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_show_secrets
    handler: python

??? preview

    === "`signature_show_secrets: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_secrets: false
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_show_secrets: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_secrets: true
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_show_permissions
    handler: python

??? preview

    === "`signature_show_permissions: true`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_permissions: true
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_show_permissions: false`"
        
        ::: .github/workflows/example_workflow.yml
            options:
                signature_show_permissions: false
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_version
    handler: python

!!! info

    To automatically grab the latest `major` or `semver` release, *mkdocstrings-github* uses local git tags matching the patterns `vX` (major) and `vX.Y.Z` (semver). Make sure your repository has appropriate tags if you wish to use these versioning options.

    When using `signature_version: sha`, the [`signature_version_tag`][mkdocstrings_handlers.github.config.GitHubOptions.signature_version_tag] option defaults to `latest`, which grabs the most recently created tag in the repository (based on its creation date).

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

??? preview

    === "`signature_version: ref`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: my_current_branch
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version: major`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: v1
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version: semver`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: v1.2.3
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version: string`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: a_custom_version
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version: sha`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: sha
                signature_version_tag: latest
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_version_string
    handler: python

??? preview

    === "`signature_version_string: latest`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: latest
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version_string: foobar`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: string
                signature_version_string: foobar
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_version_tag
    handler: python

??? preview

    === "`signature_version_tag: latest` (default)"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: sha
                show_inputs: false
                show_secrets: false
                show_source: false

    === "`signature_version_tag: v0.7.0`"

        ::: .github/workflows/example_workflow.yml
            options:
                signature_version: sha
                signature_version_tag: v0.7.0
                show_inputs: false
                show_secrets: false
                show_source: false

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_prematter
    handler: python

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_indent
    handler: python

::: mkdocstrings_handlers.github.config.GitHubOptions.signature_postmatter
    handler: python
    
::: mkdocstrings_handlers.github.config.GitHubOptions.signature_postmatter_indent
    handler: python

??? preview

    ````md title="markdown syntax"
    ::: .github/workflows/example_workflow.yml
        options:
          signature_prematter: |
            name: Example workflow
            on:
              workflow_dispatch:
            jobs:
              example:
          signature_indent: 4
          signature_postmatter_indent: 2
          signature_postmatter: |
            subsequent:
              name: subsequent job
              needs: [example]
              ...
    ````

    ::: .github/workflows/example_workflow.yml
        options:
          signature_prematter: |
            name: Example workflow
            on:
              workflow_dispatch:
            jobs:
              example:
          signature_indent: 4
          signature_postmatter_indent: 2
          signature_postmatter: |
              subsequent:
                name: subsequent job
                needs: [example]
                ...
