$ErrorActionPreference = 'Stop'
docker compose -f .dev/docker-compose.test.yml build odoo
docker compose -f .dev/docker-compose.test.yml up -d db
docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d possible_web_menu_hoot --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons --test-enable --test-tags /possible_web_menu:TestWebMenuHoot --stop-after-init
