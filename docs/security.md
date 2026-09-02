# Security

The public route accepts only normalized, allowlisted configuration. It has no
caller-provided ORM domain, model, field, company, website, or ordering input.
It validates the selected pricelist as active, web-menu enabled, and global or
compatible with the active website company. Product queries explicitly restrict
results to global products or the active website company.

`sudo()` is limited to public read paths after those server-side restrictions;
it never returns arbitrary records or exposes pricing through a probeable
pricelist ID. The Builder options route requires Website Designer access before
using elevated read access.

The sole production `innerHTML` assignment is the documented trusted-QWeb
generated-content boundary. Product names, categories, descriptions, and
references are escaped by QWeb; descriptions are normalized to plain text.
Editor feedback is static translated markup and backend exception details are
not exposed. Cleanup targets only named runtime descendants in a detached clone
and cannot remove unrelated authored content.
