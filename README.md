# POSsible Web Menu

The module renders an allowlisted POS menu configuration on a public website through a readonly JSON-RPC route and server-side QWeb.

Generated menu output is runtime-only. Odoo 19 saves a detached clone, and the Website Builder plugin removes the generated boundary before serialization while retaining headings, subtitles, and canonical `data-*` configuration.

Use `scripts/test.sh js-utils`, `scripts/test.sh js-interaction`, and `scripts/test.sh js-builder-cleanup` for isolated browser checks. Checkpoint C's configuration UI is still pending.
