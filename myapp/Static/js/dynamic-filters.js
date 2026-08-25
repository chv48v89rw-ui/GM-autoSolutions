/**
 * Dynamic Filter System for GM AutoSolutions
 * Provides AutoTrader-style dynamic filtering with real-time counts
 */

class DynamicFilters {
    constructor() {
        this.apiEndpoint = '/api/filter-counts/';
        this.filterFields = [
            'make', 'model', 'variant', 'year_from', 'year_to',
            'price_from', 'price_to', 'mileage_from', 'mileage_to',
            'fuel_type', 'transmission', 'condition',
            'engine_size_from', 'engine_size_to', 'doors', 'body_type',
            'previous_owners', 'seats', 'exterior_color', 'interior_color',
            'seat_material', 'interior_trim', 'color', 'features',
            'number_of_keys', 'fuel_economy_source', 'fuel_economy_from',
            'fuel_economy_to', 'fuel_economy_combined', 'value_source'
        ];
        this.debounceTimer = null;
        this.debounceDelay = 300; // milliseconds
        this.currentFilterData = {};
        
        this.init();
    }

    init() {
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupFilters());
        } else {
            this.setupFilters();
        }
    }

    setupFilters() {
        // Find all filter forms
        const filterForms = document.querySelectorAll('#filterForm, #filterFormMobile, form[action="/cars/"]');
        
        filterForms.forEach(form => {
            this.attachEventListeners(form);
        });

        // Initial load of filter data
        this.updateFilterCounts();
    }

    attachEventListeners(form) {
        // Add change event listeners to all filter fields
        this.filterFields.forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.addEventListener('change', () => this.handleFilterChange(form));
                // For text inputs, also listen for input events with debouncing
                if (field.tagName === 'INPUT' && field.type === 'text') {
                    field.addEventListener('input', () => this.handleFilterChange(form));
                }
            }
        });
    }

    handleFilterChange(form) {
        // Debounce the filter update to avoid excessive API calls
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.updateFilterCounts(form);
        }, this.debounceDelay);
    }

    getCurrentFilterValues(form) {
        const filterValues = {};
        
        this.filterFields.forEach(fieldName => {
            const field = form ? form.querySelector(`[name="${fieldName}"]`) : document.querySelector(`[name="${fieldName}"]`);
            if (field && field.value) {
                filterValues[fieldName] = field.value;
            }
        });

        return filterValues;
    }

    async updateFilterCounts(form = null) {
        try {
            const filterValues = this.getCurrentFilterValues(form);
            const queryString = new URLSearchParams(filterValues).toString();
            
            const response = await fetch(`${this.apiEndpoint}?${queryString}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.currentFilterData = data;
            
            // Update all filter dropdowns with new data
            this.updateFilterDropdowns(data, form);
            
        } catch (error) {
            console.error('Error updating filter counts:', error);
        }
    }

    updateFilterDropdowns(data, form = null) {
        // Map of API field names to form field names
        const fieldMappings = {
            'make': 'make',
            'model': 'model',
            'variant': 'variant',
            'year': 'year_from', // Will update both year_from and year_to
            'price': 'price_from', // Will update both price_from and price_to
            'mileage': 'mileage_from', // Will update both mileage_from and mileage_to
            'fuel_type': 'fuel_type',
            'transmission': 'transmission',
            'condition': 'condition',
            'engine_size': 'engine_size_from', // Will update both engine_size_from and engine_size_to
            'doors': 'doors',
            'body_type': 'body_type',
            'previous_owners': 'previous_owners',
            'seats': 'seats',
            'exterior_color': 'exterior_color',
            'interior_color': 'interior_color',
            'seat_material': 'seat_material',
            'interior_trim': 'interior_trim',
            'number_of_keys': 'number_of_keys',
            'fuel_economy_source': 'fuel_economy_source',
            'fuel_economy_combined': 'fuel_economy_combined',
            'value_source': 'value_source'
        };

        // Update each dropdown
        Object.keys(fieldMappings).forEach(apiField => {
            const formField = fieldMappings[apiField];
            const selectElement = form ? form.querySelector(`[name="${formField}"]`) : document.querySelector(`[name="${formField}"]`);
            
            if (selectElement && data[apiField]) {
                this.updateSelectOptions(selectElement, data[apiField], formField);
            }
        });
    }

    updateSelectOptions(selectElement, options, fieldName) {
        // Store current selection
        const currentValue = selectElement.value;
        
        // Clear existing options (keep the first empty option)
        const firstOption = selectElement.querySelector('option:first-child');
        selectElement.innerHTML = '';
        
        if (firstOption) {
            selectElement.appendChild(firstOption);
        } else {
            // Add default empty option if it doesn't exist
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = this.getDefaultLabel(fieldName);
            selectElement.appendChild(defaultOption);
        }
        
        // Add new options with counts
        options.forEach(option => {
            if (option.count > 0) { // Only show options with counts
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = `${option.label} (${option.count})`;
                selectElement.appendChild(optionElement);
            }
        });
        
        // Restore selection if it still exists in the new options
        const optionExists = Array.from(selectElement.options).some(option => option.value === currentValue);
        if (optionExists) {
            selectElement.value = currentValue;
        } else {
            selectElement.value = '';
        }
    }

    getDefaultLabel(fieldName) {
        const labels = {
            'make': '-- All Makes --',
            'model': '-- All Models --',
            'variant': '-- All Variants --',
            'year_from': '-- Year from --',
            'year_to': '-- Year to --',
            'price_from': '-- Price from --',
            'price_to': '-- Price to --',
            'mileage_from': '-- Mileage from --',
            'mileage_to': '-- Mileage to --',
            'fuel_type': '-- All Fuel Types --',
            'transmission': '-- All Transmissions --',
            'condition': '-- All Conditions --',
            'engine_size_from': '-- Engine Size from --',
            'engine_size_to': '-- Engine Size to --',
            'doors': '-- All Doors --',
            'body_type': '-- All Body Types --',
            'previous_owners': '-- All Owners --',
            'seats': '-- All Seats --',
            'exterior_color': '-- All Exterior Colors --',
            'interior_color': '-- All Interior Colors --',
            'seat_material': '-- All Seat Materials --',
            'interior_trim': '-- All Interior Trims --',
            'number_of_keys': '-- All Keys --',
            'fuel_economy_source': '-- All Fuel Economy Sources --',
            'fuel_economy_combined': '-- All Fuel Economy --',
            'value_source': '-- All Value Sources --'
        };
        
        return labels[fieldName] || '-- Select --';
    }

    // Public method to manually trigger filter update
    refreshFilters() {
        this.updateFilterCounts();
    }
}

// Initialize the dynamic filters system
const dynamicFilters = new DynamicFilters();

// Make it available globally for potential external use
window.DynamicFilters = DynamicFilters;
window.dynamicFilters = dynamicFilters;