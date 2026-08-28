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

## B3 — Clean-before-save behavior and public browser tour

- Deliverables: save cleanup and public website tour.
- Tests: page architecture assertion and browser tour.
- Completion: generated HTML never persists.
- Commit status: pending.

## C — Website Builder configuration dialog

- Deliverables: editor option, dialog, history operation and clone behavior.
- Tests: unit and builder tour coverage.
- Completion: configuration is undoable and each snippet remains independent.
- Commit status: pending.
