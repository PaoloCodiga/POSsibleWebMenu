# POSsible Web Menu rules

- Target Odoo release: 19.0 Community; technical addon: `possible_web_menu`.
- Keep all comments and docstrings in English. Never modify Odoo core.
- Do not depend on `website_sale` or use legacy frontend APIs.
- Browser requests never provide arbitrary domains, models, orders, companies, or websites.
- Run static checks and the Docker test commands before declaring completion.
- Layout: Python in `models`/`controllers`, XML in `views`, browser code in `static`, tests in `tests` and `static/tests`, Docker support in `.dev`.
