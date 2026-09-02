# Architecture

The public Interaction normalizes canonical snippet data and calls the readonly
JSON-RPC renderer. The renderer allows only known filters, layouts, sort modes,
and a website-compatible pricelist; it queries product templates and renders a
trusted server-side QWeb fragment. That fragment is inserted exclusively inside
`.o_possible_web_menu_generated`.

The Builder option loads allowed pricelists and POS categories through its
authenticated route. Apply is one `BuilderAction`, which updates the complete
canonical dataset then dispatches `update_interactions`. The menu Interaction
is registered in public, edit, and preview registries, so each snippet refreshes
independently in its active context.

The Website Builder plugin removes runtime-only output and state from Odoo 19's
detached save clone. Saved markup retains structural snippets, headings,
subtitles, static container, and canonical configuration only. A duplicated
snippet retains configuration but starts an independent Interaction and fresh
render.
