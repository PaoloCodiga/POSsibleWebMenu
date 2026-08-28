$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force artifacts | Out-Null
docker compose -f .dev/docker-compose.test.yml up -d --build db
try {
  docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d possible_web_menu_test --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -i possible_web_menu --stop-after-init
  docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d possible_web_menu_test --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons --test-enable --test-tags /possible_web_menu --stop-after-init
} finally { docker compose -f .dev/docker-compose.test.yml down -v }
