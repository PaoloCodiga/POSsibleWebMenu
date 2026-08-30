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

The frontend implementation is intentionally outside Checkpoint A and will be re-verified before it is tested.
