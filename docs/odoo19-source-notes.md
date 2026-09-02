# Odoo 19 source verification notes

Verified against local official image `odoo:19.0` reporting `19.0-20260810`.

- `odoo/http.py`: `route()` accepts `type="jsonrpc"`, `methods`, and `readonly`; JSON-RPC route wrappers discard unknown keyword arguments before invoking explicit controller arguments.
- `addons/product/models/product_pricelist.py`: `_get_products_price(self, products, *args, **kwargs)` is the batch API and returns a dictionary keyed by product ID.
- `addons/website/views/snippets/snippets.xml`: snippet group and structure anchors are `<snippets id="snippet_groups">` and `<snippets id="snippet_structure">`, not `div` elements.
- `addons/point_of_sale/views/product_view.xml`: provides the POS product form/list extensions and `pos_categ_ids` anchors used by the inherited views.
- `addons/website/static/src/builder/website_builder.js`: the website plugin registry is `website-plugins`.
- `addons/website/models/ir_ui_view.py`: `ir.ui.view._render_template(template, values=None)` is the supported website QWeb rendering API.
- `addons/account/models/account_tax.py`: `account.tax.compute_all(price_unit, currency=None, quantity=1.0, product=None, partner=None, ...)` handles included and excluded taxes.
- `addons/web/static/src/public/interaction.js`: public interactions use `setup`, `willStart`, `start`, and `destroy`; asynchronous initial work belongs in `willStart`.
- `addons/web/tests/test_js.py`: `HOOTCommon.get_hoot_filters()` converts `_test_params` descriptors to `id=<hash>` parameters. B2.1 filters the Hoot suite descriptor `@possible_web_menu/possible_web_menu_utils` through this inherited helper.

## B3 Website Builder lifecycle

- `html_editor/static/src/editor.js` builds a detached clone in `getElContent()` and invokes `clean_for_save_handlers` with that clone as `root`.
- `website/static/src/builder/plugins/edit_interaction_plugin.js` stops interactions before cloning and restarts the original afterwards. `on_cloned_handlers` receives `cloneEl`; newly inserted clones start their own interactions.
- Website edit mode uses `.o_editable` and `body.editor_enable`. The Interaction uses those markers only for editor feedback.
- Browser tours use `registry.category("web_tour.tours")`; Website Builder patterns use `registerWebsitePreviewTour` and `:iframe` selectors from `@website/js/tours/tour_utils`.
- The B3 persistence test creates an isolated `website.page` fixture with a
  real positive pricelist and product. It proves public rendering before edit,
  uses the native Builder save action, asserts the persisted architecture has
  no generated runtime markup, and proves the public reload renders again.

## C1 Website Builder configuration UI

- `html_builder/static/src/core/utils.js`: `BaseOptionComponent` receives the
  Builder environment, including `getEditingElement()` for the selected
  snippet. A snippet option declares `static template` and `static selector`.
  The active element can be a descendant, so snippet-level `data-*` reads use
  `getEditingElement().closest(selector)`.
- `website/static/src/builder/plugins/options/countdown_option_plugin.js`:
  Website Builder options are registered through a `Plugin` in
  `registry.category("website-plugins")`, with the option supplied through the
  `builder_options` resource and a sequence from
  `@html_builder/utils/option_sequence`.
- `html_builder/static/src/core/builder_action.js`: `BuilderAction` is the
  API that applies editor mutations and participates in Builder history. C1
  deliberately does not register or invoke an action, so the dialog cannot
  mutate the snippet before C2 adds the proper history operation.
- `website/static/src/builder/plugins/options/embed_code_option_plugin.js` and
  `embed_code_option_dialog.{js,xml}`: a Builder action or option opens a
  custom OWL component with `this.services.dialog.add(Component, props)`; the
  dialog extends `Component`, includes `Dialog`, and receives `close` in props.
- `website/static/src/builder/plugins/font/add_font_dialog.js`: OWL dialogs use
  `useState`, `onWillStart`, `useService`, and the supported
  `rpc` import from `@web/core/network/rpc` for asynchronous loading and error
  state. This is the pattern used by C1.
- `website/static/src/builder/website_builder.js`: the active Website Builder
  gathers classes from `registry.category("website-plugins")` into its editor
  context. The dialog has access only to the selected element configuration
  passed by the option component; it does not retain an editor DOM reference.
- The C1 options route returns only allowed active web-menu pricelists
  (identifier, name, currency) and POS categories (identifier, name, parent,
  sequence, depth). The dialog uses native checkbox multi-selection, a local
  case-insensitive category search, and depth indentation for the hierarchy.

## C2 atomic apply and Builder history

- `html_builder/static/src/core/builder_action.js`: a `BuilderAction` receives
  the editor context and implements `apply({ editingElement, value })`. The
  action is the supported place for a related DOM mutation; it may dispatch
  `update_interactions` after the mutation to refresh public interactions.
- `html_builder/static/src/core/builder_actions_plugin.js`: Builder actions are
  registered through the plugin `builder_actions` resource. Calling
  `editor.shared.builderActions.applyAction(actionId, spec)` executes the
  action through the operation mutex and calls `history.addStep()` once after
  the action completes. Therefore all synchronous changes inside one action
  are a single undo/redo entry.
- `html_builder/static/src/core/operation_plugin.js`: `operation.next()`
  serializes Builder operations. It is used internally by `applyAction()` and
  should not be replaced with a custom undo stack.
- `html_builder/static/src/builder.js`: the Website Builder’s Undo and Redo
  controls invoke `editor.shared.history.undo()` and `.redo()` through the
  same operation mutex. Attribute mutation records produced by one C2 action
  are restored together while the selected snippet remains connected.
- `website/static/src/builder/plugins/options/countdown_option_plugin.js`:
  standard options use `BuilderAction` and `dispatchTo("update_interactions",
  editingElement)` when an option needs its public interaction restarted.

## C3 Builder insertion and edit lifecycle

- `website/static/src/js/tours/tour_utils.js`: `insertSnippet()` is the
  supported Website Builder tour helper. For a custom snippet group it opens
  the group and inserts the selected snippet through the native add dialog.
- `website/static/src/core/website_edit_service.js`: refreshing interactions
  in edit mode stops affected public instances, then activates entries from
  `public.interactions.edit`. A dynamic public interaction that must refresh
  after Builder configuration changes therefore needs an edit registry entry.
- `website_sale/static/src/snippets/s_dynamic_snippet_products/dynamic_snippet_products.js`:
  dynamic snippets register the same interaction in `public.interactions`,
  `public.interactions.edit`, and `public.interactions.preview`. The POS Web
  Menu follows that Odoo 19 pattern so newly inserted snippets render after
  Builder Apply as well as after a public-page reload.
