#!/usr/bin/env sh
set -eu
mkdir -p artifacts
docker compose -f .dev/docker-compose.test.yml up -d db
trap 'docker compose -f .dev/docker-compose.test.yml down -v' EXIT
docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d possible_web_menu_test --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -i possible_web_menu --stop-after-init
docker compose -f .dev/docker-compose.test.yml run --rm odoo odoo -d possible_web_menu_test --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons --test-enable --test-tags /possible_web_menu --stop-after-init
