# POSsible Web Menu

POSsible Web Menu 19.0.1.0.0 adds a configurable POS product menu to Odoo 19
Website pages. It renders current product and pricelist data on demand; menu
output is never saved in the Website page architecture.

## Administrator and editor flow

1. Install `possible_web_menu`.
2. Enable **Visible in Web Menu** on each product template that may appear.
3. Assign POS categories and, when a product has more than one, choose its
   **Primary Web Menu Category**.
4. Enable **Available in Web Menu** on the pricelist that website editors may
   use.
5. Open Website Builder.
6. Drag **POS Web Menu** from the POSsible block group onto a page.
7. Select the snippet and click **Configure menu**.
8. Select a pricelist, categories, filters, display options, ordering, and a
   layout.
9. Click **Apply configuration** and use the normal Builder Undo/Redo controls
   if required.
10. Save the Website page.

The public page retrieves fresh, allowed data at render time. Builder save
retains only authored content and canonical `data-*` configuration.

## V1 limitations

- One menu row is rendered per `product.template`; variants do not create
  separate rows.
- Product images and cart/order workflows are intentionally out of scope.
- The module has no `website_sale` dependency.
- There is no fiscal-position selector.
- Configuration remains in the Website snippet architecture; there is no
  persistent reusable snippet-configuration model.

## Validation

Run the project checks from the module directory:

```sh
scripts/test.sh checkpoint-b3
scripts/hoot.sh
scripts/static-checks.sh
```

The release workflow is additionally covered by a real Chrome Website Builder
tour: insert, configure, apply, undo, redo, save, and public reload.
