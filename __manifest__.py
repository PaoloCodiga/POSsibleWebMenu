{
    "name": "POSsible Web Menu",
    "version": "19.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "author": "POSsible",
    "depends": ["website", "point_of_sale"],
    "data": [
        "views/product_template_views.xml",
        "views/product_pricelist_views.xml",
        "data/product_template_actions.xml",
        "views/snippets/snippets.xml",
        "views/snippets/s_possible_web_menu.xml",
        "views/snippets/web_menu_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "possible_web_menu/static/src/snippets/s_possible_web_menu/000.scss",
            "possible_web_menu/static/src/snippets/s_possible_web_menu/possible_web_menu_utils.js",
            "possible_web_menu/static/src/snippets/s_possible_web_menu/possible_web_menu.js",
        ],
        "website.website_builder_assets": [
            "possible_web_menu/static/src/website_builder/possible_web_menu_option.xml",
            "possible_web_menu/static/src/website_builder/possible_web_menu_option_plugin.js",
        ],
        "web.assets_unit_tests": [
            "possible_web_menu/static/src/snippets/s_possible_web_menu/possible_web_menu_utils.js",
            "possible_web_menu/static/src/snippets/s_possible_web_menu/possible_web_menu.js",
            "possible_web_menu/static/tests/possible_web_menu_utils.test.js",
            "possible_web_menu/static/tests/possible_web_menu_interaction.test.js",
        ],
    },
    "application": False,
    "installable": True,
}
