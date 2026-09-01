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
