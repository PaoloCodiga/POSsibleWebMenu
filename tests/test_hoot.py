import os

from odoo.addons.web.tests.test_js import HOOTCommon, unit_test_error_checker
from odoo.tests import no_retry, tagged


@tagged("post_install", "-at_install", "possible_web_menu")
class TestWebMenuHoot(HOOTCommon):
    """Runs only the addon Hoot modules through Odoo's native filter."""

    HOOT_DESCRIPTORS = (
        "@possible_web_menu/possible_web_menu_utils",
        "@possible_web_menu/possible_web_menu_interaction",
        "@possible_web_menu/possible_web_menu_builder_cleanup",
    )

    @classmethod
    def _get_hoot_descriptors(cls):
        requested = os.environ.get("POSSIBLE_WEB_MENU_HOOT_DESCRIPTOR")
        if not requested:
            return cls.HOOT_DESCRIPTORS
        if requested not in cls.HOOT_DESCRIPTORS:
            raise ValueError("Unsupported possible_web_menu HOOT descriptor.")
        return (requested,)

    def setUp(self):
        super().setUp()
        # Odoo's generic setup initializes _test_params. Set the descriptor
        # afterwards, then regenerate HOOTCommon's native hash filter.
        self._test_params = [("+", descriptor) for descriptor in self._get_hoot_descriptors()]
        self.hoot_filters = self.get_hoot_filters()

    @no_retry
    def test_hoot_modules(self):
        self.assertTrue(self.hoot_filters)
        self.browser_js(
            f"/web/tests?headless&loglevel=2&preset=desktop&timeout=15000{self.hoot_filters}",
            """
                new Promise((resolve, reject) => {
                    const deadline = Date.now() + 30000;
                    const poll = () => {
                        if (globalThis.__possibleWebMenuHootExecuted) {
                            resolve(true);
                        } else if (Date.now() >= deadline) {
                            reject(new Error("The possible_web_menu Hoot suite did not execute"));
                        } else {
                            setTimeout(poll, 50);
                        }
                    };
                    poll();
                })
            """,
            "",
            login="admin",
            timeout=3600,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=unit_test_error_checker,
        )
