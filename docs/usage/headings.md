# Headings options

??? info "Example action/workflow"

    ??? preview "compsite action `action.yaml`"

        ```yaml title="action.yaml"
        --8<-- "action.yaml"
        ```

    ??? preview "reusable workflow `.github/workflows/example_workflow.yml`"

        ```yaml title=".github/workflows/example_workflow.yml"
        --8<-- ".github/workflows/example_workflow.yml"
        ```


::: mkdocstrings_handlers.github.config.GitHubOptions.show_heading
    handler: python

??? preview

    === "`show_heading: true`"

        ::: .
            options:
                show_heading: true

    === "`show_heading: false`"
        
        ::: .
            options:
                show_heading: false

::: mkdocstrings_handlers.github.config.GitHubOptions.heading
    handler: python

??? preview

    === "`heading: ''`"

        ::: .

    === "`heading: 'A custom heading'`"
        
        ::: .
            options:
               heading: 'A custom heading'

::: mkdocstrings_handlers.github.config.GitHubOptions.heading_level
    handler: python

??? preview

    === "`heading_level: 3`"

        ::: .

    === "`heading_level: 5`"
        
        ::: .
            options:
               heading_level: 5

::: mkdocstrings_handlers.github.config.GitHubOptions.show_branding
    handler: python

??? preview

    === "`show_branding: true`"

        ::: .
            options:
                show_branding: true

    === "`show_branding: false`"
        
        ::: .
            options:
                show_branding: false

::: mkdocstrings_handlers.github.config.GitHubOptions.branding_icon
    handler: python

??? preview

    === "`branding_icon: ''`"

        ::: .

    === "`branding_icon: 'briefcase'`"
        
        ::: .
            options:
                branding_icon: 'briefcase'

::: mkdocstrings_handlers.github.config.GitHubOptions.branding_icon_color
    handler: python

??? preview

    === "`branding_icon_color: ''`"

        ::: .

    === "`branding_icon_color: 'green'`"
        
        ::: .
            options:
                branding_icon_color: 'green'

::: mkdocstrings_handlers.github.config.GitHubOptions.show_toc_entry
    handler: python

??? preview

    === "`show_toc_entry: true`"

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [`Example object`](#permalink-to-object){ title="#permalink-to-object" }   
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" } 

    === "`show_toc_entry: false`"

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" }


::: mkdocstrings_handlers.github.config.GitHubOptions.toc_label
    handler: python

??? preview

    === "`toc_label: ''`"

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [`Example object`](#permalink-to-object){ title="#permalink-to-object" }   
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" } 

    === "`toc_label: 'Custom label'`"

        **Table of contents**  
        [Some heading](#permalink-to-some-heading){ title="#permalink-to-some-heading" }  
        [`Custom label`](#permalink-to-object){ title="#permalink-to-object" }   
        [Other heading](#permalink-to-other-heading){ title="#permalink-to-other-heading" }