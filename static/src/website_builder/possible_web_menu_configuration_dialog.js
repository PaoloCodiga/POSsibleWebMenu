/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";

export class PossibleWebMenuConfigurationDialog extends Component {
    static template = "possible_web_menu.ConfigurationDialog";
    static components = { Dialog };
    static props = {
        close: Function,
        configuration: Object,
    };

    setup() {
        const configuration = this.props.configuration;
        this.state = useState({
            loading: true,
            error: "",
            pricelists: [],
            categories: [],
            pricelistId: configuration.pricelistId || 0,
            selectedCategoryIds: [...configuration.posCategoryIds],
            categorySearch: "",
            includeChildCategories: configuration.includeChildCategories,
            filterSale: configuration.filterSale,
            filterPos: configuration.filterPos,
            filterPurchase: configuration.filterPurchase,
            filterMode: configuration.filterMode,
            showDescription: configuration.showDescription,
            showInternalReference: configuration.showInternalReference,
            showUncategorized: configuration.showUncategorized,
            taxDisplay: configuration.taxDisplay,
            sortMode: configuration.sortMode,
            layout: configuration.layout,
            validationRequested: false,
            validationMessage: "",
        });
        onWillStart(() => this.loadOptions());
    }

    async loadOptions() {
        try {
            const options = await rpc("/possible_web_menu/builder/options", {});
            this.state.pricelists = options.pricelists || [];
            this.state.categories = options.categories || [];
        } catch {
            this.state.error = _t("The menu configuration options could not be loaded.");
        } finally {
            this.state.loading = false;
        }
    }

    get isPricelistValid() {
        const pricelistId = Number(this.state.pricelistId);
        return this.state.pricelists.some((pricelist) => pricelist.id === pricelistId);
    }

    get filteredCategories() {
        const search = this.state.categorySearch.trim().toLocaleLowerCase();
        return this.state.categories.filter((category) => !search || category.name.toLocaleLowerCase().includes(search));
    }

    categoryIndent(category) {
        return `padding-inline-start: ${category.depth * 1.25}rem;`;
    }

    isCategorySelected(categoryId) {
        return this.state.selectedCategoryIds.includes(categoryId);
    }

    selectPricelist(event) {
        this.state.pricelistId = Number(event.currentTarget.value);
    }

    toggleCategory(event) {
        const categoryId = Number(event.currentTarget.value);
        const selectedCategoryIds = new Set(this.state.selectedCategoryIds);
        if (event.currentTarget.checked) {
            selectedCategoryIds.add(categoryId);
        } else {
            selectedCategoryIds.delete(categoryId);
        }
        this.state.selectedCategoryIds = [...selectedCategoryIds].sort((left, right) => left - right);
    }

    validateConfiguration() {
        this.state.validationRequested = true;
        this.state.validationMessage = this.isPricelistValid
            ? _t("Configuration is valid. Applying changes is available in Checkpoint C2.")
            : "";
    }
}
