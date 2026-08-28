# Odoo 19 source verification notes

Verified against local official image `odoo:19.0` reporting `19.0-20260810`.

- `odoo/http.py`: `route()` accepts `type="jsonrpc"`, `methods`, and `readonly`; JSON-RPC route wrappers discard unknown keyword arguments before invoking explicit controller arguments.
- `addons/product/models/product_pricelist.py`: `_get_products_price(self, products, *args, **kwargs)` is the batch API and returns a dictionary keyed by product ID.
- `addons/website/views/snippets/snippets.xml`: snippet group and structure anchors are `<snippets id="snippet_groups">` and `<snippets id="snippet_structure">`, not `div` elements.
- `addons/point_of_sale/views/product_view.xml`: provides the POS product form/list extensions and `pos_categ_ids` anchors used by the inherited views.
- `addons/website/static/src/builder/website_builder.js`: the website plugin registry is `website-plugins`.

The frontend implementation is intentionally outside Checkpoint A and will be re-verified before it is tested.
