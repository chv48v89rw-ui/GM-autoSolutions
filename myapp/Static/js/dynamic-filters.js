/**
 * Complete Filter System for GM AutoSolutions
 * Provides cascading dropdown functionality for make/model/variant using CAR_HIERARCHY
 */

// CAR_HIERARCHY data structure (mirrors the Python version)
const CAR_HIERARCHY = {
    'Toyota': {
        'Alphard': ['240G', '240S', '250S', '350G', '350S', 'Executive Lounge', 'Hybrid'],
        'Century': ['Standard', 'SUV'],
        'Crown': [
            'Royal Saloon', 'Royal Extra',
            'Athlete', 'Majesta',
            'RS', 'G', 'Hybrid',
            'Crossover', 'Sport', 'Estate', 'Sedan'
        ],
        'Crown Majesta': ['A-Type', 'C-Type'],
        'Fortuner': ['GX', 'GXL', 'Crusade', 'Legender', 'GR Sport'],
        'GR86': ['RC', 'SZ', 'RZ', 'Premium'],
        'GR Corolla': ['Core', 'Circuit', 'Morizo'],
        'GR Supra': ['2.0', '3.0 Premium', 'A91 Edition'],
        'GR Yaris': ['RC', 'RZ', 'GRMN'],
        'GranAce': ['Premium', 'G'],
        'Granvia': ['Premium', 'VX'],
        'Land Cruiser': [
            '40 Series', '55 Series',
            '60 Series', '70 Series',
            '80 Series', '90 Series',
            '100 Series', '105 Series',
            '200 Series', '250 Series',
            '300 Series',
            'GR Sport',
            'ZX', 'VX', 'GX', 'AX'
        ],
        'Land Cruiser Prado': [
            'TX', 'TX-L', 'TZ',
            'TZ-G', 'VX',
            'GX', 'VX-L',
            'Kakadu',
            'Altitude'
        ],
        'Mirai': ['XLE', 'Limited'],
        'Sequoia': ['SR5', 'Limited', 'Platinum', 'Capstone', 'TRD Pro'],
        'Sienna': ['LE', 'XLE', 'Limited', 'Platinum', 'Hybrid'],
        'Tacoma': ['SR', 'SR5', 'TRD Sport', 'TRD Off-Road', 'Limited', 'TRD Pro'],
        'Tundra': ['SR', 'SR5', 'Limited', '1794 Edition', 'Platinum', 'Capstone', 'TRD Pro'],
        'Vellfire': ['2.4Z', '2.5Z', '3.5Z', 'Executive Lounge', 'Hybrid']
    },
    'Honda': {
        'Pilot': ['EX-L', 'Touring'],
        'Ridgeline': ['Sport', 'RTL'],
    },
    'BMW': {
        '1 Series': [
            '114i', '116d', '116i', '118d', '118i',
            '120d', '120i', '123d', '125d',
            '125i', '128ti', '130i',
            '135i', 'M135i', 'M140i'
        ],
        '2 Series': [
            'M235i', 'M240i'
        ],
        '3 Series': [
            '330d', '330e', '330i',
            '335d', '335i',
            '340d', '340i',
            'M340d', 'M340i',
            'M Sport',
            'M3', 'M3 Competition', 'M3 CS'
        ],
        '4 Series': [
            '418d', '418i',
            '420d', '420i',
            '425d', '428i',
            '430d', '430i',
            '435d', '435i',
            '440d', '440i',
            'M440d', 'M440i',
            'M Sport',
            'M4', 'M4 Competition', 'M4 CSL'
        ],
        '5 Series': [
            '518d', '520d', '520i',
            '523i', '525d', '525i',
            '528i', '530d', '530e', '530i',
            '535d', '535i',
            '540d', '540i',
            '545e',
            '550d', '550i',
            'M550i',
            'M Sport',
            'M5', 'M5 Competition', 'M5 CS'
        ],
        '6 Series': [
            '620d',
            '630d', '630i',
            '635d', '635i',
            '640d', '640i',
            '650i',
            'M6'
        ],
        '7 Series': [
            '725d', '728i',
            '730d', '730i',
            '735i',
            '740d', '740e', '740i',
            '745e',
            '750d', '750i',
            '760Li', '760i',
            'M760Li'
        ],
        '8 Series': [
            '840d', '840i',
            '850i',
            'M850i',
            'M8', 'M8 Competition'
        ],
        'X1': [
            'sDrive16d',
            'sDrive18d', 'sDrive18i',
            'sDrive20d', 'sDrive20i',
            'xDrive18d',
            'xDrive20d', 'xDrive20i',
            'xDrive23i',
            'xDrive25d', 'xDrive25e', 'xDrive25i',
            'xDrive28i',
            'xDrive30e'
        ],
        'X2': [
            'sDrive18d', 'sDrive18i',
            'sDrive20i',
            'xDrive20d', 'xDrive20i',
            'xDrive25e',
            'M35i'
        ],
        'X3': [
            'sDrive18d',
            'xDrive20d', 'xDrive20i',
            'xDrive30d', 'xDrive30e', 'xDrive30i',
            'xDrive35d',
            'M40d', 'M40i',
            'X3 M', 'X3 M Competition'
        ],
        'X4': [
            'xDrive20d', 'xDrive20i',
            'xDrive30d', 'xDrive30i',
            'M40d', 'M40i',
            'X4 M', 'X4 M Competition'
        ],
        'X5': [
            'xDrive25d',
            'xDrive30d',
            'xDrive35d',
            'xDrive40d', 'xDrive40i',
            'xDrive45e',
            'xDrive50e',
            'M50d', 'M50i',
            'X5 M', 'X5 M Competition'
        ],
        'X6': [
            'xDrive30d',
            'xDrive35i',
            'xDrive40d', 'xDrive40i',
            'M50d', 'M50i',
            'X6 M', 'X6 M Competition'
        ],
        'X7': [
            'xDrive30d',
            'xDrive40d', 'xDrive40i',
            'xDrive50d',
            'M50d',
            'M60i',
            'XB7 Alpina'
        ],
        'XM': [
            'XM',
            'XM Label',
            'XM Label Red'
        ],
        'Z4': [
            'sDrive18i',
            'sDrive20i',
            'sDrive23i',
            'sDrive28i',
            'sDrive30i',
            'M40i'
        ],
        'i Series': [
            'i3',
            'i4 eDrive35',
            'i4 eDrive40',
            'i4 xDrive40',
            'i4 M50',
            'i5 eDrive40',
            'i5 xDrive40',
            'i5 M60',
            'i7 eDrive50',
            'i7 xDrive60',
            'i7 M70',
            'iX xDrive40',
            'iX xDrive50',
            'iX M60',
            'iX1',
            'iX2',
            'iX3'
        ],
        'M Models': [
            'M2',
            'M2 Competition',
            'M2 CS',
            'M3',
            'M3 Competition',
            'M3 CS',
            'M4',
            'M4 Competition',
            'M4 CSL',
            'M5',
            'M5 Competition',
            'M5 CS',
            'M6',
            'M8',
            'M8 Competition',
            'X3 M',
            'X3 M Competition',
            'X4 M',
            'X4 M Competition',
            'X5 M',
            'X5 M Competition',
            'X6 M',
            'X6 M Competition',
            'XM',
            'XM Label',
            'XM Label Red'
        ]
    },
    'Mercedes-Benz': {
        'A-Class': [
            'A35 AMG', 'A45 AMG', 'A45 S AMG'
        ],
        'C-Class': [
            'C200', 'C220d',
            'C300', 'C300e', 'C350', 'C350e',
            'C400', 'C36 AMG', 'C43 AMG',
            'C55 AMG', 'C63 AMG', 'C63 S AMG'
        ],
        'E-Class': [
            'E180', 'E200', 'E200 CGI', 'E220 CDI',
            'E220d', 'E230', 'E240', 'E250',
            'E250 CDI', 'E270 CDI', 'E280',
            'E300', 'E300 BlueTEC', 'E300e',
            'E320', 'E350', 'E350 CDI',
            'E350e', 'E400', 'E430',
            'E450', 'E500', 'E550',
            'E63 AMG', 'E63 S AMG'
        ],
        'S-Class': [
            'S320', 'S350', 'S400', 'S420',
            'S430', 'S450', 'S500', 'S550',
            'S560', 'S600', 'S63 AMG', 'S65 AMG',
            'S63 AMG', 'S65 AMG', 'Maybach', 'Pullman'
        ],
        'G-Class': [
            'G350', 'G500', 'G550', 'G63 AMG',
            'G65 AMG', '4x4²'
        ],
        'GLC': [
            'GLC200', 'GLC220d', 'GLC250', 'GLC300',
            'GLC350e', 'GLC43 AMG', 'GLC63 AMG', 'GLC63 S AMG'
        ],
        'GLE': [
            'GLE300', 'GLE350', 'GLE400', 'GLE450',
            'GLE500', 'GLE580', 'GLE43 AMG', 'GLE63 AMG', 'GLE63 S AMG'
        ],
        'GLS': [
            'GLS450', 'GLS550', 'GLS580', 'GLS63 AMG'
        ],
        'AMG GT': [
            'AMG GT', 'AMG GT S', 'AMG GT R', 'AMG GT R Pro',
            'AMG GT C', 'AMG GT 4-Door', 'AMG GT 63 S'
        ],
        'SL': [
            'SL43', 'SL55 AMG', 'SL63 AMG'
        ],
        'SLC': [
            'SLC180', 'SLC200', 'SLC300', 'SLC43 AMG'
        ],
        'CLS': [
            'CLS220', 'CLS250', 'CLS300', 'CLS350',
            'CLS450', 'CLS53 AMG', 'CLS63 AMG'
        ],
        'EQA': [
            'EQA250', 'EQA300', 'EQA350'
        ],
        'EQB': [
            'EQB250', 'EQB300', 'EQB350'
        ],
        'EQC': [
            'EQC300', 'EQC400'
        ],
        'EQE': [
            'EQE300', 'EQE350', 'EQE43 AMG', 'EQE53 AMG'
        ],
        'EQS': [
            'EQS450', 'EQS450+', 'EQS580', 'EQS53 AMG'
        ],
        'Maybach': [
            'S480', 'S500', 'S560', 'S680',
            'GLS600', 'Mercedes-Maybach'
        ]
    }
};

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
        
        const models = CAR_HIERARCHY[make] ? Object.keys(CAR_HIERARCHY[make]) : [];
        modelSelect.innerHTML = '<option value="">-- All Models --</option>';
        
        models.sort().forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            modelSelect.appendChild(option);
        });
        
        // Trigger variant load with current model selection
        loadVariants(make, modelSelect.value);
    }
    
    function loadVariants(make, model) {
        if (!make || !model) {
            variantSelect.innerHTML = '<option value="">-- All Variants --</option>';
            return;
        }
        
        const variants = CAR_HIERARCHY[make] && CAR_HIERARCHY[make][model] 
            ? CAR_HIERARCHY[make][model] 
            : [];
        
        variantSelect.innerHTML = '<option value="">-- All Variants --</option>';
        
        const uniqueVariants = [...new Set(variants)].sort();
        uniqueVariants.forEach(variant => {
            const option = document.createElement('option');
            option.value = variant;
            option.textContent = variant;
            variantSelect.appendChild(option);
        });
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