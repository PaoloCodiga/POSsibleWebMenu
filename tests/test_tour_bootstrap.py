import logging

from odoo import SUPERUSER_ID, api
from odoo.tests import HttpCase, tagged


_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install", "possible_web_menu", "possible_web_menu_tour_bootstrap")
@tagged("post_install", "-at_install", "possible_web_menu", "possible_web_menu_browser_js")
class TestPossibleWebMenuBrowserBootstrap(HttpCase):
    def test_public_browser_js_bootstrap(self):
        self.browser_js(
            "/",
            """
            if (!document.body) { throw new Error('Public Website body is missing'); }
            if (!document.querySelector('html[data-website-id]')) {
                throw new Error('Website frontend did not initialize');
            }
            if (window.odoo && window.odoo.__module_loader && window.odoo.__module_loader.failed) {
                throw new Error('Fatal module-loader error');
            }
            console.log('test successful');
            """,
            timeout=60,
        )

    def test_public_menu_browser_js(self):
        with self.registry.cursor() as cursor:
            environment = api.Environment(cursor, SUPERUSER_ID, {})
            website = environment['website'].get_current_website()
            category = environment['pos.category'].create({'name': 'B3 Test Category'})
            product = environment['product.template'].create({
                'name': 'B3 Visible Product', 'list_price': 12.5,
                'available_in_pos': True, 'sale_ok': True, 'web_menu_visible': True,
                'company_id': website.company_id.id,
                'pos_categ_ids': [(6, 0, [category.id])],
            })
            pricelist = environment['product.pricelist'].create({
                'name': 'B3 Test Web Menu Pricelist',
                'active': True,
                'web_menu_available': True,
                'company_id': website.company_id.id,
            })
            renderer = environment['possible.web.menu.renderer']
            configuration = renderer._normalize_config({
                'pricelist_id': pricelist.id,
                'pos_category_ids': [category.id],
                'include_child_categories': True,
                'filter_sale': True,
                'filter_pos': True,
                'filter_purchase': False,
                'filter_mode': 'all',
                'show_description': False,
                'show_internal_reference': False,
                'show_uncategorized': False,
                'tax_display': 'included',
                'sort_mode': 'favorite_ref_name',
                'layout': 'leaders',
            })
            try:
                self.assertTrue(pricelist.exists())
                self.assertTrue(pricelist.active)
                self.assertTrue(pricelist.web_menu_available)
                self.assertIn(pricelist.company_id, (False, website.company_id))
                self.assertTrue(product.exists())
                self.assertTrue(product.web_menu_visible)
                self.assertTrue(product.sale_ok)
                self.assertTrue(product.available_in_pos)
                self.assertIn(category, product.pos_categ_ids)

                allowed_pricelist = renderer._get_allowed_pricelist(configuration, website)
                renderer_result = renderer._render_menu(configuration, website)
                rendered_html = str(renderer_result['html'])
                self.assertEqual(allowed_pricelist, pricelist)
                self.assertGreater(renderer_result['product_count'], 0)
                self.assertIn('B3 Visible Product', rendered_html)
                self.assertIn('B3 Test Category', rendered_html)
                self.assertIn('o_possible_web_menu', rendered_html)
                self.assertTrue(rendered_html.strip())
            except AssertionError:
                _logger.exception('Backend renderer precheck: FAIL')
                raise
            _logger.info('Backend renderer precheck: PASS')
            _logger.info('Product count: %s', renderer_result['product_count'])
            _logger.info('Expected product present: yes')
            view = environment['ir.ui.view'].create({
                'name': 'B3 public menu page', 'type': 'qweb', 'key': 'possible_web_menu.b3_public_page',
                'arch': f'<t t-name="possible_web_menu.b3_public_page"><t t-call="website.layout"><div id="wrap"><section class="s_possible_web_menu" data-snippet="s_possible_web_menu" data-config-version="1" data-pricelist-id="{pricelist.id}" data-pos-category-ids="{category.id}" data-include-child-categories="true" data-filter-sale="true" data-filter-pos="true" data-filter-purchase="false" data-filter-mode="all" data-show-description="false" data-show-internal-reference="false" data-show-uncategorized="false" data-tax-display="included" data-sort-mode="favorite_ref_name" data-layout="leaders"><div class="container"><h2>Menu</h2><p>Discover</p><div class="s_possible_web_menu_content"/></div></section></div></t></t>',
            })
            page = environment['website.page'].create({
                'url': '/b3-public-menu', 'view_id': view.id, 'website_id': website.id,
                'is_published': True,
            })
            cursor.commit()
            fixture_ids = {
                'category': category.id,
                'product': product.id,
                'pricelist': pricelist.id,
                'view': view.id,
                'page': page.id,
            }
        try:
            _logger.info("[6/9] Browser_js test invocation")
            self.browser_js('/b3-public-menu', """
            new Promise((resolve, reject) => {
                const snippet = document.querySelector('.s_possible_web_menu');
                const configuredPricelistId = Number.parseInt(snippet?.dataset.pricelistId, 10);
                console.log('B3.2B static snippet diagnostics', JSON.stringify({
                    snippetExists: Boolean(snippet),
                    generatedExists: Boolean(snippet?.querySelector('.o_possible_web_menu_generated')),
                    pricelistId: snippet?.dataset.pricelistId,
                    posCategoryIds: snippet?.dataset.posCategoryIds,
                    includeChildCategories: snippet?.dataset.includeChildCategories,
                    filterSale: snippet?.dataset.filterSale,
                    filterPos: snippet?.dataset.filterPos,
                    filterPurchase: snippet?.dataset.filterPurchase,
                    filterMode: snippet?.dataset.filterMode,
                    taxDisplay: snippet?.dataset.taxDisplay,
                    sortMode: snippet?.dataset.sortMode,
                    layout: snippet?.dataset.layout,
                }));
                if (!snippet) throw new Error('snippet missing');
                if (!Number.isInteger(configuredPricelistId) || configuredPricelistId <= 0 || configuredPricelistId !== __FIXTURE_PRICELIST_ID__) {
                    throw new Error('snippet pricelist configuration does not match the fixture');
                }
                const interactionModuleName = '@possible_web_menu/snippets/s_possible_web_menu/possible_web_menu';
                const utilsModuleName = '@possible_web_menu/snippets/s_possible_web_menu/possible_web_menu_utils';
                const reportBootstrap = async (stage) => {
                    const loader = window.odoo?.loader;
                    const frontendAssetUrl = performance.getEntriesByType('resource')
                        .map((entry) => entry.name)
                        .find((url) => url.includes('web.assets_frontend_lazy'));
                    const frontendAsset = frontendAssetUrl ? await fetch(frontendAssetUrl).then((response) => response.text()) : '';
                    const registry = loader?.modules.get('@web/core/registry')?.registry;
                    const interactionClass = registry?.category('public.interactions').get('possible_web_menu');
                    const interactionService = window.odoo?.__WOWL_DEBUG__?.root?.env?.services?.['public.interactions'];
                    const instance = interactionClass && interactionService?.interactions.find((colibri) => colibri.el === snippet && colibri.interaction instanceof interactionClass);
                    const interaction = instance?.interaction;
                    console.log('B3.2C frontend bootstrap diagnostics', JSON.stringify({
                        stage,
                        possibleWebMenuUtilsInProductionFrontendAsset: frontendAsset.includes(utilsModuleName),
                        possibleWebMenuInteractionInProductionFrontendAsset: frontendAsset.includes(interactionModuleName),
                        interactionModuleFactoryPresent: Boolean(loader?.factories.has(interactionModuleName)),
                        interactionModuleExecuted: Boolean(loader?.modules.has(interactionModuleName)),
                        publicInteractionsRegistryEntryPresent: Boolean(interactionClass),
                        publicInteractionServiceActive: Boolean(interactionService?.isActive),
                        publicInteractionServiceProcessesEntry: Boolean(interactionService?.Interactions.includes(interactionClass)),
                        selectorMatchesSnippet: Boolean(interactionClass && snippet.matches(interactionClass.selector)),
                        interactionInstanceStartedForSnippet: Boolean(instance),
                        interactionGeneration: interaction?.generation,
                        interactionReady: instance?.isReady,
                        contentAriaBusy: snippet.querySelector('.s_possible_web_menu_content')?.getAttribute('aria-busy'),
                        rpcServiceType: typeof interaction?.services.rpc,
                    }));
                };
                window.setTimeout(() => reportBootstrap('after-public-assets-load'), 1000);
                console.log('[8/9] Browser-side asynchronous render wait');
                const deadline = Date.now() + 55000;
                const waitForRender = () => {
                    const content = snippet.querySelector('.o_possible_web_menu_generated');
                    const ready = content && snippet.querySelector('.s_possible_web_menu_content').getAttribute('aria-busy') !== 'true';
                    if (ready) {
                        if (!content.querySelector('.o_possible_web_menu_product_name')) {
                            reject(new Error('generated product markup missing'));
                            return;
                        }
                        if (!content.textContent.includes('B3 Visible Product')) {
                            reject(new Error('fixture product was not rendered'));
                            return;
                        }
                        console.log('test successful');
                        resolve();
                        return;
                    }
                    if (Date.now() >= deadline) {
                        reportBootstrap('render-wait-timeout').finally(() => reject(new Error('menu render did not finish within 55 seconds')));
                        return;
                    }
                    window.setTimeout(waitForRender, 100);
                };
                waitForRender();
            })
            """.replace('__FIXTURE_PRICELIST_ID__', str(pricelist.id)), timeout=60)
        finally:
            with self.registry.cursor() as cursor:
                environment = api.Environment(cursor, SUPERUSER_ID, {})
                environment['website.page'].browse(fixture_ids['page']).unlink()
                environment['ir.ui.view'].browse(fixture_ids['view']).unlink()
                environment['product.pricelist'].browse(fixture_ids['pricelist']).unlink()
                environment['product.template'].browse(fixture_ids['product']).unlink()
                environment['pos.category'].browse(fixture_ids['category']).unlink()
                cursor.commit()
            _logger.info("[9/9] Test completion and process exit")


@tagged("post_install", "-at_install", "possible_web_menu", "possible_web_menu_builder_persistence")
class TestPossibleWebMenuBuilderPersistence(HttpCase):
    def test_builder_save_strips_runtime_menu_and_public_reload_renders_it(self):
        with self.registry.cursor() as cursor:
            environment = api.Environment(cursor, SUPERUSER_ID, {})
            website = environment["website"].get_current_website()
            category = environment["pos.category"].create({"name": "B3 Builder Category"})
            product = environment["product.template"].create({
                "name": "B3 Builder Visible Product",
                "list_price": 14.5,
                "available_in_pos": True,
                "sale_ok": True,
                "web_menu_visible": True,
                "company_id": website.company_id.id,
                "pos_categ_ids": [(6, 0, [category.id])],
            })
            pricelist = environment["product.pricelist"].create({
                "name": "B3 Builder Web Menu Pricelist",
                "active": True,
                "web_menu_available": True,
                "company_id": website.company_id.id,
            })
            view = environment["ir.ui.view"].create({
                "name": "B3 builder persistence page",
                "type": "qweb",
                "key": "possible_web_menu.b3_builder_persistence_page",
                "arch": f'''<t t-name="possible_web_menu.b3_builder_persistence_page"><t t-call="website.layout"><div id="wrap"><section class="s_possible_web_menu" data-snippet="s_possible_web_menu" data-config-version="1" data-pricelist-id="{pricelist.id}" data-pos-category-ids="{category.id}" data-include-child-categories="true" data-filter-sale="true" data-filter-pos="true" data-filter-purchase="false" data-filter-mode="all" data-show-description="false" data-show-internal-reference="false" data-show-uncategorized="false" data-tax-display="included" data-sort-mode="favorite_ref_name" data-layout="leaders"><div class="container"><h2 class="s_possible_web_menu_title">B3 Builder Menu</h2><p>Builder persistence fixture</p><div class="s_possible_web_menu_content" aria-busy="false"/></div></section></div></t></t>''',
            })
            page = environment["website.page"].create({
                "url": "/b3-builder-persistence",
                "view_id": view.id,
                "website_id": website.id,
                "is_published": True,
            })
            cursor.commit()
            fixture_ids = {
                "category": category.id,
                "product": product.id,
                "pricelist": pricelist.id,
                "view": view.id,
                "page": page.id,
            }
        try:
            self.browser_js(
                "/b3-builder-persistence",
                """
                new Promise((resolve, reject) => {
                    const deadline = Date.now() + 30000;
                    const waitForPreview = () => {
                        const generated = document.querySelector('.o_possible_web_menu_generated');
                        if (generated?.textContent.includes('B3 Builder Visible Product')) {
                            console.log('test successful');
                            resolve();
                            return;
                        }
                        if (Date.now() >= deadline) {
                            reject(new Error('public dynamic preview did not render before Builder save'));
                            return;
                        }
                        setTimeout(waitForPreview, 100);
                    };
                    waitForPreview();
                })
                """,
                timeout=35,
            )
            self.start_tour(
                self.env["website"].get_client_action_url("/b3-builder-persistence"),
                "possible_web_menu_builder_persistence",
                login="admin",
            )
            with self.registry.cursor() as cursor:
                environment = api.Environment(cursor, SUPERUSER_ID, {})
                persisted_architecture = environment["ir.ui.view"].browse(fixture_ids["view"]).arch_db
                self.assertIn("B3 Builder Menu Saved", persisted_architecture)
                self.assertIn(f'data-pricelist-id="{fixture_ids["pricelist"]}"', persisted_architecture)
                self.assertIn(f'data-pos-category-ids="{fixture_ids["category"]}"', persisted_architecture)
                self.assertNotIn("o_possible_web_menu_generated", persisted_architecture)
                self.assertNotIn("B3 Builder Visible Product", persisted_architecture)
                self.assertNotIn("o_possible_web_menu_runtime_message", persisted_architecture)
            self.browser_js(
                "/b3-builder-persistence",
                """
                new Promise((resolve, reject) => {
                    const deadline = Date.now() + 30000;
                    const waitForReload = () => {
                        const generated = document.querySelector('.o_possible_web_menu_generated');
                        if (generated?.textContent.includes('B3 Builder Visible Product')) {
                            console.log('test successful');
                            resolve();
                            return;
                        }
                        if (Date.now() >= deadline) {
                            reject(new Error('public menu did not render after Builder save and reload'));
                            return;
                        }
                        setTimeout(waitForReload, 100);
                    };
                    waitForReload();
                })
                """,
                timeout=35,
            )
        finally:
            with self.registry.cursor() as cursor:
                environment = api.Environment(cursor, SUPERUSER_ID, {})
                environment["website.page"].browse(fixture_ids["page"]).unlink()
                environment["ir.ui.view"].browse(fixture_ids["view"]).unlink()
                environment["product.pricelist"].browse(fixture_ids["pricelist"]).unlink()
                environment["product.template"].browse(fixture_ids["product"]).unlink()
                environment["pos.category"].browse(fixture_ids["category"]).unlink()
                cursor.commit()
