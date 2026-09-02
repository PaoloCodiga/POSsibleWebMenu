param([ValidateSet('js-utils', 'js-interaction', 'js-builder-cleanup', 'js-builder-configuration', 'backend', 'checkpoint-b3')] [string] $Command = 'checkpoint-b3')
$ErrorActionPreference = 'Stop'
$Database = 'possible_web_menu_test'
docker compose -f .dev/docker-compose.test.yml up -d db
function Invoke-Hoot([string] $Descriptor) { docker compose -f .dev/docker-compose.test.yml run --rm -e "POSSIBLE_WEB_MENU_HOOT_DESCRIPTOR=$Descriptor" odoo odoo -d $Database --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -i possible_web_menu --test-enable --test-tags /possible_web_menu:TestWebMenuHoot --stop-after-init }
switch ($Command) {
  'js-utils' { Invoke-Hoot '@possible_web_menu/possible_web_menu_utils' }
  'js-interaction' { Invoke-Hoot '@possible_web_menu/possible_web_menu_interaction' }
  'js-builder-cleanup' { Invoke-Hoot '@possible_web_menu/possible_web_menu_builder_cleanup' }
  'js-builder-configuration' { Invoke-Hoot '@possible_web_menu/possible_web_menu_builder_configuration' }
  'backend' { docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d $Database --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -u possible_web_menu --test-enable --test-tags '/possible_web_menu,-/possible_web_menu:TestWebMenuHoot' --stop-after-init }
  'checkpoint-b3' { & $PSCommandPath js-utils; & $PSCommandPath js-interaction; & $PSCommandPath js-builder-cleanup; & $PSCommandPath backend }
}
