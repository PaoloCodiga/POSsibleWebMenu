# Functional specification

POSsible Web Menu provides a draggable Odoo 19 Website snippet that renders
allowed product templates as a public POS menu.

The editor chooses an allowed web-menu pricelist, zero or more POS categories,
child-category inclusion, Sales/POS/Purchase eligibility flags with all/any
matching, descriptions, internal references, uncategorized products, tax
display, ordering, and leaders, clean, or two-column layout.

An empty category selection means all categories. A product must be explicitly
marked **Visible in Web Menu**. When a product belongs to multiple eligible POS
categories, its Primary Web Menu Category is used; otherwise the first category
in deterministic POS sequence/name/id order is used. Products outside the
website company are excluded.

Apply writes the complete canonical configuration atomically to the selected
snippet. It refreshes only that snippet, creates one history operation, and is
reversible through normal Website Builder Undo/Redo. Saving removes generated
runtime HTML only; reopening the public page performs a fresh render.
