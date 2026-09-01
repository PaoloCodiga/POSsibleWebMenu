#!/usr/bin/env sh
set -eu
command="${1:-checkpoint-b3}"
database="possible_web_menu_test"
compose() { docker compose -f .dev/docker-compose.test.yml "$@"; }
run_odoo() { compose run --rm "$@"; }
run_hoot() { run_odoo -e "POSSIBLE_WEB_MENU_HOOT_DESCRIPTOR=$1" odoo odoo -d "$database" --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -i possible_web_menu --test-enable --test-tags /possible_web_menu:TestWebMenuHoot --stop-after-init; }
compose up -d db
case "$command" in
  js-utils) run_hoot @possible_web_menu/possible_web_menu_utils ;;
  js-interaction) run_hoot @possible_web_menu/possible_web_menu_interaction ;;
  js-builder-cleanup) run_hoot @possible_web_menu/possible_web_menu_builder_cleanup ;;
  backend) run_odoo odoo -d "$database" --db_host=db --db_user=odoo --db_password=odoo --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons -u possible_web_menu --test-enable --test-tags '/possible_web_menu,-/possible_web_menu:TestWebMenuHoot' --stop-after-init ;;
  checkpoint-b3) "$0" js-utils; "$0" js-interaction; "$0" js-builder-cleanup; "$0" backend ;;
  *) echo "Usage: $0 {js-utils|js-interaction|js-builder-cleanup|backend|checkpoint-b3}" >&2; exit 2 ;;
esac
