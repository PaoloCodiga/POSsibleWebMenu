# Checkpoint B execution plan

## B1 — QWeb renderer, public route, snippet XML and CSS

- Deliverables: verified renderer, safe JSON-RPC route, QWeb fragment, preconfigured snippet shell and responsive CSS.
- Tests: renderer/unit tests, route tests, XML validation, clean install.
- Completion: public server can render a preconfigured snippet without persisted generated content.
- Commit status: in progress.

## B2 — Public Interaction and Hoot tests

- Deliverables: Odoo 19 Interaction, dataset utilities, RPC refresh and Hoot tests.
- Tests: Hoot utility/Interaction cases.
- Completion: independent snippet instances refresh correctly.
- Commit status: pending.

## B3 — Builder-safe runtime and persistence boundary

- Runtime QWeb output is wrapped in `.o_possible_web_menu_generated`.
- The Odoo 19 Website Builder plugin cleans this runtime boundary only from the detached save clone.
- Canonical `data-*` configuration, headings, subtitles, static content container, and authored content remain intact.
- Isolated HOOT descriptors: `@possible_web_menu/possible_web_menu_utils`, `@possible_web_menu/possible_web_menu_interaction`, and `@possible_web_menu/possible_web_menu_builder_cleanup`.
- A real Chrome Website Builder tour saves a configured fixture page, verifies the persisted architecture contains no generated runtime markup, and verifies a public reload renders the menu again.
- Checkpoint C remains responsible for the configuration dialog and Builder actions.

## C — Website Builder configuration dialog

- Deliverables: editor option, dialog, history operation and clone behavior.
- Tests: unit and builder tour coverage.
- Completion: configuration is undoable and each snippet remains independent.
- Commit status: pending.
