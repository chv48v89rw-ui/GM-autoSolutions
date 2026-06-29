from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Report, 
                     SavedSearch, CarComparison, Notification, NotificationPreference)

CAR_HIERARCHY = {
    'Toyota': {
        'Corolla': ['Axio', 'Fielder', 'NZE', 'RunX'],
        'Premio': ['X', 'G', 'G Superior'],
        'Allion': ['X', 'G'],
        'Mark X': ['250G', '300G'],
        'Crown': ['Athlete', 'Royal Saloon', 'Majesta'],
        'Vitz': ['F', 'U', 'RS'],
        'Yaris': ['F', 'Sport'],
        'Aqua': ['Hybrid'],
        'IST': ['150G'],
        'Passo': ['X', 'G'],
        'Harrier': ['Elegance', 'Premium', 'Progress', 'Hybrid'],
        'RAV4': ['J', 'G', 'Adventure', 'Limited', '4WD'],
        'Vanguard': ['240S', '350S'],
        'Land Cruiser': ['70 Series', '80 Series', '100 Series', '200 Series', '300 Series'],
        'Land Cruiser Prado': ['TX', 'TX-L', 'TZ', 'TZ-G', 'VX'],
        'Hilux': ['Single Cab', 'Extra Cab', 'Double Cab', '2WD', '4WD', 'Revo'],
        'Probox': ['DX', 'GL'],
        'Succeed': ['UL', 'UL-X'],
        'Noah': ['X', 'G', 'Hybrid'],
        'Voxy': ['X', 'ZS', 'Hybrid'],
        'Esquire': ['Gi', 'Hybrid'],
        'Alphard': ['240S', '350S', 'Executive Lounge'],
        'Vellfire': ['2.4Z', '3.5Z', 'Executive Lounge'],
        'Hiace': ['Commuter', 'DX', 'GL'],
        'Camry': ['GL', 'Grande', 'Hybrid'],
    'Auris': ['150X', 'RS'],
    'Prius': ['S', 'G', 'A'],
    'Prius Alpha': ['S', 'G'],
    'Corolla Cross': ['G', 'Hybrid'],
    'C-HR': ['G', 'Hybrid'],
    'Raize': ['X', 'G', 'Z'],
    'Rush': ['X', 'G'],
    'Sienta': ['X', 'G', 'Hybrid'],
    'Wish': ['X', 'S'],
    'Belta': ['X', 'G'],
    'bB': ['S', 'Z'],
    'Blade': ['Master'],
    'Porte': ['F', 'G'],
    'Spade': ['F', 'G'],
    'Raum': ['C', 'G'],
    'Ractis': ['X', 'G'],
    'FJ Cruiser': ['Base'],
    'Kluger': ['Grande', 'GX'],
    'Highlander': ['XLE', 'Limited'],
    'Tacoma': ['SR', 'SR5', 'TRD Sport'],
    'Tundra': ['SR5', 'Limited'],
    'Sequoia': ['SR5', 'Limited'],
    'LiteAce': ['DX'],
    'TownAce': ['DX'],
    'Dyna': ['Truck'],
    'ToyoAce': ['Truck'],
    'Coaster': ['Standard', 'High Roof'],
    'Granvia': ['Premium'],
    'bZ4X': ['FWD', 'AWD'],
    'GR86': ['SZ', 'RZ'],
    'GR Corolla': ['Core', 'Circuit'],
    'GR Yaris': ['RZ'],
    },

    'Honda': {
        'Fit': ['F', 'RS', 'Hybrid'],
        'Jazz': ['Base'],
        'Civic': ['LX', 'EX', 'RS', 'Sport'],
        'Accord': ['LX', 'EX', 'Touring', 'Hybrid'],
        'Insight': ['Hybrid'],
        'Vezel': ['Hybrid', 'RS'],
        'CR-V': ['LX', 'EX', 'EX-L'],
        'HR-V': ['LX', 'EX'],
        'Stepwgn': ['Spada', 'Air'],
        'Freed': ['G', 'Hybrid'],
        'Odyssey': ['Absolute', 'Hybrid'],
        'City': ['S', 'V', 'RS'],
        'Airwave': ['M', 'L'],
        'Stream': ['RSZ', 'X'],
        'Shuttle': ['G', 'Hybrid'],
        'Grace': ['LX', 'Hybrid'],
        'CR-Z': ['Alpha', 'Hybrid'],
        'Element': ['EX'],
        'Life': ['C', 'Diva'],
        'N-Box': ['G', 'Custom'],
        'N-One': ['Premium', 'RS'],
        'N-WGN': ['G', 'Custom'],
        'Mobilio': ['Spike', 'X'],
        'Edix': ['20X'],
        'Crossroad': ['18L', '20X'],
        'Pilot': ['EX-L', 'Touring'],
        'Ridgeline': ['Sport', 'RTL'],
        'ZR-V': ['Sport', 'e:HEV'],
        'e': ['Advance'],
        },

    'BMW': {
    '1 Series': ['116i', '118i', '120i', 'M135i'],
    '2 Series': ['218i', '220i', 'M240i'],
    '3 Series': ['318i', '320i', '330i', '340i', 'M Sport'],
    '4 Series': ['420i', '430i', '440i', 'M Sport'],
    '5 Series': ['520i', '530i', '540i', 'M550i', 'M Sport'],
    '6 Series': ['630i', '640i'],
    '7 Series': ['730i', '740i', '750i', '760Li'],
    '8 Series': ['840i', '850i'],

    'X1': ['sDrive18i', 'xDrive20i', 'xDrive25i'],
    'X2': ['sDrive18i', 'xDrive20i'],
    'X3': ['xDrive20i', 'xDrive30i', 'M40i'],
    'X4': ['xDrive20i', 'xDrive30i', 'M40i'],
    'X5': ['xDrive30d', 'xDrive40i', 'xDrive45e'],
    'X6': ['xDrive40i', 'M50i'],
    'X7': ['xDrive40i', 'M60i'],

    'Z4': ['sDrive20i', 'M40i'],

    'i Series': ['i3', 'i4', 'i5', 'i7', 'iX'],

    'M Models': ['M2', 'M3', 'M4', 'M5', 'M8', 'XM']
},

    'Mercedes-Benz': {
    'A-Class': ['A180', 'A200', 'A250', 'A35 AMG', 'A45 AMG'],
    'B-Class': ['B180', 'B200'],

    'C-Class': ['C180', 'C200', 'C220d', 'C250', 'C300', 'C43 AMG', 'C63 AMG'],
    'E-Class': ['E200', 'E250', 'E300', 'E350', 'E400', 'E53 AMG', 'E63 AMG'],

    'S-Class': ['S350', 'S400', 'S450', 'S500', 'S560', 'S580', 'S680', 'Maybach'],

    'CLA': ['CLA180', 'CLA200', 'CLA250', 'CLA35 AMG', 'CLA45 AMG'],
    'CLS': ['CLS220d', 'CLS350', 'CLS400'],

    'GLA': ['GLA180', 'GLA200', 'GLA250', 'GLA35 AMG'],
    'GLB': ['GLB180', 'GLB200', 'GLB250'],
    'GLC': ['GLC200', 'GLC220d', 'GLC300', 'GLC43 AMG', 'GLC63 AMG'],
    'GLE': ['GLE250d', 'GLE300d', 'GLE350', 'GLE400', 'GLE450', 'GLE53 AMG', 'GLE63 AMG'],
    'GLS': ['GLS350d', 'GLS400d', 'GLS450', 'GLS580', 'Maybach GLS'],

    'G-Class': ['G350d', 'G400d', 'G63 AMG'],

    'SL': ['SL400', 'SL500', 'SL55 AMG', 'SL63 AMG'],
    'SLC': ['SLC180', 'SLC200'],
    'SLK': ['SLK200', 'SLK350'],

    'EQ Series': ['EQA 250', 'EQB 300', 'EQC 400', 'EQE 350', 'EQS 450', 'EQS 580'],

    'AMG GT': ['AMG GT 43', 'AMG GT 53', 'AMG GT 63'],

    'Vito': ['111 CDI', '114 CDI', '119 CDI'],
    'V-Class': ['V220d', 'V250d'],

    'Sprinter': ['311 CDI', '313 CDI', '316 CDI', '319 CDI']
},

   'Audi': {
    'A1': ['Sportback'],
    'A3': ['30 TFSI', '35 TFSI', '40 TFSI', 'S3', 'RS3'],
    'A4': ['30 TFSI', '35 TFSI', '40 TFSI', 'S4'],
    'A5': ['40 TFSI', '45 TFSI', 'S5'],
    'A6': ['35 TFSI', '40 TFSI', '45 TFSI', '50 TDI', 'S6'],
    'A7': ['45 TFSI', '50 TDI', '55 TFSI', 'S7'],
    'A8': ['55 TFSI', '60 TFSI', 'L'],

    'Q2': ['30 TFSI', '35 TFSI'],
    'Q3': ['35 TFSI', '40 TFSI', '45 TFSI', 'RS Q3'],
    'Q5': ['40 TFSI', '45 TDI', '50 TDI', 'SQ5'],
    'Q7': ['45 TFSI', '50 TDI', '55 TFSI', 'SQ7'],
    'Q8': ['55 TFSI', '60 TFSI', 'SQ8', 'RS Q8'],

    'TT': ['40 TFSI', '45 TFSI', 'TTS', 'TT RS'],

    'e-tron': ['50 Quattro', '55 Quattro', 'GT'],

    'RS Models': ['RS3', 'RS4', 'RS5', 'RS6', 'RS7', 'RS Q8']
},

    'Lexus': {
    'IS': ['250', '300', '300h', '350', 'F Sport'],
    'ES': ['250', '300h', '350', '250h'],
    'GS': ['250', '300', '350', '450h'],
    'LS': ['460', '500h', '600h', 'LS 500'],

    'NX': ['200t', '300h', '350h', '250', '350'],
    'RX': ['270', '350', '450h', '200t', '300', '350h'],

    'UX': ['200', '250h'],
    'CT': ['200h'],

    'GX': ['460', '470', '550'],
    'LX': ['450d', '570', '600'],

    'RC': ['300', '350', '300h', 'F Sport', 'RC F'],
    'LC': ['500', '500h', 'LC 500'],
    'LM': ['350', '500h'],  # luxury van (very important for Kenya elites)

    'HS': ['250h'],
},

   'Volkswagen': {
    'Golf': ['TSI', 'TDI', 'GTI', 'R', 'GTE'],
    'Polo': ['TSI', 'GTI', 'Comfortline'],
    'Passat': ['TSI', 'TDI', 'R-Line'],
    'Jetta': ['TSI', 'GLI'],

    'Tiguan': ['TSI', 'TDI', '4Motion', 'R-Line'],
    'Touareg': ['V6 TDI', 'V6 TSI', 'R-Line'],

    'Amarok': ['TDI', 'V6 TDI', 'Aventura'],

    # Common in Kenya imports
    'Touran': ['TSI', 'TDI'],
    'Sharan': ['TSI', 'TDI'],
    'Caddy': ['Van', 'Life', 'Cargo'],

    'Transporter': ['T5', 'T6', 'T6.1'],
    'Caravelle': ['T5', 'T6'],

    'Multivan': ['Comfortline', 'Highline'],

    # Compact SUVs (very important for modern Kenya imports)
    'T-Cross': ['TSI'],
    'T-Roc': ['TSI', 'R'],
    'Taigo': ['TSI'],

    # EV line (starting to appear in Kenya)
    'ID.3': ['Pro', 'Pro S'],
    'ID.4': ['Pure', 'Pro', 'GTX'],
    'ID.5': ['Pro', 'GTX'],

    # Performance
    'Arteon': ['TSI', 'R-Line'],
},

    'Ford': {
    'Ranger': ['2.2 TDCi', '3.2 TDCi', '2.0 Bi-Turbo', 'Wildtrak', 'XLT', 'XL'],
    'Everest': ['Trend', 'Titanium', 'Limited', 'Platinum'],

    'Focus': ['S', 'SE', 'Titanium', 'ST'],
    'Fiesta': ['S', 'SE', 'ST'],
    'Mondeo': ['Trend', 'Titanium'],

    'Kuga': ['EcoBoost', 'Titanium'],

    'Explorer': ['XLT', 'Limited', 'ST'],

    'Mustang': ['GT V8', 'EcoBoost', 'Mach 1'],

    # Very important for Kenya (commercial + imports)
    'Transit': ['Van', 'Bus', 'Custom'],
    'Tourneo': ['Connect', 'Custom'],

    'Edge': ['Titanium', 'Sport'],

    'EcoSport': ['Trend', 'Titanium'],

    'F-150': ['XL', 'XLT', 'Lariat', 'Raptor'],

    'Bronco': ['Base', 'Big Bend', 'Wildtrak', 'Raptor'],
},

    'Chevrolet': {
    'Spark': ['LS', 'LT'],
    'Aveo': ['LS', 'LT'],
    'Cruze': ['LS', 'LT', 'Premier'],
    'Sonic': ['LS', 'LT'],
    'Optra': ['LS', 'LT'],

    'Malibu': ['LS', 'LT', 'Premier'],
    'Impala': ['LT', 'Premier'],

    'Captiva': ['LS', 'LT'],
    'Trailblazer': ['LT', 'LTZ'],

    'Equinox': ['LS', 'LT'],
    'Traverse': ['LS', 'LT'],

    'Colorado': ['LT', 'Z71', 'High Country'],

    'Tahoe': ['LT', 'LTZ'],
    'Suburban': ['LT', 'Premier'],
},

    'Hyundai': {
    'i10': ['Base', 'Grand'],
    'i20': ['Base', 'Active'],
    'i30': ['Base', 'N Line'],

    'Accent': ['GLS', 'Sport'],
    'Elantra': ['SE', 'SEL', 'Limited'],
    'Sonata': ['SE', 'SEL', 'Hybrid'],

    'i40': ['Sedan', 'Tourer'],

    'Tucson': ['GLS', 'Limited', 'N Line'],
    'Santa Fe': ['Sport', 'Limited', 'Calligraphy'],

    'Kona': ['Base', 'Electric', 'N Line'],
    'Creta': ['Base', 'SX'],
    'Venue': ['Base', 'SX'],

    'Palisade': ['SEL', 'Limited', 'Calligraphy'],

    'ix35': ['GLS', 'Limited'],
    'ix20': ['GLS'],

    'Staria': ['Van', 'Tourer'],
    'H-1': ['Van', 'Bus'],

    'Ioniq': ['Hybrid', 'Electric'],
    'Ioniq 5': ['Standard', 'Long Range', 'AWD'],
    'Ioniq 6': ['Standard', 'Long Range'],

    'Porter': ['Truck'],
    'Mighty': ['Truck'],
},

    'Kia': {
    'Picanto': ['Base', 'EX', 'GT-Line'],
    'Morning': ['Base', 'EX'],

    'Rio': ['Base', 'EX', 'GT-Line'],

    'Cerato': ['S', 'EX', 'GT', 'Forte'],

    'Optima': ['EX', 'SX', 'Hybrid'],
    'K5': ['LX', 'GT-Line'],

    'Sportage': ['LX', 'EX', 'GT-Line'],
    'Sorento': ['LX', 'EX', 'SX'],
    'Seltos': ['EX', 'GT-Line'],

    'Stonic': ['EX', 'GT-Line'],

    'Carnival': ['LX', 'EX', 'SX'],
    'Carens': ['LX', 'EX'],

    'Niro': ['Hybrid', 'EV'],

    'EV6': ['Light', 'Wind', 'GT'],
    'EV9': ['Air', 'Earth', 'GT-Line'],
},

   'Nissan': {
    'March': ['Base'],
    'Micra': ['Base'],

    'Note': ['e-Power', 'X', 'Medalist'],
    'Tiida': ['Latio', 'Axis'],

    'Juke': ['Base'],

    'Bluebird Sylphy': ['G', 'X'],
    'Sunny': ['EX', 'Super Saloon'],

    'Latio': ['X', 'G'],

    'X-Trail': ['20S', '20X', 'Hybrid', '4WD'],
    'Qashqai': ['2WD', '4WD'],

    'Kicks': ['X', 'e-Power'],
    
    'Murano': ['XV'],
    'Pathfinder': ['SE', 'LE'],
    'Terrano': ['2.0', '4WD'],

    'Patrol': ['Y61', 'Y62'],

    'Navara': ['King Cab', 'Double Cab', '4WD', 'PRO-4X'],

    'Serena': ['Highway Star', 'S-Hybrid'],

    'Elgrand': ['250 Highway Star', '350 Highway Star'],

    'Caravan': ['DX', 'GX'],
    'NV200': ['Vanette', 'DX'],

    'Note Aura': ['e-Power'],
    'Dayz': ['Highway Star'],

    'Leaf': ['S', 'SV', 'SL'],
},

    'Mazda': {
    'Demio': ['13S', '15S', 'SKYACTIV'],
    'Mazda2': ['15S', 'Hybrid'],

    'Axela': ['15S', '20S'],
    'Mazda3': ['15S', '20S', 'Skyactiv-G'],

    'Atenza': ['20S', '25S'],
    'Mazda6': ['20S', '25S', 'Diesel'],

    'CX-3': ['15S', '20S'],
    'CX-30': ['20S', '25S', 'Skyactiv-X'],

    'CX-5': ['20S', '25S', '2.2D', 'Skyactiv-G'],
    'CX-50': ['2.5 S', 'Turbo'],

    'CX-8': ['25S', '2.2D'],
    'CX-9': ['25T', '2.5T'],

    'CX-60': ['PHEV', 'Diesel'],
    'CX-90': ['Turbo', 'PHEV'],

    'BT-50': ['Single Cab', 'Double Cab', '3.2D'],

    'Bongo': ['Van', 'Truck'],
    'Scrum': ['Van'],
    'Flair': ['XG', 'Hybrid'],
    'Carol': ['GX'],
},

   'Subaru': {
    'Impreza': ['1.6i', '2.0i', '2.0i-S'],
    
    'Legacy': ['2.0i', '2.5i', 'GT'],
    'Legacy B4': ['2.0GT', '2.5GT'],

    'Outback': ['2.5i', '3.6R', 'Premium'],

    'Forester': ['2.0i', '2.0XT', '2.5i', 'Premium', 'Advance'],

    'XV': ['1.6i', '2.0i', '2.0e-Boxer'],
    'Crosstrek': ['2.0i', 'Hybrid'],

    'WRX': ['STI', 'S4', 'Turbo'],

    'Levorg': ['1.6GT', '2.0GT'],

    'Exiga': ['2.0i', '2.5i'],

    'BRZ': ['S', 'R'],

    'Justy': ['1.0i'],

    'Sambar': ['Truck', 'Van'],

    'Pleo': ['L', 'RS'],

    'Stella': ['Custom'],
},

    'Volvo': {
    'S60': ['T4', 'T5', 'T6', 'Recharge'],
    'S90': ['T5', 'T6', 'Recharge'],

    'V40': ['T3', 'T4'],

    'V60': ['T4', 'T5', 'T6', 'Recharge'],

    'XC40': ['T4', 'T5', 'Recharge', 'Pure Electric'],
    'XC60': ['T5', 'T6', 'Recharge'],
    'XC90': ['T5', 'T6', 'Recharge'],

    'EX30': ['Single Motor', 'Twin Motor'],

    'EX40': ['Single Motor', 'Twin Motor'],

    'C40': ['Recharge'],

    'S80': ['2.0', '2.5T'],
},

  'Land Rover / Range Rover': {
    'Defender': ['90', '110', '130', 'X', 'SE', 'HSE'],

    'Discovery': ['3', '4', '5', 'SE', 'HSE'],
    'Discovery Sport': ['S', 'SE', 'HSE', 'R-Dynamic'],

    'Range Rover': ['Vogue', 'Autobiography', 'HSE', 'SV', 'SV Autobiography'],

    'Range Rover Sport': ['SE', 'HSE', 'HSE Dynamic', 'Autobiography', 'SVR'],

    'Range Rover Velar': ['S', 'SE', 'R-Dynamic S', 'R-Dynamic SE', 'R-Dynamic HSE'],

    'Range Rover Evoque': ['S', 'SE', 'HSE', 'R-Dynamic'],

    'Freelander': ['2', 'HSE'],

    'Classic Range Rover': ['3.0', '4.4 V8'],
},
    'Suzuki': {
    'Alto': ['Base', 'VXL'],

    'Swift': ['GL', 'GLX', 'RS'],

    'Baleno': ['GL', 'GLX'],

    'Celerio': ['Base', 'GL'],

    'Dzire': ['GL', 'GLX'],

    'Jimny': ['JL', 'JLX', 'GLX'],

    'Vitara': ['GL', 'GLX'],

    'Grand Vitara': ['JX', 'LX'],

    'Escudo': ['XG', 'XL'],

    'Wagon R': ['FX', 'FX-S'],

    'Every': ['Van', 'Join', 'PA'],
    
    'Spacia': ['Hybrid X', 'Custom'],
},

    'Mitsubishi': {
    'Lancer': ['GLX', 'EX', 'EVO X'],

    'Outlander': ['24G', 'PHEV', '2.0', '2.4'],

    'ASX': ['2WD', '4WD'],

    'Pajero': ['Short Wheel Base', 'Long Wheel Base', 'Exceed', 'GLS'],

    'Pajero Sport': ['Dakar', 'Exceed', 'GLS'],

    'Triton': ['Single Cab', 'Double Cab', '4WD', 'Athlete'],

    'RVR': ['2WD', '4WD'],

    'Eclipse Cross': ['2.0', 'PHEV'],

    'Delica D5': ['G', 'P'],
},

    'Isuzu': {
    'D-Max': ['Single Cab', 'Extended Cab', 'Double Cab', '4WD', 'LS', 'LS-T'],

    'MU-X': ['LS', 'LS-M', 'LS-T', 'Premium'],

    'N-Series': ['NHR', 'NKR', 'NPR', 'NQR', 'Truck'],

    'F-Series': ['FTR', 'FVR', 'FVZ'],

    'Trooper': ['3.1D', '3.0D'],

    'MU-7': ['3.0', '4x4'],
},

    'Daihatsu': {
    'Mira': ['L', 'X', 'Custom'],

    'Move': ['L', 'Custom', 'X', 'RS'],

    'Tanto': ['L', 'Custom', 'RS'],

    'Terios': ['CX', 'TX', '4WD'],

    'Boon': ['CL', 'CX'],

    'Hijet': ['Cargo', 'Truck', 'Van'],

    'Atrai': ['RS', 'Custom'],

    'Cast': ['Style', 'Activa', 'Sport'],

    'Thor': ['Custom', 'Premium'],

    'Wake': ['D', 'L', 'Custom'],

    'Copen': ['Active Top', 'Robe'],
},

   'Peugeot': {
    '108': ['Active', 'Allure'],

    '208': ['Active', 'Allure', 'GT Line', 'e-208'],

    '2008': ['Active', 'Allure', 'GT'],

    '3008': ['Active', 'Allure', 'GT', 'Hybrid'],

    '5008': ['Active', 'Allure', 'GT'],

    '308': ['Active', 'Allure', 'GT Line'],

    '508': ['Allure', 'GT', 'GT Line'],

    'Partner': ['Van', 'Tepee'],

    'Rifter': ['Active', 'Allure'],

    'Expert': ['Van', 'Combi'],

    'Boxer': ['Van', 'L2', 'L3'],

    '3008 Hybrid': ['GT Hybrid'],
},
    'Renault': {
    'Clio': ['Expression', 'Dynamique'],

    'Duster': ['Expression', 'Dynamique', '4WD'],

    'Koleos': ['Zen', 'Intens', 'Initiale Paris'],

    'Captur': ['Zen', 'Intens'],

    'Megane': ['GT Line', 'RS'],

    'Kadjar': ['Zen', 'Intens'],

    'Arkana': ['RS Line'],

    'Trafic': ['Van', 'Passenger'],

    'Master': ['Van', 'L2H2'],

    'Sandero': ['Stepway', 'Essential'],

    'Logan': ['Expression'],
},

    'Jeep': {
    'Wrangler': ['Sport', 'Sahara', 'Rubicon', 'Unlimited'],

    'Grand Cherokee': ['Laredo', 'Limited', 'Overland', 'Summit', 'Trackhawk'],

    'Cherokee': ['Latitude', 'Limited', 'Trailhawk'],

    'Compass': ['Longitude', 'Limited', 'Trailhawk'],

    'Renegade': ['Sport', 'Limited', 'Trailhawk'],

    'Gladiator': ['Sport', 'Rubicon'],
},

   'Porsche': {
    'Macan': ['Base', 'T', 'S', 'GTS', 'Turbo'],

    'Cayenne': ['Base', 'S', 'GTS', 'Turbo', 'Turbo GT'],

    'Panamera': ['4', '4S', 'GTS', 'Turbo', 'Turbo S'],

    '911': ['Carrera', 'Carrera S', 'Turbo', 'Turbo S', 'GT3'],

    'Taycan': ['4S', 'Turbo', 'Turbo S', 'Cross Turismo'],

    'Boxster': ['718', 'S'],

    'Cayman': ['718', 'S'],
},

   'Mini': {
    'Cooper': ['Base', 'S', 'JCW'],

    'Countryman': ['Cooper', 'Cooper S', 'JCW'],

    'Clubman': ['Cooper', 'Cooper S'],

    'Paceman': ['Cooper S'],

    'Convertible': ['Cooper', 'Cooper S'],

    'Electric': ['Cooper SE'],
},

    'Jaguar': {
    'XE': ['Prestige', 'R-Sport', 'S'],

    'XF': ['Prestige', 'Portfolio', 'R-Sport'],

    'XJ': ['Luxury', 'Premium Luxury', 'Autobiography'],

    'F-Pace': ['Prestige', 'R-Dynamic', 'S', 'SVR'],

    'E-Pace': ['SE', 'R-Dynamic'],

    'I-Pace': ['EV400', 'S', 'SE', 'HSE'],

    'F-Type': ['Coupe', 'Convertible', 'R', 'SVR'],
},

    'BYD': {
    'Atto 3': ['Standard Range', 'Extended Range'],

    'Dolphin': ['Active', 'Comfort', 'Premium'],

    'Seal': ['Dynamic', 'Premium', 'Performance'],

    'Han': ['EV', 'DM-i'],

    'Tang': ['EV', 'DM-i'],

    'Song Plus': ['DM-i', 'EV'],

    'Seagull': ['Active', 'Free', 'Flying Edition'],
},

    'Jetour': {
    'X70 Plus': ['Comfort', 'Luxury', 'Premium'],

    'Dashing': ['Comfort', 'Luxury', 'Sport'],

    'X90 Plus': ['Luxury', 'Flagship'],

    'T2': ['Adventure', 'Off-road'],

    'X50': ['Comfort', 'Luxury'],
},

    'Chery': {
    'Tiggo 4 Pro': ['Comfort', 'Luxury'],

    'Tiggo 7 Pro': ['Comfort', 'Luxury', 'Premium'],

    'Tiggo 8 Pro': ['Executive', 'Luxury', 'Max'],

    'Arrizo 5': ['Comfort', 'Luxury'],

    'Arrizo 8': ['Luxury', 'Flagship'],

    'Tiggo 2 Pro': ['Comfort'],

    'Tiggo 9': ['Luxury', 'Hybrid'],
},

    'Haval': {
    'Jolion': ['Premium', 'Luxury', 'Hybrid'],

    'H6': ['Premium', 'Luxury', 'Hybrid'],

    'H2': ['Luxury'],

    'H9': ['Luxury', 'Off-road'],

    'Big Dog': ['Adventure', 'Off-road'],

    'Dargo': ['Luxury', 'Off-road'],
},

    'GWM': {
    'Poer': ['Commercial', 'Passenger', '4WD'],

    'Tank 300': ['Luxury', 'Off-road'],

    'Tank 500': ['Luxury', 'Hybrid'],

    'Wingle': ['Single Cab', 'Double Cab'],

    'Haval H5': ['Diesel', '4WD'],
},

    'Tesla': {
    'Model 3': ['Standard Range', 'Long Range', 'Performance'],

    'Model Y': ['Standard Range', 'Long Range', 'Performance'],

    'Model S': ['Long Range', 'Plaid'],

    'Model X': ['Long Range', 'Plaid'],

    'Cybertruck': ['AWD', 'Cyberbeast'],

    'Roadster': ['2.0'],
},

    'MG': {
    'ZS': ['Comfort', 'Luxury', 'EV'],

    'HS': ['Comfort', 'Luxury', 'Plug-in Hybrid'],

    'MG4': ['Standard', 'Luxury', 'XPower'],

    'MG5': ['Comfort', 'Luxury'],

    'MG ZS EV': ['Standard Range', 'Long Range'],

    'MG Cyberster': ['GT', 'Electric Roadster'],

    'RX5': ['Luxury'],
},

    'Geely': {
        'Coolray': ['Standard', 'Luxury', 'Sport'],
        'Azkarra': ['Hybrid', 'AWD'],
        'Emgrand': ['Comfort', 'Luxury'],
        'Okavango': ['7-Seater', 'Luxury'],
    },

    'Changan': {
        'CS15': ['Comfort'],
        'CS35': ['Comfort', 'Plus'],
        'CS55': ['Plus', 'Luxury'],
        'CS75': ['Plus', 'Premium'],
        'UNI-T': ['Luxury', 'Sport'],
        'UNI-K': ['Luxury'],
        'Alsvin': ['Comfort'],
    },

    'GAC': {
        'GS3': ['Power', 'Luxury'],
        'GS4': ['Luxury', 'Sport'],
        'GS8': ['Luxury', '7-Seater'],
        'GA4': ['Sedan', 'Luxury'],
        'GN6': ['MPV', 'Luxury'],
    },

    'FAW': {
        'Bestune T33': ['Luxury'],
        'Bestune T55': ['Luxury'],
        'Bestune T77': ['Luxury'],
        'V2': ['Truck'],
        'V5': ['Truck'],
    },

    'SsangYong': {
        'Korando': ['2WD', '4WD', 'Diesel'],
        'Rexton': ['Luxury', '7-Seater'],
        'Tivoli': ['Base', 'Luxury'],
        'Musso': ['Double Cab', '4WD'],
    },

    'Fiat': {
        '500': ['Pop', 'Lounge'],
        'Panda': ['Easy', 'Cross'],
        'Tipo': ['Sedan', 'Hatchback'],
        'Doblo': ['Cargo', 'Family'],
        'Fullback': ['Pickup', '4WD'],
    },

    'Opel': {
        'Astra': ['Edition', 'GS Line'],
        'Corsa': ['Base', 'Elegance'],
        'Insignia': ['Grand Sport'],
        'Mokka': ['Elegance', 'GS Line'],
    },

    'RAM': {
        '1500': ['Tradesman', 'Big Horn', 'Laramie', 'Rebel'],
        '2500': ['Heavy Duty'],
        '3500': ['Heavy Duty'],
    },

    'Dodge': {
        'Charger': ['SXT', 'R/T', 'Scat Pack'],
        'Challenger': ['SXT', 'R/T', 'Hellcat'],
        'Durango': ['SXT', 'GT', 'SRT'],
    },

    'Cadillac': {
        'Escalade': ['Luxury', 'Premium Luxury', 'Sport'],
        'XT5': ['Luxury', 'Premium Luxury'],
        'XT6': ['Luxury', 'Sport'],
        'CT5': ['Luxury', 'Sport'],
    },

    'Hino': {
        '300 Series': ['Light Duty Truck'],
        '500 Series': ['Medium Duty Truck'],
        '700 Series': ['Heavy Duty Truck'],
    },

    'Fuso': {
        'Canter': ['Light Duty Truck'],
        'Fighter': ['Medium Duty Truck'],
        'Super Great': ['Heavy Duty Truck'],
    },

    'Lamborghini': {
        'Huracan': ['EVO', 'Tecnica', 'Performante'],
        'Urus': ['S', 'Performante'],
        'Aventador': ['S', 'SVJ'],
        'Revuelto': ['Hybrid V12'],
    },
}

def get_combined_car_hierarchy():
    hierarchy = {
        make: {model: variants.copy() for model, variants in models.items()}
        for make, models in CAR_HIERARCHY.items()
    }
    try:
        for car in Car.objects.all().values('make', 'model', 'variant'):
            make_value = car.get('make') or ''
            model_value = car.get('model') or ''
            variant_value = car.get('variant') or ''
            if not make_value or not model_value:
                continue
            if make_value not in hierarchy:
                hierarchy[make_value] = {}
            if model_value not in hierarchy[make_value]:
                hierarchy[make_value][model_value] = []
            if variant_value and variant_value not in hierarchy[make_value][model_value]:
                hierarchy[make_value][model_value].append(variant_value)
    except Exception:
        pass
    return hierarchy


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'id': 'password-input'
        }),
        help_text='Minimum 8 characters, must include a number or symbol (!@#$%^&*)'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'id': 'password-confirm-input'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if password:
            # Check minimum length
            if len(password) < 8:
                raise forms.ValidationError(
                    "Password must be at least 8 characters long."
                )
            
            # Check for at least one number or symbol
            import re
            if not re.search(r'[0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
                raise forms.ValidationError(
                    "Password must include at least one number or symbol (!@#$%^&*)."
                )
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'profile_picture')
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }




class BuyerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
        }


class DealershipRegistrationForm(forms.ModelForm):
    company_name = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company name (optional - defaults to username)'
        })
    )

    class Meta:
        model = Dealership
        fields = ('company_name', 'description', 'logo', 'website', 'instagram_url', 'facebook_url', 'twitter_url', 'youtube_url', 'linkedin_url', 'tiktok_url', 'email', 
                 'phone_number', 'location', 'area_code', 'address')
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your dealership',
                'rows': 4
            }),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website URL (optional)'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram URL (optional)'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Facebook URL (optional)'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Twitter URL (optional)'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'YouTube URL (optional)'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn URL (optional)'
            }),
            'tiktok_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'TikTok URL (optional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (City/Area)'
            }),
            'area_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area code (e.g., 00100 for Nairobi CBD)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Full street address for precise map location',
                'rows': 4
            }),
        }


class CarForm(forms.ModelForm):
    make = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    model = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    variant = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Variant --')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    exterior_color = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Exterior Color --')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interior_color = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Interior Color --')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    seat_material = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Seat Material --')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interior_trim = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Interior Trim --')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Car
        fields = ('title', 'make', 'model', 'variant', 'year', 'price', 'mileage', 
                 'fuel_type', 'transmission', 'condition', 'color', 'exterior_color', 'interior_color', 'seat_material', 'interior_trim', 'seats',
                 'engine_size', 'doors', 'body_type', 'previous_owners',
                 'description', 'main_image', 'features')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Car title'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price in KES'
            }),
            'mileage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mileage (km)'
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'exterior_color': forms.Select(attrs={'class': 'form-select'}),
            'interior_color': forms.Select(attrs={'class': 'form-select'}),
            'seat_material': forms.Select(attrs={'class': 'form-select'}),
            'interior_trim': forms.Select(attrs={'class': 'form-select'}),
            'seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of seats'
            }),
            'engine_size': forms.Select(attrs={'class': 'form-select'}),
            'doors': forms.Select(attrs={'class': 'form-select'}),
            'body_type': forms.Select(attrs={'class': 'form-select'}),
            'previous_owners': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description',
                'rows': 4
            }),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
            'image4': forms.FileInput(attrs={'class': 'form-control'}),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Features (comma-separated): ABS, Power Steering, AC, etc.',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        make_value = self.data.get('make') or self.initial.get('make') or (instance.make if instance else '')
        model_value = self.data.get('model') or self.initial.get('model') or (instance.model if instance else '')
        variant_value = self.data.get('variant') or self.initial.get('variant') or (instance.variant if instance else '')

        self.fields['make'].choices = self.get_make_choices()
        self.fields['model'].choices = self.get_model_choices(make_value)
        self.fields['variant'].choices = self.get_variant_choices(make_value, model_value)

        self.fields['exterior_color'].choices = [('', '-- Select Exterior Color --')] + CarSearchForm.EXTERIOR_COLOR_CHOICES
        self.fields['interior_color'].choices = [('', '-- Select Interior Color --')] + CarSearchForm.INTERIOR_COLOR_CHOICES
        self.fields['seat_material'].choices = [('', '-- Select Seat Material --')] + CarSearchForm.SEAT_MATERIAL_CHOICES
        self.fields['interior_trim'].choices = [('', '-- Select Interior Trim --')] + CarSearchForm.INTERIOR_TRIM_CHOICES

        if make_value and model_value and variant_value:
            variant_values = [choice[0] for choice in self.fields['variant'].choices]
            if variant_value not in variant_values:
                self.fields['variant'].choices.append((variant_value, variant_value))

    @staticmethod
    def get_make_choices():
        try:
            hierarchy = get_combined_car_hierarchy()
            all_makes = sorted(hierarchy.keys())
        except Exception:
            all_makes = sorted(set(CAR_HIERARCHY.keys()))
        return [('', '-- Select Make --')] + [(make, make) for make in all_makes]

    @staticmethod
    def get_model_choices(make=None):
        if not make:
            return [('', '-- Select Make First --')]

        models = set()
        try:
            hierarchy = get_combined_car_hierarchy()
            models.update(hierarchy.get(make, {}).keys())
        except Exception:
            models.update(CAR_HIERARCHY.get(make, {}).keys())

        return [('', '-- Select Model --')] + [(model, model) for model in sorted(models) if model]

    @staticmethod
    def get_variant_choices(make=None, model=None):
        if not make:
            return [('', '-- Select Make First --')]
        if not model:
            return [('', '-- Select Model First --')]

        variants = []
        try:
            hierarchy = get_combined_car_hierarchy()
            variants = hierarchy.get(make, {}).get(model, [])
        except Exception:
            variants = CAR_HIERARCHY.get(make, {}).get(model, [])
        variants = [v for v in sorted(set(v for v in variants if v))]
        return [('', '-- Select Variant --')] + [(variant, variant) for variant in variants]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '5',
                'step': '0.1',
                'placeholder': '0.0 - 5.0'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review',
                'rows': 4
            }),
        }


class DealershipReviewForm(forms.ModelForm):
    class Meta:
        model = DealershipReview
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '5',
                'step': '0.1',
                'placeholder': '0.0 - 5.0'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review',
                'rows': 4
            }),
        }


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ('buyer_name', 'buyer_email', 'buyer_phone', 'message')
        widgets = {
            'buyer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'buyer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }),
            'buyer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 4
            }),
        }


class EnquiryReplyForm(forms.Form):
    response = forms.CharField(
        label='Response to buyer',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Write your reply to the buyer'
        })
    )


class ConversationMessageForm(forms.Form):
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Type your message here...'
        })
    )


class CarSearchForm(forms.Form):
    @staticmethod
    def get_make_choices():
        try:
            hierarchy = get_combined_car_hierarchy()
            all_makes = sorted(hierarchy.keys())
        except Exception:
            all_makes = sorted(set(CAR_HIERARCHY.keys()))
        return [('', '-- All Makes --')] + [(make, make) for make in all_makes]

    @staticmethod
    def get_model_choices(make=None):
        if not make:
            return [('', '-- Select Make First --')]

        models = set()
        try:
            hierarchy = get_combined_car_hierarchy()
            models.update(hierarchy.get(make, {}).keys())
        except Exception:
            models.update(CAR_HIERARCHY.get(make, {}).keys())

        return [('', '-- All Models --')] + [(model, model) for model in sorted(models) if model]

    @staticmethod
    def get_variant_choices(make=None, model=None):
        if not make:
            return [('', '-- Select Make First --')]
        if not model:
            return [('', '-- Select Model First --')]

        variants = []
        try:
            hierarchy = get_combined_car_hierarchy()
            variants = hierarchy.get(make, {}).get(model, [])
        except Exception:
            variants = CAR_HIERARCHY.get(make, {}).get(model, [])
        variants = [v for v in sorted(set(v for v in variants if v))]
        return [('', '-- All Variants --')] + [(variant, variant) for variant in variants]

    make = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    model = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    variant = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['make'].choices = self.get_make_choices()
        except Exception:
            self.fields['make'].choices = [('', '-- All Makes --')]

        selected_make = self.data.get('make') or self.initial.get('make')
        selected_model = self.data.get('model') or self.initial.get('model')

        self.fields['model'].choices = self.get_model_choices(selected_make)
        self.fields['variant'].choices = self.get_variant_choices(selected_make, selected_model)
 
    current_year = timezone.now().year
 
    YEAR_CHOICES = [('', '--- Year from ---')] + [
        (year, str(year)) for year in range(current_year, 1989, -1)
    ]
 
    year_from = forms.ChoiceField(required=False, choices=YEAR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    YEAR_TO_CHOICES = [('', '--- Year to ---')] + [
        (year, str(year)) for year in range(current_year, 1989, -1)
    ]
 
    year_to = forms.ChoiceField(required=False, choices=YEAR_TO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    PRICE_CHOICES = [
        ('', '--- Price from ---'),
        ('100000', '100,000'),
        ('150000', '150,000'),
        ('200000', '200,000'),
        ('250000', '250,000'),
        ('300000', '300,000'),
        ('350000', '350,000'),
        ('400000', '400,000'),
        ('450000', '450,000'),
        ('500000', '500,000'),
        ('550000', '550,000'),
        ('600000', '600,000'),
        ('650000', '650,000'),
        ('700000', '700,000'),
        ('750000', '750,000'),
        ('800000', '800,000'),
        ('850000', '850,000'),
        ('900000', '900,000'),
        ('950000', '950,000'),
        ('1000000', '1,000,000'),
        ('1500000', '1,500,000'),
        ('2000000', '2,000,000'),
        ('2500000', '2,500,000'),
        ('3000000', '3,000,000'),
        ('3500000', '3,500,000'),
        ('4000000', '4,000,000'),
        ('4500000', '4,500,000'),
        ('5000000', '5,000,000'),
        ('5500000', '5,500,000'),
        ('6000000', '6,000,000'),
        ('6500000', '6,500,000'),
        ('7000000', '7,000,000'),
        ('7500000', '7,500,000'),
        ('8000000', '8,000,000'),
        ('8500000', '8,500,000'),
        ('9000000', '9,000,000'),
        ('9500000', '9,500,000'),
        ('10000000', '10,000,000'),
        ('15000000', '15,000,000'),
        ('20000000', '20,000,000'),
        ('25000000', '25,000,000'),
        ('30000000', '30,000,000'),
        ('35000000', '35,000,000'),
        ('40000000', '40,000,000'),
        ('45000000', '45,000,000'),
        ('50000000', '50,000,000'),
    ]
 
    price_from = forms.ChoiceField(required=False, choices=PRICE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    PRICE_TO_CHOICES = [
        ('', '--- Price to ---'),
        ('150000', '150,000'),
        ('200000', '200,000'),
        ('250000', '250,000'),
        ('300000', '300,000'),
        ('350000', '350,000'),
        ('400000', '400,000'),
        ('450000', '450,000'),
        ('500000', '500,000'),
        ('550000', '550,000'),
        ('600000', '600,000'),
        ('650000', '650,000'),
        ('700000', '700,000'),
        ('750000', '750,000'),
        ('800000', '800,000'),
        ('850000', '850,000'),
        ('900000', '900,000'),
        ('950000', '950,000'),
        ('1000000', '1,000,000'),
        ('1500000', '1,500,000'),
        ('2000000', '2,000,000'),
        ('2500000', '2,500,000'),
        ('3000000', '3,000,000'),
        ('3500000', '3,500,000'),
        ('4000000', '4,000,000'),
        ('4500000', '4,500,000'),
        ('5000000', '5,000,000'),
        ('5500000', '5,500,000'),
        ('6000000', '6,000,000'),
        ('6500000', '6,500,000'),
        ('7000000', '7,000,000'),
        ('7500000', '7,500,000'),
        ('8000000', '8,000,000'),
        ('8500000', '8,500,000'),
        ('9000000', '9,000,000'),
        ('9500000', '9,500,000'),
        ('10000000', '10,000,000'),
        ('15000000', '15,000,000'),
        ('20000000', '20,000,000'),
        ('25000000', '25,000,000'),
        ('30000000', '30,000,000'),
        ('35000000', '35,000,000'),
        ('40000000', '40,000,000'),
        ('45000000', '45,000,000'),
        ('50000000', '50,000,000'),
        ('55000000', '55,000,000'),
        ('60000000', '60,000,000'),
        ('65000000', '65,000,000'),
    ]
 
    price_to = forms.ChoiceField(required=False, choices=PRICE_TO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    MILEAGE_CHOICES = [
        ('', '--- Mileage from ---'),
        ('1000', '1,000 km'),
        ('10000', '10,000 km'),
        ('20000', '20,000 km'),
        ('30000', '30,000 km'),
        ('40000', '40,000 km'),
        ('50000', '50,000 km'),
        ('60000', '60,000 km'),
        ('70000', '70,000 km'),
        ('80000', '80,000 km'),
        ('90000', '90,000 km'),
        ('100000', '100,000 km'),
        ('110000', '110,000 km'),
        ('120000', '120,000 km'),
        ('130000', '130,000 km'),
        ('140000', '140,000 km'),
        ('150000', '150,000 km'),
        ('160000', '160,000 km'),
        ('170000', '170,000 km'),
        ('180000', '180,000 km'),
        ('190000', '190,000 km'),
        ('200000', '200,000 km'),
        ('210000', '210,000 km'),
        ('220000', '220,000 km'),
        ('230000', '230,000 km'),
        ('240000', '240,000 km'),
        ('250000', '250,000 km'),
        ('260000', '260,000 km'),
        ('270000', '270,000 km'),
        ('280000', '280,000 km'),
        ('290000', '290,000 km'),
        ('300000', '300,000 km'),
        ('310000', '310,000 km'),
        ('320000', '320,000 km'),
        ('330000', '330,000 km'),
        ('340000', '340,000 km'),
        ('350000', '350,000 km'),
        ('360000', '360,000 km'),
        ('370000', '370,000 km'),
        ('380000', '380,000 km'),
        ('390000', '390,000 km'),
        ('400000', '400,000 km'),
    ]
 
    MILEAGE_TO_CHOICES = [
        ('', '--- Mileage to ---'),
        ('10000', '10,000 km'),
        ('20000', '20,000 km'),
        ('30000', '30,000 km'),
        ('40000', '40,000 km'),
        ('50000', '50,000 km'),
        ('60000', '60,000 km'),
        ('70000', '70,000 km'),
        ('80000', '80,000 km'),
        ('90000', '90,000 km'),
        ('100000', '100,000 km'),
        ('110000', '110,000 km'),
        ('120000', '120,000 km'),
        ('130000', '130,000 km'),
        ('140000', '140,000 km'),
        ('150000', '150,000 km'),
        ('160000', '160,000 km'),
        ('170000', '170,000 km'),
        ('180000', '180,000 km'),
        ('190000', '190,000 km'),
        ('200000', '200,000 km'),
        ('210000', '210,000 km'),
        ('220000', '220,000 km'),
        ('230000', '230,000 km'),
        ('240000', '240,000 km'),
        ('250000', '250,000 km'),
        ('260000', '260,000 km'),
        ('270000', '270,000 km'),
        ('280000', '280,000 km'),
        ('290000', '290,000 km'),
        ('300000', '300,000 km'),
        ('310000', '310,000 km'),
        ('320000', '320,000 km'),
        ('330000', '330,000 km'),
        ('340000', '340,000 km'),
        ('350000', '350,000 km'),
        ('360000', '360,000 km'),
        ('370000', '370,000 km'),
        ('380000', '380,000 km'),
        ('390000', '390,000 km'),
        ('400000', '400,000 km'),
    ]
 
    mileage_from = forms.ChoiceField(required=False, choices=MILEAGE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    mileage_to = forms.ChoiceField(required=False, choices=MILEAGE_TO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    fuel_type = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Fuel Types --')] + list(Car.FUEL_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    transmission = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Transmissions --')] + list(Car.TRANSMISSION_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    condition = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Conditions --')] + list(Car.CONDITION_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    ENGINE_SIZE_FROM_CHOICES = [('', '--- Engine Size from ---')] + list(Car.ENGINE_SIZE_CHOICES)

    engine_size_from = forms.ChoiceField(required=False, choices=ENGINE_SIZE_FROM_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

    ENGINE_SIZE_TO_CHOICES = [('', '--- Engine Size to ---')] + list(Car.ENGINE_SIZE_CHOICES)

    engine_size_to = forms.ChoiceField(required=False, choices=ENGINE_SIZE_TO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
 
    doors = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Doors --')] + list(Car.DOORS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    body_type = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Body Types --')] + list(Car.BODY_TYPE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    previous_owners = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Owners --')] + list(Car.OWNERS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    seats = forms.ChoiceField(
        required=False,
        choices=[
            ('', '-- All Seats --'),
            ('2', '2 Seats'),
            ('4', '4 Seats'),
            ('5', '5 Seats'),
            ('7', '7 Seats'),
            ('8', '8+ Seats'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    EXTERIOR_COLOR_CHOICES = sorted([
        ('Arctic White', 'Arctic White'),
        ('Black', 'Black'),
        ('Blue', 'Blue'),
        ('Bright Red', 'Bright Red'),
        ('Bronze', 'Bronze'),
        ('Brown', 'Brown'),
        ('Burgundy', 'Burgundy'),
        ('Candy Red', 'Candy Red'),
        ('Champagne Gold', 'Champagne Gold'),
        ('Charcoal Grey', 'Charcoal Grey'),
        ('Cherry Red', 'Cherry Red'),
        ('Chocolate Brown', 'Chocolate Brown'),
        ('Copper', 'Copper'),
        ('Copper Orange', 'Copper Orange'),
        ('Cream', 'Cream'),
        ('Dark Brown', 'Dark Brown'),
        ('Dark Grey', 'Dark Grey'),
        ('Electric Blue', 'Electric Blue'),
        ('Emerald Green', 'Emerald Green'),
        ('Forest Green', 'Forest Green'),
        ('Gold', 'Gold'),
        ('Grey', 'Grey'),
        ('Gunmetal Grey', 'Gunmetal Grey'),
        ('Ivory', 'Ivory'),
        ('Jet Black', 'Jet Black'),
        ('Light Blue', 'Light Blue'),
        ('Light Grey', 'Light Grey'),
        ('Lime Green', 'Lime Green'),
        ('Matte Black', 'Matte Black'),
        ('Matte Blue', 'Matte Blue'),
        ('Matte Green', 'Matte Green'),
        ('Matte Grey', 'Matte Grey'),
        ('Matte Silver', 'Matte Silver'),
        ('Metallic Silver', 'Metallic Silver'),
        ('Midnight Blue', 'Midnight Blue'),
        ('Mocha', 'Mocha'),
        ('Multi-Color', 'Multi-Color'),
        ('Mustard Yellow', 'Mustard Yellow'),
        ('Nardo Grey', 'Nardo Grey'),
        ('Navy Blue', 'Navy Blue'),
        ('Olive Green', 'Olive Green'),
        ('Orange', 'Orange'),
        ('Other', 'Other'),
        ('Pearl White', 'Pearl White'),
        ('Pink', 'Pink'),
        ('Purple', 'Purple'),
        ('Red', 'Red'),
        ('Royal Blue', 'Royal Blue'),
        ('Ruby Red', 'Ruby Red'),
        ('Slate Grey', 'Slate Grey'),
        ('Sky Blue', 'Sky Blue'),
        ('Steel Blue', 'Steel Blue'),
        ('Sunflower Yellow', 'Sunflower Yellow'),
        ('Teal', 'Teal'),
        ('Titanium Silver', 'Titanium Silver'),
        ('Turquoise', 'Turquoise'),
        ('Two-Tone', 'Two-Tone'),
        ('Violet', 'Violet'),
        ('White', 'White'),
        ('Wine Red', 'Wine Red'),
        ('Yellow', 'Yellow'),
    ])
    EXTERIOR_COLOR_CHOICES = [('Other', 'Other')] + [choice for choice in EXTERIOR_COLOR_CHOICES if choice[0] != 'Other']

    exterior_color = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Exterior Colors --')] + EXTERIOR_COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    INTERIOR_COLOR_CHOICES = sorted([
        ('Anthracite', 'Anthracite'),
        ('Beige', 'Beige'),
        ('Black', 'Black'),
        ('Black / Beige', 'Black / Beige'),
        ('Black / Blue', 'Black / Blue'),
        ('Black / Brown', 'Black / Brown'),
        ('Black / Grey', 'Black / Grey'),
        ('Black / Red', 'Black / Red'),
        ('Black / White', 'Black / White'),
        ('Blue', 'Blue'),
        ('Brown', 'Brown'),
        ('Brown / Beige', 'Brown / Beige'),
        ('Burgundy', 'Burgundy'),
        ('Camel', 'Camel'),
        ('Charcoal', 'Charcoal'),
        ('Chocolate Brown', 'Chocolate Brown'),
        ('Cream', 'Cream'),
        ('Dark Brown', 'Dark Brown'),
        ('Dark Grey', 'Dark Grey'),
        ('Espresso Brown', 'Espresso Brown'),
        ('Green', 'Green'),
        ('Grey', 'Grey'),
        ('Ivory', 'Ivory'),
        ('Jet Black', 'Jet Black'),
        ('Light Grey', 'Light Grey'),
        ('Mocha', 'Mocha'),
        ('Navy Blue', 'Navy Blue'),
        ('Orange', 'Orange'),
        ('Other', 'Other'),
        ('Oyster', 'Oyster'),
        ('Red', 'Red'),
        ('Red / Black', 'Red / Black'),
        ('Saddle Tan', 'Saddle Tan'),
        ('Sand Beige', 'Sand Beige'),
        ('Tan', 'Tan'),
        ('Tan / Black', 'Tan / Black'),
        ('Taupe', 'Taupe'),
        ('White', 'White'),
        ('White / Black', 'White / Black'),
    ])
    INTERIOR_COLOR_CHOICES = [('Other', 'Other')] + [choice for choice in INTERIOR_COLOR_CHOICES if choice[0] != 'Other']

    interior_color = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Interior Colors --')] + INTERIOR_COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    SEAT_MATERIAL_CHOICES = sorted([
        ('Alcantara', 'Alcantara'),
        ('Cloth', 'Cloth'),
        ('Fabric', 'Fabric'),
        ('Leather', 'Leather'),
        ('Leatherette', 'Leatherette'),
        ('Mixed Leather / Alcantara', 'Mixed Leather / Alcantara'),
        ('Mixed Leather / Cloth', 'Mixed Leather / Cloth'),
        ('Nappa Leather', 'Nappa Leather'),
        ('Other', 'Other'),
        ('Premium Leather', 'Premium Leather'),
        ('Suede', 'Suede'),
        ('Synthetic Leather', 'Synthetic Leather'),
        ('Velour', 'Velour'),
        ('Vinyl', 'Vinyl'),
    ])
    SEAT_MATERIAL_CHOICES = [('Other', 'Other')] + [choice for choice in SEAT_MATERIAL_CHOICES if choice[0] != 'Other']

    seat_material = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Seat Materials --')] + SEAT_MATERIAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    INTERIOR_TRIM_CHOICES = sorted([
        ('Aluminum', 'Aluminum'),
        ('Brushed Aluminum', 'Brushed Aluminum'),
        ('Carbon Fiber', 'Carbon Fiber'),
        ('Carbon Fiber Look', 'Carbon Fiber Look'),
        ('Chrome', 'Chrome'),
        ('Gloss Wood', 'Gloss Wood'),
        ('Leather Wrapped', 'Leather Wrapped'),
        ('Matte Wood', 'Matte Wood'),
        ('Mixed Materials', 'Mixed Materials'),
        ('Open-Pore Wood', 'Open-Pore Wood'),
        ('Other', 'Other'),
        ('Piano Black', 'Piano Black'),
        ('Satin Chrome', 'Satin Chrome'),
        ('Wood Trim', 'Wood Trim'),
    ])
    INTERIOR_TRIM_CHOICES = [('Other', 'Other')] + [choice for choice in INTERIOR_TRIM_CHOICES if choice[0] != 'Other']

    interior_trim = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Interior Trims --')] + INTERIOR_TRIM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
    color = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Color (e.g., Red, Black, White)'
    }))
 
    features = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Features (e.g., ABS, AC, Power Steering)'
    }))

   

    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 'description')
        widgets = {
            'report_type': forms.Select(choices=Report.REPORT_TYPES),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


# New Forms for Features #5, #6, #7, #8

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ('name', 'make', 'model', 'year_from', 'year_to', 'price_from', 'price_to',
                 'mileage_from', 'mileage_to', 'fuel_type', 'transmission', 'condition', 
                 'color', 'body_type', 'features', 'alert_on_new', 'alert_on_price_drop',
                 'price_drop_percentage')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name your search (e.g., Toyota under 500k)'
            }),
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Make'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'year_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'From year'}),
            'year_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'To year'}),
            'price_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'From price'}),
            'price_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'To price'}),
            'mileage_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'From mileage'}),
            'mileage_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'To mileage'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'body_type': forms.Select(attrs={'class': 'form-select'}),
            'features': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated features'}),
            'alert_on_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alert_on_price_drop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price_drop_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ComparisonForm(forms.Form):
    """Form for adding cars to comparison"""
    car_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        help_text="Comma-separated car IDs"
    )
    
    def clean_car_ids(self):
        car_ids = self.cleaned_data.get('car_ids', '')
        if car_ids:
            return [int(id.strip()) for id in car_ids.split(',') if id.strip().isdigit()]
        return []


class NotificationPreferenceForm(forms.ModelForm):
    
    class Meta:
        model = NotificationPreference
        fields = ('email_on_new_car', 'email_on_price_drop', 'email_on_enquiry_response',
                 'email_on_review_approved', 'email_on_promotions',
                 'sms_on_new_car', 'sms_on_price_drop', 'sms_on_enquiry_response',
                 'sms_phone_number', 'push_on_new_car', 'push_on_price_drop',
                 'push_on_enquiry_response', 'notification_frequency')
        widgets = {
            'email_on_new_car': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_on_price_drop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_on_enquiry_response': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_on_review_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_on_promotions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_on_new_car': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_on_price_drop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_on_enquiry_response': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254712345678'
            }),
            'push_on_new_car': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_on_price_drop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_on_enquiry_response': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_frequency': forms.Select(attrs={'class': 'form-select'}),
        }


