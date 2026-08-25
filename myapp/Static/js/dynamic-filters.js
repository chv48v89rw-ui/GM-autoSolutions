/**
 * Basic Filter System for GM AutoSolutions
 * Provides simple cascading dropdown functionality for make/model/variant
 */

document.addEventListener('DOMContentLoaded', function() {
    const makeSelect = document.getElementById('id_make');
    const modelSelect = document.getElementById('id_model');
    const variantSelect = document.getElementById('id_variant');
    
    function loadModels(make) {
        if (!make) {
            modelSelect.innerHTML = '<option value="">-- All Models --</option>';
            variantSelect.innerHTML = '<option value="">-- All Variants --</option>';
            return;
        }
        
        fetch(`/api/models-for-make/?make=${encodeURIComponent(make)}`)
            .then(response => response.json())
            .then(data => {
                modelSelect.innerHTML = '<option value="">-- All Models --</option>';
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model;
                    option.textContent = model;
                    modelSelect.appendChild(option);
                });
                
                // Trigger variant load with current model selection
                loadVariants(make, modelSelect.value);
            })
            .catch(error => console.error('Error loading models:', error));
    }
    
    function loadVariants(make, model) {
        if (!make || !model) {
            variantSelect.innerHTML = '<option value="">-- All Variants --</option>';
            return;
        }
        
        fetch(`/api/models-for-make/?make=${encodeURIComponent(make)}&model=${encodeURIComponent(model)}`)
            .then(response => response.json())
            .then(data => {
                variantSelect.innerHTML = '<option value="">-- All Variants --</option>';
                if (data.variants && data.variants.length > 0) {
                    data.variants.forEach(variant => {
                        const option = document.createElement('option');
                        option.value = variant;
                        option.textContent = variant;
                        variantSelect.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error loading variants:', error));
    }
    
    if (makeSelect) {
        makeSelect.addEventListener('change', function() {
            loadModels(this.value);
        });
        
        // Load models on page load if make is selected
        if (makeSelect.value) {
            loadModels(makeSelect.value);
        }
    }
    
    if (modelSelect) {
        modelSelect.addEventListener('change', function() {
            loadVariants(makeSelect.value, this.value);
        });
    }
});