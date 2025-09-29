# Usage 

!!! info "Example action/workflow"

    Throughout the next pages, we will use a composite action `action.yaml` and a reusable workflow `.github/workflows/example_workflow.yml` as examples.

    ??? example "compsite action `action.yaml`"

        ```yaml title="action.yaml"
        --8<-- "action.yaml"
        ```

    ??? example "reusable workflow `.github/workflows/example_workflow.yml`"

        ```yaml title=".github/workflows/example_workflow.yml"
        --8<-- ".github/workflows/example_workflow.yml"
        ```

## Installation

This package is extension package to [*mkdocstrings*](https://mkdocstrings.github.io/), a framework for auto-documentation for various languages. Language support is inserted into the framework by providing *handlers*. The *mkdocstrings-github* package provides a GitHub handler.

--8<-- "README.md:install"

The default *mkdocstrings* handler is the [Python handler](https://mkdocstrings.github.io/python). You can change the default hanlder and set the GitHub handler as default be defining the `default_handler` configuration option of `mkdocstrings` in `mkdocs.yml`:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    default_handler: github
```

## Injecting documentation

With the GitHub handler installed and configured as default handler, you can inject documentation for a GitHub action or a reusable workflow in your Markdown pages:

```markdown
::: <path to action or workflow from the git root>
```

If another handler was defined as default handler, you can explicitely ask for the GitHub handler to be used when injecting documentation with the handler option:

```markdown
::: <path to action or workflow from the git root>
    handler: github
```

The path to the action or workflow is consistent with how they are called in GitHub Actions.
For actions, the path should the folder containing the `action.yml` or `action.yaml` file. The filename should not be included. 

=== "`action.yaml` or `action.yml`"

    ```markdown
    ::: .
    ```

=== "`.github/actions/myaction/action.yml`"

    ```markdown
    ::: .github/actions/myaction
    ```

=== "`action/nested/in/directory/action.yaml`"

    ```markdown
    ::: action/nested/in/directory
    ```

For reusable workflows, which are workflows that include the [`workflow_call`](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_call) trigger, the full path should be included. 

=== "`.github/workflows/reusable_workflow.yaml`"

    ```markdown
    ::: .github/workflows/reusable_workflow.yaml
    ```

=== "`.github/workflows/myworkflow.yml`"

    ```markdown
    ::: .github/workflows/myworkflow.yml
    ```

## Linking

For every documented action or workflow, HTML tags are inserted on the page to allow linking with the action/workflow path as the id. Additionally, linking to action and workflow parameters, and cross-linking to other parameters, is possible with the [`parameters_anchors`][mkdocstrings_handlers.github.config.GitHubOptions.parameters_anchors] option.

## Configuration

When installed, the Github handler can be configured in `mkdocs.yml`

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      github:
        ... # The GitHub handler configuration
```

### Global-only options

Some options are **global only**, and go directly under the handler's name.

::: mkdocstrings_handlers.github.config.GitHubConfig.hostname
    handler: python

::: mkdocstrings_handlers.github.config.GitHubConfig.repo
    handler: python

::: mkdocstrings_handlers.github.config.GitHubConfig.feather_icons_source
    handler: python

### Global/local options

The other options can be used both globally *and* locally, under the `options` key. For example, globally:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      github:
        options:
          do_something: true
```

...and locally, overriding the global configuration:

```markdown title="docs/some_page.md"
::: .github/workflows/reusable-workflow.yml
    handler: github
    options:
        do_something: true
```

These options affect how the documentation is collected from sources and rendered. See the following tables summarizing the options, and get more details for each option in the following pages:

- [General options](./general.md): Generic options that does not fit in the below catagories. 
- [Headings options](./headings.md): options related to the headings and the table of contents.
- [Signature options](./signatures.md): options related to the shown call signature.
- [Parameters options](./parameters.md): options related to the input (and output) parameters of the action or workflow.

::: mkdocstrings_handlers.github.config.GitHubOptions
    handler: python
    options:
        show_bases: false
        show_source: false
        show_root_heading: false
        members: false