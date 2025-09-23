from inline_snapshot import external, register_format_alias, snapshot

register_format_alias(".html", ".txt")


action_show = snapshot(
    {
        (("description", ""), ("show_description", True), ("show_source", True)): external(
            "hash:9aa8eb734c7c*.html"
        ),
        (
            ("description", "Custom heading"),
            ("show_description", True),
            ("show_source", True),
        ): external("hash:ef78405111c9*.html"),
        (("description", ""), ("show_description", False), ("show_source", False)): external(
            "hash:5a2f11e94bc0*.html"
        ),
        (
            ("heading", ""),
            ("heading_level", 1),
            ("show_action_branding", False),
            ("show_action_branding_toc", False),
            ("show_heading", True),
            ("show_toc_entry", False),
            ("toc_label", ""),
        ): external("hash:6e9183554e68*.html"),
        (
            ("heading", "Custom heading"),
            ("heading_level", 2),
            ("show_action_branding", False),
            ("show_action_branding_toc", False),
            ("show_heading", True),
            ("show_toc_entry", False),
            ("toc_label", "Custom toc label"),
        ): external("hash:95fa34cbe058*.html"),
        (
            ("heading", ""),
            ("heading_level", 3),
            ("show_action_branding", True),
            ("show_action_branding_toc", True),
            ("show_heading", True),
            ("show_toc_entry", False),
            ("toc_label", ""),
        ): external("hash:a4c607c86340*.html"),
        (
            ("heading", ""),
            ("heading_level", 1),
            ("show_action_branding", False),
            ("show_action_branding_toc", False),
            ("show_heading", False),
            ("show_toc_entry", True),
            ("toc_label", ""),
        ): external("hash:b75ea44c27bf*.html"),
        (
            ("heading", ""),
            ("heading_level", 1),
            ("show_action_branding", False),
            ("show_action_branding_toc", False),
            ("show_heading", False),
            ("show_toc_entry", False),
            ("toc_label", ""),
        ): external("hash:a2f1180444cf*.html"),
        (
            ("show_signature", True),
            ("signature_version", "major"),
            ("signature_version_string", ""),
        ): external("hash:812324905baf*.html"),
        (
            ("show_signature", True),
            ("signature_version", "semver"),
            ("signature_version_string", ""),
        ): external("hash:82112e80241a*.html"),
        (
            ("show_signature", True),
            ("signature_version", "string"),
            ("signature_version_string", "latest"),
        ): external("hash:fa52cc987e9e*.html"),
        (
            ("show_signature", False),
            ("signature_version", "string"),
            ("signature_version_string", ""),
        ): external("hash:d0a05ae0b002*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "table"),
            ("show_inputs", True),
            ("show_inputs_only_required", False),
            ("show_outputs", True),
        ): external("hash:2ea2d3056980*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "table"),
            ("show_inputs", True),
            ("show_inputs_only_required", True),
            ("show_outputs", False),
        ): external("hash:724ef1bf689b*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "table"),
            ("show_inputs", False),
            ("show_inputs_only_required", False),
            ("show_outputs", False),
        ): external("hash:a26842d079de*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "table"),
            ("show_inputs", True),
            ("show_inputs_only_required", False),
            ("show_outputs", True),
        ): external("hash:c7185d5dd0e1*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "table"),
            ("show_inputs", True),
            ("show_inputs_only_required", True),
            ("show_outputs", False),
        ): external("hash:4da21c2add49*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "table"),
            ("show_inputs", False),
            ("show_inputs_only_required", False),
            ("show_outputs", False),
        ): external("hash:28b7cbe1f4d8*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "list"),
            ("show_inputs", True),
            ("show_inputs_only_required", False),
            ("show_outputs", True),
        ): external("hash:399e8f33e560*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "list"),
            ("show_inputs", True),
            ("show_inputs_only_required", True),
            ("show_outputs", False),
        ): external("hash:399a99a5d4c2*.html"),
        (
            ("parameters_order", "alphabetical"),
            ("parameters_section_style", "list"),
            ("show_inputs", False),
            ("show_inputs_only_required", False),
            ("show_outputs", False),
        ): external("hash:c8452e9efbb4*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "list"),
            ("show_inputs", True),
            ("show_inputs_only_required", False),
            ("show_outputs", True),
        ): external("hash:77bb9791c45f*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "list"),
            ("show_inputs", True),
            ("show_inputs_only_required", True),
            ("show_outputs", False),
        ): external("hash:83b9ea7ef21f*.html"),
        (
            ("parameters_order", "source"),
            ("parameters_section_style", "list"),
            ("show_inputs", False),
            ("show_inputs_only_required", False),
            ("show_outputs", False),
        ): external("hash:00970758cb92*.html"),
    }
)
