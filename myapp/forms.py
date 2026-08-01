from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Report, 
                     SavedSearch, CarComparison, Notification, NotificationPreference)

CAR_HIERARCHY = {
   'Toyota': {
    'Agya': ['E', 'G', 'GR Sport'],
    'Allex': ['XS150', 'RS180'],
    'Alphard': ['240G', '240S', '250S', '350G', '350S', 'Executive Lounge', 'Hybrid'],
    'Aqua': ['L', 'S', 'G', 'X-Urban', 'GR Sport', 'Hybrid'],
    'Auris': ['150X', '180G', 'RS', 'Hybrid'],
    'Avanza': ['E', 'G', 'S'],
    'Avensis': ['1.8', '2.0', '2.2 D-4D'],
    'Aygo': ['X', 'X-Play', 'X-Cite'],
    'bB': ['S', 'Z', 'ZX Version'],
    'Belta': ['X', 'G'],
    'Blade': ['Master', 'Master G'],
    'bZ4X': ['FWD', 'AWD', 'Limited'],
    'C-HR': ['S', 'G', 'GR Sport', 'Hybrid'],
    'Caldina': ['ZT', 'GT-Four'],
    'Camry': ['GL', 'Grande', 'Atara', 'Ascent', 'SE', 'XLE', 'XSE', 'TRD', 'Hybrid'],
    'Carina': ['Ti', 'GT'],
    'Celica': ['GT', 'GT-Four'],
    'Century': ['Standard', 'SUV'],
    'Corolla': [
        'L', 'LE', 'SE', 'XSE', 'XLE',
        'Axio', 'Fielder', 'NZE',
        'RunX', 'Altis', 'Hybrid',
        'GR Sport'
    ],
    'Corolla Cross': ['L', 'G', 'X', 'Z', 'Hybrid', 'GR Sport'],
    'Corolla Rumion': ['G', 'S'],
    'Corolla Spacio': ['X', 'G'],
    'Corsa': ['EL', 'MOA'],
    'Crown': [
        'Royal Saloon', 'Royal Extra',
        'Athlete', 'Majesta',
        'RS', 'G', 'Hybrid',
        'Crossover', 'Sport', 'Estate', 'Sedan'
    ],
    'Crown Majesta': ['A-Type', 'C-Type'],
    'Dyna': ['Truck', 'Dump', 'Double Cab'],
    'Esquire': ['Xi', 'Gi', 'Hybrid'],
    'Estima': ['Aeras', 'G', 'Hybrid'],
    'FJ Cruiser': ['Base', 'Trail Teams'],
    'Fortuner': ['GX', 'GXL', 'Crusade', 'Legender', 'GR Sport'],
    'GR86': ['RC', 'SZ', 'RZ', 'Premium'],
    'GR Corolla': ['Core', 'Circuit', 'Morizo'],
    'GR Supra': ['2.0', '3.0 Premium', 'A91 Edition'],
    'GR Yaris': ['RC', 'RZ', 'GRMN'],
    'GranAce': ['Premium', 'G'],
    'Granvia': ['Premium', 'VX'],
    'Harrier': [
        'S', 'G', 'Elegance',
        'Premium', 'Progress',
        'Z', 'Hybrid'
    ],
    'Hiace': [
        'DX', 'GL', 'Super GL',
        'Commuter', 'Grand Cabin',
        'High Roof', 'Wide Body'
    ],
    'Hilux': [
        'Single Cab', 'Extra Cab',
        'Double Cab',
        'SR', 'SR5',
        'Invincible',
        'Rogue',
        'GR Sport',
        '2WD', '4WD',
        'Revo'
    ],
    'Highlander': ['LE', 'XLE', 'Limited', 'Platinum', 'Hybrid'],
    'Hilux Surf': ['SSR-X', 'SSR-G'],
    'iQ': ['100G', '130G'],
    'IST': ['150G', '180G'],
    'Kluger': ['GX', 'GXL', 'Grande', 'Hybrid'],
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
    'LiteAce': ['DX', 'GL'],
    'Mark II': ['Grande', 'Tourer V'],
    'Mark X': ['250G', '250S', '300G', '350RDS', 'GRMN'],
    'Mirai': ['XLE', 'Limited'],
    'MR2': ['G-Limited', 'GT'],
    'Noah': ['X', 'G', 'Si', 'S-Z', 'Hybrid'],
    'Passo': ['X', 'G', 'Moda'],
    'Picnic': ['GL'],
    'Porte': ['F', 'G', 'Y'],
    'Premio': ['F', 'X', 'G', 'G Superior', 'EX'],
    'Prius': ['L', 'S', 'A', 'A Touring', 'G', 'Z', 'Hybrid'],
    'Prius Alpha': ['S', 'G', 'Hybrid'],
    'Probox': ['DX', 'DX Comfort', 'GL', 'Hybrid'],
    'Raize': ['X', 'G', 'Z', 'Hybrid'],
    'RAV4': [
        'GX', 'GXL', 'Cruiser',
        'Adventure',
        'Edge',
        'Limited',
        'Hybrid',
        'Prime',
        '4WD'
    ],
    'Ractis': ['X', 'G'],
    'Raum': ['C', 'G'],
    'Rush': ['X', 'G', 'S'],
    'Sequoia': ['SR5', 'Limited', 'Platinum', 'Capstone', 'TRD Pro'],
    'Sienna': ['LE', 'XLE', 'Limited', 'Platinum', 'Hybrid'],
    'Sienta': ['X', 'G', 'Z', 'Hybrid'],
    'Soarer': ['GT', 'GT-T', '430SCV'],
    'Spade': ['F', 'G'],
    'Sprinter': ['SE', 'XE'],
    'Starlet': ['XL', 'GT Turbo', 'Glanza V'],
    'Succeed': ['UL', 'UL-X', 'TX', 'Hybrid'],
    'Supra': ['SZ', 'SZ-R', 'RZ', '3.0'],
    'Tacoma': ['SR', 'SR5', 'TRD Sport', 'TRD Off-Road', 'Limited', 'TRD Pro'],
    'TownAce': ['DX', 'GL'],
    'ToyoAce': ['Truck', 'Double Cab'],
    'Tundra': ['SR', 'SR5', 'Limited', '1794 Edition', 'Platinum', 'Capstone', 'TRD Pro'],
    'Vanguard': ['240S', '350S'],
    'Vellfire': ['2.4Z', '2.5Z', '3.5Z', 'Executive Lounge', 'Hybrid'],
    'Verossa': ['VR25', 'VR25 Turbo'],
    'Vitz': ['B', 'F', 'U', 'RS', 'GR Sport', 'Hybrid'],
    'Voxy': ['X', 'V', 'ZS', 'S-Z', 'Hybrid'],
    'Wish': ['X', 'G', 'S', 'Z'],
    'Yaris': ['L', 'LE', 'SE', 'XLE', 'F', 'Sport', 'GR Sport', 'Hybrid'],
    'Yaris Cross': ['GX', 'GXL', 'Urban', 'Hybrid']
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
    '1 Series': [
        '114i', '116d', '116i', '118d', '118i',
        '120d', '120i', '123d', '125d',
        '125i', '128ti', '130i',
        '135i', 'M135i', 'M140i'
    ],

    '2 Series': [
        '216d', '218d', '218i',
        '220d', '220i',
        '225d', '225e',
        '228i', '230i',
        'M235i', 'M240i'
    ],

    '3 Series': [
        '316d', '316i',
        '318d', '318i',
        '320d', '320i',
        '323i', '325d', '325i',
        '328i', '330d', '330e', '330i',
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
        'A140', 'A150', 'A160', 'A170', 'A180', 'A190', 'A200',
        'A210 Evolution', 'A220', 'A250', 'A250e',
        'A35 AMG', 'A45 AMG', 'A45 S AMG'
    ],

    'B-Class': [
        'B150', 'B160', 'B170', 'B180', 'B200',
        'B200 CDI', 'B220', 'B250', 'B250e'
    ],

    'C-Class': [
        'C160', 'C180', 'C180 Kompressor', 'C200',
        'C200 Kompressor', 'C220d', 'C230',
        'C230 Kompressor', 'C240', 'C250',
        'C250 CGI', 'C250d', 'C280', 'C300',
        'C300e', 'C320', 'C350', 'C350e',
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
        'E450', 'E500', 'E500E',
        'E550', 'E43 AMG', 'E53 AMG',
        'E55 AMG', 'E63 AMG', 'E63 S AMG'
    ],

    'S-Class': [
        'S250 CDI', 'S280', 'S300', 'S300h',
        'S320', 'S350', 'S350 BlueTEC',
        'S400', 'S400d', 'S420',
        'S430', 'S450', 'S450h',
        'S500', 'S500e', 'S550',
        'S560', 'S580', 'S580e',
        'S600', 'S650', 'S680',
        'S63 AMG', 'S65 AMG',
        'Maybach S560', 'Maybach S580', 'Maybach S680'
    ],

    'CLA': [
        'CLA180', 'CLA200', 'CLA220',
        'CLA250', 'CLA250e',
        'CLA35 AMG', 'CLA45 AMG', 'CLA45 S AMG'
    ],

    'CLS': [
        'CLS220d', 'CLS250', 'CLS250 CDI',
        'CLS300', 'CLS350', 'CLS350 CDI',
        'CLS400', 'CLS400d', 'CLS450',
        'CLS500', 'CLS53 AMG',
        'CLS55 AMG', 'CLS63 AMG'
    ],

    'CLE': [
        'CLE200', 'CLE220d', 'CLE300',
        'CLE450', 'CLE53 AMG'
    ],

    'GLA': [
        'GLA180', 'GLA180d', 'GLA200',
        'GLA200d', 'GLA220', 'GLA220d',
        'GLA250', 'GLA250e',
        'GLA35 AMG', 'GLA45 AMG'
    ],

    'GLB': [
        'GLB180', 'GLB200', 'GLB200d',
        'GLB220d', 'GLB250', 'GLB250e',
        'GLB35 AMG'
    ],

    'GLC': [
        'GLC200', 'GLC200d', 'GLC220',
        'GLC220d', 'GLC250', 'GLC250d',
        'GLC300', 'GLC300d', 'GLC300e',
        'GLC350d', 'GLC350e',
        'GLC400', 'GLC400d',
        'GLC43 AMG', 'GLC63 AMG', 'GLC63 S AMG'
    ],

    'GLE': [
        'GLE250d', 'GLE300d', 'GLE350',
        'GLE350d', 'GLE350e',
        'GLE400', 'GLE400d',
        'GLE450', 'GLE500',
        'GLE580', 'GLE53 AMG',
        'GLE43 AMG',
        'GLE63 AMG', 'GLE63 S AMG'
    ],

    'GLS': [
        'GLS350d', 'GLS400d',
        'GLS450', 'GLS500',
        'GLS580', 'GLS600 Maybach',
        'Maybach GLS600',
        'AMG GLS63', 'GLS63 AMG'
    ],

    'G-Class': [
        '230GE', '240GD', '250GD',
        '270 CDI', '280GE',
        '290GD', '300GD', '300GE',
        'G230', 'G250', 'G270',
        'G290', 'G300', 'G320',
        'G350d', 'G400d',
        'G500', 'G500 4x4²',
        'G550', 'G550 4x4²',
        'G650 Landaulet',
        'AMG G55', 'AMG G63', 'AMG G65'
    ],

    'SL': [
        'SL280', 'SL300', 'SL320',
        'SL350', 'SL400', 'SL450',
        'SL500', 'SL550', 'SL600',
        'SL55 AMG', 'SL63 AMG', 'SL65 AMG'
    ],

    'SLC': [
        'SLC180', 'SLC200', 'SLC250',
        'SLC300', 'SLC43 AMG'
    ],

    'SLK': [
        'SLK170', 'SLK200', 'SLK230',
        'SLK250', 'SLK280',
        'SLK300', 'SLK350',
        'SLK32 AMG', 'SLK55 AMG'
    ],

    'CLK': [
        'CLK200', 'CLK200 Kompressor',
        'CLK230 Kompressor', 'CLK240',
        'CLK280', 'CLK320',
        'CLK350', 'CLK430',
        'CLK500', 'CLK55 AMG',
        'CLK63 AMG'
    ],

    'CL-Class': [
        'CL500', 'CL500 4MATIC',
        'CL550', 'CL600',
        'CL63 AMG', 'CL65 AMG'
    ],

    'R-Class': [
        'R280', 'R300', 'R320 CDI',
        'R350', 'R500', 'R63 AMG'
    ],

    'M-Class': [
        'ML230', 'ML250', 'ML270',
        'ML270 CDI', 'ML280',
        'ML280 CDI', 'ML300',
        'ML300 CDI', 'ML320',
        'ML320 CDI', 'ML350',
        'ML350 Bluetec', 'ML400',
        'ML430', 'ML500',
        'ML550', 'ML55 AMG',
        'ML63 AMG'
    ],

    'GL-Class': [
        'GL320', 'GL320 CDI',
        'GL350', 'GL350 Bluetec',
        'GL420 CDI', 'GL450',
        'GL500', 'GL550',
        'GL63 AMG'
    ],

    'GLK': [
        'GLK200', 'GLK220 CDI',
        'GLK250', 'GLK280',
        'GLK300', 'GLK320',
        'GLK350'
    ],

    'EQ Series': [
        'EQA 220', 'EQA 250', 'EQA 250+',
        'EQA 300', 'EQA 350',
        'EQB 250', 'EQB 250+',
        'EQB 300', 'EQB 350',
        'EQC 400',
        'EQE 350', 'EQE 350+',
        'EQE 500', 'EQE 500 SUV',
        'AMG EQE 43', 'AMG EQE 53',
        'EQS 450', 'EQS 450+',
        'EQS 500', 'EQS 580',
        'Maybach EQS 680',
        'AMG EQS 53',
        'AMG EQS SUV 53',
        'EQT', 'eCitan',
        'eVito', 'eSprinter'
    ],

    'AMG GT': [
        'AMG GT', 'AMG GT S',
        'AMG GT C', 'AMG GT R',
        'AMG GT Pro',
        'AMG GT Track Series',
        'AMG GT Black Series',
        'AMG GT 43',
        'AMG GT 53',
        'AMG GT 63',
        'AMG GT 63 S',
        'AMG GT XX'
    ],

    'Citan': [
        '109 CDI', '111 CDI', '112 CDI'
    ],

    'Vaneo': [
        '1.6', '1.7 CDI', '1.9'
    ],

    'Vito': [
        '109 CDI', '110 CDI',
        '111 CDI', '113 CDI',
        '114 CDI', '115 CDI',
        '116 CDI', '119 CDI',
        '120 CDI'
    ],

    'V-Class': [
        'V200d', 'V220d',
        'V250d', 'V300',
        'V300d'
    ],

    'X-Class': [
        'X220d', 'X250d', 'X350d'
    ],

    'Sprinter': [
        '208 CDI', '210 CDI',
        '211 CDI', '212 CDI',
        '213 CDI', '214 CDI',
        '310 CDI', '311 CDI',
        '313 CDI', '314 CDI',
        '315 CDI', '316 CDI',
        '317 CDI', '318 CDI',
        '319 CDI', '411 CDI',
        '413 CDI', '416 CDI',
        '419 CDI', '511 CDI',
        '515 CDI', '516 CDI',
        '517 CDI', '519 CDI',
        '519 BlueTEC'
    ],

    'T-Class': [
        'T160', 'T180'
    ]
},


   'Audi': {
    'A1': [
        '25 TFSI', '30 TFSI', '35 TFSI',
        'Sportback', 'Citycarver', 'Allstreet'
    ],

    'A3': [
        '1.4 TFSI', '1.5 TFSI', '1.6 TDI',
        '2.0 TDI', '30 TFSI', '30 TDI',
        '35 TFSI', '35 TDI',
        '40 TFSI', '40 TFSI e',
        '45 TFSI e',
        'S3', 'RS3'
    ],

    'A4': [
        '1.8 TFSI', '2.0 TFSI', '2.0 TDI',
        '30 TFSI', '35 TFSI', '35 TDI',
        '40 TFSI', '40 TDI',
        '45 TFSI', '45 TDI',
        'S4', 'RS4'
    ],

    'A5': [
        '35 TFSI', '40 TFSI', '40 TDI',
        '45 TFSI', '45 TDI',
        'S5', 'RS5'
    ],

    'A6': [
        '35 TFSI', '40 TFSI', '40 TDI',
        '45 TFSI', '45 TDI',
        '50 TDI', '55 TFSI',
        '55 TFSI e',
        'S6', 'RS6'
    ],

    'A7': [
        '45 TFSI', '50 TDI',
        '55 TFSI', '55 TFSI e',
        'S7', 'RS7'
    ],

    'A8': [
        '50 TDI',
        '55 TFSI',
        '60 TFSI',
        'L',
        'L Horch',
        'S8'
    ],

    'Q2': [
        '30 TFSI',
        '35 TFSI',
        '35 TDI',
        '40 TFSI',
        'SQ2'
    ],

    'Q3': [
        '30 TFSI',
        '35 TFSI',
        '35 TDI',
        '40 TFSI',
        '40 TDI',
        '45 TFSI',
        '45 TFSI e',
        'RS Q3',
        'RS Q3 Sportback'
    ],

    'Q4 e-tron': [
        '35 e-tron',
        '40 e-tron',
        '45 e-tron',
        '50 e-tron Quattro',
        'Sportback'
    ],

    'Q5': [
        '35 TDI',
        '40 TDI',
        '40 TFSI',
        '45 TDI',
        '45 TFSI',
        '50 TDI',
        '50 TFSI e',
        '55 TFSI e',
        'SQ5'
    ],

    'Q6 e-tron': [
        'Performance',
        'Quattro',
        'SQ6 e-tron'
    ],

    'Q7': [
        '45 TDI',
        '45 TFSI',
        '50 TDI',
        '55 TFSI',
        '60 TFSI',
        'SQ7'
    ],

    'Q8': [
        '50 TDI',
        '55 TFSI',
        '60 TFSI',
        '55 TFSI e',
        'SQ8',
        'RS Q8',
        'RS Q8 Performance'
    ],

    'TT': [
        '40 TFSI',
        '45 TFSI',
        'TTS',
        'TT RS'
    ],

    'R8': [
        'V10',
        'V10 Performance',
        'GT'
    ],

    'e-tron': [
        '50 Quattro',
        '55 Quattro',
        'S e-tron',
        'Sportback',
        'GT',
        'RS e-tron GT'
    ],

    'RS Models': [
        'RS3',
        'RS4',
        'RS5',
        'RS6',
        'RS7',
        'RS Q3',
        'RS Q3 Sportback',
        'RS Q8',
        'RS Q8 Performance',
        'RS e-tron GT'
    ],

    'S Models': [
        'S1',
        'S3',
        'S4',
        'S5',
        'S6',
        'S7',
        'S8',
        'SQ2',
        'SQ5',
        'SQ6 e-tron',
        'SQ7',
        'SQ8',
        'TTS'
    ]
},

  'Lexus': {
    'CT': [
        '200h', '200h F Sport'
    ],

    'HS': [
        '250h'
    ],

    'IS': [
        '200', '200t',
        '250', '250 AWD',
        '300', '300 AWD',
        '300h',
        '350', '350 AWD',
        '500',
        'F Sport',
        'IS F',
        'IS 500 F Sport Performance'
    ],

    'ES': [
        '200',
        '250',
        '250 AWD',
        '250h',
        '300h',
        '330',
        '350',
        '350 F Sport'
    ],

    'GS': [
        '200t',
        '250',
        '300',
        '300 AWD',
        '350',
        '350 AWD',
        '450h',
        'F Sport',
        'GS F'
    ],

    'LS': [
        '400',
        '430',
        '460',
        '460L',
        '500',
        '500 AWD',
        '500h',
        '600h',
        'LS 500',
        'LS 500h',
        'F Sport',
        'Executive'
    ],

    'UX': [
        '200',
        '200 AWD',
        '250h',
        '250h AWD',
        '300e',
        'F Sport'
    ],

    'NX': [
        '200',
        '200t',
        '250',
        '300',
        '300h',
        '350',
        '350 F Sport',
        '350h',
        '450h+',
        'F Sport'
    ],

    'RX': [
        '200t',
        '270',
        '300',
        '330',
        '350',
        '350L',
        '350h',
        '400h',
        '450h',
        '450h+',
        '500h F Sport Performance',
        'F Sport'
    ],

    'GX': [
        '460',
        '470',
        '550',
        '550 Premium',
        '550 Luxury',
        '550 Overtrail',
        '550 Overtrail+'
    ],

    'LX': [
        '450',
        '450d',
        '470',
        '570',
        '600',
        '600 F Sport',
        '600 VIP'
    ],

    'RC': [
        '200t',
        '300',
        '300 AWD',
        '300h',
        '350',
        '350 AWD',
        'F Sport',
        'RC F',
        'RC F Track Edition'
    ],

    'LC': [
        '500',
        '500 Convertible',
        '500h',
        'LC 500',
        'LC 500h',
        'LC Inspiration Series'
    ],

    'LM': [
        '300h',
        '350',
        '500h',
        'Executive',
        'VIP'
    ],

    'LBX': [
        'Elegant',
        'Relax',
        'Cool',
        'Hybrid'
    ],

    'RZ': [
        '300e',
        '450e',
        '550e F Sport'
    ],

    'SC': [
        '300',
        '400',
        '430'
    ],

    'LFA': [
        'Standard',
        'Nürburgring Package'
    ],

    'F Models': [
        'IS F',
        'GS F',
        'RC F',
        'RC F Track Edition',
        'LFA'
    ]
},

  'Volkswagen': {
    'Golf': [
        '1.2 TSI', '1.4 TSI', '1.5 TSI',
        '1.6 TDI', '2.0 TDI',
        'TSI', 'TDI',
        'Trendline', 'Comfortline',
        'Highline',
        'GTD', 'GTI', 'GTE',
        'GTI Clubsport',
        'GTI TCR',
        'R', 'R32'
    ],

    'Polo': [
        '1.0 MPI',
        '1.0 TSI',
        '1.2 TSI',
        '1.4 TDI',
        'TSI',
        'Comfortline',
        'Trendline',
        'Highline',
        'Life',
        'Style',
        'R-Line',
        'GTI'
    ],

    'Passat': [
        '1.4 TSI',
        '1.5 TSI',
        '2.0 TSI',
        '2.0 TDI',
        'TSI',
        'TDI',
        'Comfortline',
        'Highline',
        'Business',
        'Executive',
        'Elegance',
        'R-Line',
        'GTE',
        'Alltrack'
    ],

    'Jetta': [
        '1.4 TSI',
        '1.5 TSI',
        '2.0 TSI',
        'TSI',
        'Trendline',
        'Comfortline',
        'Highline',
        'GLI'
    ],

    'Arteon': [
        'TSI',
        'TDI',
        'Elegance',
        'R-Line',
        'Shooting Brake'
    ],

    'Beetle': [
        '1.2 TSI',
        '1.4 TSI',
        '2.0 TSI',
        'Design',
        'Sport',
        'R-Line',
        'Dune'
    ],

    'Scirocco': [
        'TSI',
        'TDI',
        'R'
    ],

    'CC': [
        'TSI',
        'TDI',
        'R-Line'
    ],

    'Virtus': [
        'Comfortline',
        'Highline',
        'GT'
    ],

    'Tiguan': [
        '1.4 TSI',
        '2.0 TSI',
        '2.0 TDI',
        'TSI',
        'TDI',
        'Life',
        'Elegance',
        'R-Line',
        '4Motion',
        'Allspace',
        'Tiguan R'
    ],

    'Touareg': [
        'V6 TDI',
        'V6 TSI',
        'V8 TDI',
        'Elegance',
        'R-Line'
    ],

    'Taos': [
        'Life',
        'Comfortline',
        'Highline'
    ],

    'T-Cross': [
        'TSI',
        'Life',
        'Style',
        'R-Line'
    ],

    'T-Roc': [
        'TSI',
        'Life',
        'Style',
        'R-Line',
        'R'
    ],

    'Taigo': [
        'TSI',
        'Life',
        'Style',
        'R-Line'
    ],

    'Atlas': [
        'SE',
        'SEL',
        'SEL Premium'
    ],

    'Atlas Cross Sport': [
        'SE',
        'SEL',
        'R-Line'
    ],

    'Amarok': [
        'TDI',
        'V6 TDI',
        'Life',
        'Style',
        'PanAmericana',
        'Aventura'
    ],

    'Caddy': [
        'Cargo',
        'Panel Van',
        'Life',
        'Maxi',
        'California'
    ],

    'Touran': [
        'TSI',
        'TDI',
        'Comfortline',
        'Highline'
    ],

    'Sharan': [
        'TSI',
        'TDI',
        'Comfortline',
        'Highline'
    ],

    'Transporter': [
        'T4',
        'T5',
        'T6',
        'T6.1',
        'Panel Van',
        'Crew Van'
    ],

    'Caravelle': [
        'T5',
        'T6',
        'T6.1',
        'Comfortline',
        'Highline'
    ],

    'Multivan': [
        'Comfortline',
        'Highline',
        'Style',
        'Life'
    ],

    'Crafter': [
        'Panel Van',
        'Chassis Cab',
        'LWB',
        'MWB'
    ],

    'California': [
        'Beach',
        'Coast',
        'Ocean'
    ],

    'Up!': [
        'Move Up!',
        'High Up!',
        'GTI'
    ],

    'Fox': [
        'Trendline'
    ],

    'Lupo': [
        'Sport',
        'GTI'
    ],

    'Vento': [
        'Comfortline',
        'Highline'
    ],

    'Bora': [
        'Trendline',
        'Highline'
    ],

    'ID.3': [
        'Pure',
        'Pro',
        'Pro S',
        'GTX'
    ],

    'ID.4': [
        'Pure',
        'Pro',
        'Pro Performance',
        'GTX'
    ],

    'ID.5': [
        'Pro',
        'Pro Performance',
        'GTX'
    ],

    'ID.6': [
        'Pure',
        'Pro',
        'Prime'
    ],

    'ID.7': [
        'Pro',
        'Pro S',
        'GTX'
    ],

    'ID.Buzz': [
        'Cargo',
        'Pro',
        'LWB',
        'GTX'
    ]
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
    'March': [
        'S', 'X', 'G', '12X', '12S',
        'Bolero', 'NISMO'
    ],

    'Micra': [
        'Visia', 'Acenta', 'Tekna',
        'N-Connecta', 'Base'
    ],

    'Note': [
        'S', 'X', 'G',
        'Medalist',
        'e-Power',
        'e-Power X',
        'e-Power Medalist',
        'Autech',
        'NISMO'
    ],

    'Note Aura': [
        'G',
        'e-Power',
        'NISMO'
    ],

    'Tiida': [
        '15M',
        '18G',
        'Axis',
        'Latio'
    ],

    'Latio': [
        'S',
        'X',
        'G'
    ],

    'Sunny': [
        'EX',
        'EX Saloon',
        'Super Saloon',
        'XL',
        'XV'
    ],

    'Bluebird Sylphy': [
        '15S',
        '20M',
        'G',
        'X',
        'Axis'
    ],

    'Almera': [
        'S',
        'SV',
        'VL',
        'NISMO'
    ],

    'Sylphy': [
        'S',
        'SV',
        'Exclusive'
    ],

    'Sentra': [
        'S',
        'SV',
        'SR',
        'SR Turbo',
        'NISMO'
    ],

    'Juke': [
        'S',
        'SV',
        'SL',
        'Tekna',
        'NISMO RS'
    ],

    'Kicks': [
        'S',
        'SV',
        'SR',
        'X',
        'e-Power',
        'Autech'
    ],

    'Qashqai': [
        'Visia',
        'Acenta',
        'N-Connecta',
        'Tekna',
        '2WD',
        '4WD',
        'e-Power'
    ],

    'X-Trail': [
        '20S',
        '20X',
        '20Xi',
        '25X',
        'ST',
        'Ti',
        'Hybrid',
        'e-Power',
        '4WD',
        'Autech',
        'N-Trek'
    ],

    'Murano': [
        'S',
        'SV',
        'SL',
        'Platinum',
        'XV'
    ],

    'Pathfinder': [
        'S',
        'SE',
        'SV',
        'SL',
        'LE',
        'Platinum',
        'Rock Creek'
    ],

    'Terrano': [
        'XE',
        'XL',
        'XV',
        'Sport',
        '2.0',
        '4WD'
    ],

    'Patrol': [
        'Y60',
        'Y61',
        'Y62',
        'XE',
        'SE',
        'LE',
        'Titanium',
        'Platinum',
        'NISMO'
    ],

    'Armada': [
        'SV',
        'SL',
        'Platinum',
        'Platinum Reserve'
    ],

    'Navara': [
        'Single Cab',
        'King Cab',
        'Double Cab',
        'XE',
        'SE',
        'LE',
        'ST',
        'ST-X',
        'SL',
        'PRO-4X',
        'Warrior',
        '2WD',
        '4WD'
    ],

    'Hardbody': [
        'Single Cab',
        'Double Cab'
    ],

    'Frontier': [
        'S',
        'SV',
        'PRO-4X',
        'SL'
    ],

    'Serena': [
        'X',
        'G',
        'Highway Star',
        'Highway Star V',
        'S-Hybrid',
        'e-Power',
        'Autech'
    ],

    'Elgrand': [
        '250 Highway Star',
        '250 XG',
        '350 Highway Star',
        '350 VIP',
        'Rider'
    ],

    'Caravan': [
        'DX',
        'GX',
        'Premium GX',
        'NV350'
    ],

    'NV200': [
        'Vanette',
        'DX',
        'GX',
        'Cargo'
    ],

    'NV350': [
        'DX',
        'GX',
        'Premium GX'
    ],

    'Urvan': [
        'DX',
        'GX',
        '15-Seater'
    ],

    'Dayz': [
        'S',
        'X',
        'Highway Star',
        'Highway Star G'
    ],

    'Roox': [
        'S',
        'Highway Star'
    ],

    'Cube': [
        '15X',
        '15G',
        'Rider'
    ],

    'Wingroad': [
        '15M',
        '18RX',
        'Axis'
    ],

    'AD Van': [
        'DX',
        'VE'
    ],

    'Fuga': [
        '250GT',
        '370GT',
        'Hybrid'
    ],

    'Cima': [
        'Hybrid',
        'VIP'
    ],

    'Skyline': [
        '200GT',
        '250GT',
        '350GT',
        '370GT',
        '400R',
        'GT-R'
    ],

    'GT-R': [
        'Pure',
        'Premium',
        'Track Edition',
        'NISMO',
        'T-spec'
    ],

    '370Z': [
        'Base',
        'Sport',
        'NISMO'
    ],

    '350Z': [
        'Base',
        'Touring',
        'Track'
    ],

    'Z': [
        'Sport',
        'Performance',
        'NISMO'
    ],

    'Leaf': [
        'S',
        'SV',
        'SV Plus',
        'SL',
        'SL Plus',
        'e+'
    ],

    'Ariya': [
        'Engage',
        'Venture+',
        'Evolve',
        'Empower+',
        'Platinum+',
        'e-4ORCE'
    ],

    'Sakura': [
        'X',
        'G'
    ]
},

   'Mazda': {
    'Demio': [
        '13C', '13S', '13S Touring',
        '15C', '15S', '15S Touring',
        'XD', 'XD Touring',
        'SKYACTIV',
        'Sport'
    ],

    'Mazda2': [
        'Pure',
        'Evolve',
        'GT',
        '15S',
        'Hybrid',
        'Skyactiv-G',
        'Skyactiv-X'
    ],

    'Axela': [
        '15C',
        '15S',
        '20C',
        '20S',
        '22XD',
        'Hybrid'
    ],

    'Mazda3': [
        'Base',
        'Select',
        'Preferred',
        'Premium',
        'Premium Plus',
        '15S',
        '20S',
        '25S',
        '2.0',
        '2.5',
        'Turbo',
        'Skyactiv-G',
        'Skyactiv-D',
        'Skyactiv-X'
    ],

    'Atenza': [
        '20S',
        '25S',
        'XD',
        'XD L Package'
    ],

    'Mazda6': [
        'Sport',
        'Touring',
        'Grand Touring',
        'Signature',
        '20S',
        '25S',
        '2.2D',
        'Diesel',
        'Turbo',
        'Skyactiv-G'
    ],

    'CX-3': [
        '15S',
        '20S',
        'XD',
        'Touring',
        'GT',
        'Skyactiv-G',
        'Skyactiv-D'
    ],

    'CX-30': [
        '20S',
        '25S',
        'GT',
        'Touring',
        'Turbo',
        'Skyactiv-G',
        'Skyactiv-X'
    ],

    'CX-5': [
        'Sport',
        'Touring',
        'Carbon Edition',
        'Grand Touring',
        'Grand Touring Reserve',
        'Signature',
        '20S',
        '25S',
        '25T',
        '2.2D',
        'Turbo',
        'Skyactiv-G',
        'Skyactiv-D'
    ],

    'CX-50': [
        '2.5 S',
        'Preferred',
        'Premium',
        'Premium Plus',
        'Turbo',
        'Turbo Meridian',
        'Turbo Premium',
        'Turbo Premium Plus'
    ],

    'CX-7': [
        'Classic',
        'Luxury',
        '2.3 Turbo'
    ],

    'CX-8': [
        '25S',
        '25T',
        '2.2D',
        'Touring',
        'Asaki'
    ],

    'CX-9': [
        'Sport',
        'Touring',
        'GT',
        'Azami',
        '25T',
        '2.5T'
    ],

    'CX-60': [
        'Pure',
        'Evolve',
        'GT',
        'Azami',
        'PHEV',
        'Diesel',
        'Inline-6 Diesel'
    ],

    'CX-70': [
        'Turbo',
        'Turbo S',
        'PHEV'
    ],

    'CX-80': [
        'PHEV',
        'Diesel'
    ],

    'CX-90': [
        'Turbo',
        'Turbo S',
        'PHEV'
    ],

    'MX-5': [
        'Soft Top',
        'RF',
        'Sport',
        'Club',
        'Grand Touring'
    ],

    'MX-30': [
        'EV',
        'e-Skyactiv',
        'R-EV'
    ],

    'RX-7': [
        'Type R',
        'Spirit R'
    ],

    'RX-8': [
        'Type S',
        'Type E',
        'Spirit R'
    ],

    'BT-50': [
        'Single Cab',
        'Freestyle Cab',
        'Double Cab',
        'XT',
        'XTR',
        'GT',
        'SP',
        '3.0D',
        '3.2D'
    ],

    'B-Series': [
        'B2200',
        'B2500',
        'B2600',
        'B3000',
        'B4000'
    ],

    'Bongo': [
        'Van',
        'Truck',
        'Brawny'
    ],

    'Scrum': [
        'Van',
        'Truck',
        'Wagon'
    ],

    'Flair': [
        'XG',
        'XS',
        'Hybrid'
    ],

    'Flair Wagon': [
        'XS',
        'XT',
        'Hybrid'
    ],

    'Carol': [
        'GX',
        'GL',
        'Hybrid'
    ],

    'Premacy': [
        '20S',
        '20C'
    ],

    'Verisa': [
        'C',
        'L'
    ],

    'Tribute': [
        'Luxury',
        'Classic'
    ],

    'Proceed': [
        'Marvie'
    ]
},

  'Subaru': {
    'Impreza': [
        '1.5i',
        '1.6i',
        '2.0i',
        '2.0i-L',
        '2.0i-S',
        '2.0R',
        'WRX',
        'WRX STI',
        'STI Sport'
    ],

    'Legacy': [
        '2.0i',
        '2.5i',
        '2.5GT',
        '3.0R',
        '3.6R',
        'GT',
        'Premium',
        'Limited',
        'Touring XT'
    ],

    'Legacy B4': [
        '2.0GT',
        '2.0GT Spec.B',
        '2.5GT',
        '2.5GT tS',
        'RS'
    ],

    'Outback': [
        '2.5i',
        '2.5XT',
        '2.4 XT',
        '3.0R',
        '3.6R',
        'Premium',
        'Limited',
        'Touring',
        'Wilderness'
    ],

    'Forester': [
        '2.0i',
        '2.0XT',
        '2.5i',
        '2.5XT',
        'e-Boxer',
        'Hybrid',
        'Premium',
        'Sport',
        'Advance',
        'Limited',
        'Touring',
        'Wilderness',
        'STI Sport'
    ],

    'XV': [
        '1.6i',
        '2.0i',
        '2.0i-L',
        '2.0i-S',
        '2.0e-Boxer',
        'Hybrid',
        'Premium',
        'Advance'
    ],

    'Crosstrek': [
        '2.0i',
        '2.5i',
        'Premium',
        'Sport',
        'Limited',
        'Wilderness',
        'Hybrid'
    ],

    'WRX': [
        'Base',
        'Premium',
        'Limited',
        'GT',
        'Turbo',
        'S4',
        'STI',
        'STI Spec C',
        'STI Type RA',
        'STI tS',
        'TS'
    ],

    'Levorg': [
        '1.6GT',
        '1.6GT EyeSight',
        '2.0GT',
        '2.0STI Sport',
        'GT-H',
        'STI Sport'
    ],

    'Exiga': [
        '2.0i',
        '2.0GT',
        '2.5i',
        'GT',
        'EyeSight'
    ],

    'BRZ': [
        'RA',
        'R',
        'S',
        'STI Sport',
        'tS'
    ],

    'Tribeca': [
        '3.0R',
        '3.6R',
        'Limited'
    ],

    'Ascent': [
        'Base',
        'Premium',
        'Onyx Edition',
        'Limited',
        'Touring'
    ],

    'Solterra': [
        'Premium',
        'Limited',
        'Touring'
    ],

    'Justy': [
        '1.0i',
        '1.2',
        '4WD'
    ],

    'Sambar': [
        'Truck',
        'Van',
        'Dias Wagon'
    ],

    'Pleo': [
        'L',
        'F',
        'RS',
        'Custom'
    ],

    'Stella': [
        'L',
        'G',
        'Custom',
        'Custom RS'
    ],

    'Rex': [
        'Z',
        'G'
    ],

    'R1': [
        'R',
        'S'
    ],

    'R2': [
        'F',
        'R',
        'S'
    ],

    'Dex': [
        '1.3i'
    ],

    'Domingo': [
        'GV',
        'Aladdin'
    ],

    'Vivio': [
        'RX-R',
        'Bistro'
    ],

    'Leone': [
        'GL',
        'RX'
    ],

    'SVX': [
        'Version L',
        'Version S'
    ],

    'Alcyone': [
        'SVX'
    ]
},

   'Volvo': {
    'S40': [
        '1.6', '1.8', '2.0',
        '2.4', '2.4i', 'T4', 'T5'
    ],

    'S60': [
        'T3', 'T4', 'T5', 'T6', 'T8',
        'B4', 'B5', 'B6',
        'Recharge',
        'Polestar Engineered',
        'Momentum',
        'Inscription',
        'R-Design',
        'Ultimate'
    ],

    'S80': [
        '2.0', '2.5T', '3.0',
        '3.2', 'T6',
        'D4', 'D5',
        'Executive'
    ],

    'S90': [
        'T5', 'T6', 'T8',
        'B5', 'B6',
        'Recharge',
        'Momentum',
        'Inscription',
        'R-Design',
        'Ultimate'
    ],

    'V40': [
        'D2', 'D3', 'D4',
        'T2', 'T3', 'T4', 'T5',
        'Cross Country',
        'R-Design'
    ],

    'V50': [
        '1.8', '2.0', '2.4i',
        'T5'
    ],

    'V60': [
        'T4', 'T5', 'T6', 'T8',
        'B4', 'B5',
        'Recharge',
        'Cross Country',
        'Polestar Engineered',
        'Momentum',
        'Ultimate'
    ],

    'V70': [
        '2.0', '2.5T',
        '3.2', 'D5'
    ],

    'V90': [
        'B5', 'B6',
        'T6', 'T8',
        'Recharge',
        'Cross Country',
        'Ultimate'
    ],

    'XC40': [
        'T2', 'T3', 'T4', 'T5',
        'B3', 'B4',
        'Recharge',
        'Pure Electric',
        'Ultimate'
    ],

    'XC60': [
        'T5', 'T6', 'T8',
        'B5', 'B6',
        'Recharge',
        'Momentum',
        'Inscription',
        'R-Design',
        'Ultimate',
        'Polestar Engineered'
    ],

    'XC70': [
        '2.5T',
        '3.2',
        'D5'
    ],

    'XC90': [
        'T5', 'T6', 'T8',
        'B5', 'B6',
        'Recharge',
        'Momentum',
        'Inscription',
        'R-Design',
        'Excellence',
        'Ultimate'
    ],

    'EX30': [
        'Single Motor',
        'Single Motor Extended Range',
        'Twin Motor Performance'
    ],

    'EX40': [
        'Single Motor',
        'Twin Motor'
    ],

    'EX90': [
        'Twin Motor',
        'Twin Motor Performance'
    ],

    'EC40': [
        'Single Motor',
        'Twin Motor'
    ],

    'C40': [
        'Recharge',
        'Single Motor',
        'Twin Motor'
    ],

    'C30': [
        '1.6', '2.0',
        'T5', 'R-Design'
    ],

    'C70': [
        '2.4i',
        'T5'
    ],

    '240': [
        'GL',
        'GLE'
    ],

    '850': [
        'GLT',
        'Turbo',
        'T5-R',
        'R'
    ]
},

'Land Rover / Range Rover': {
    'Defender': [
        '90',
        '110',
        '130',
        'S',
        'SE',
        'X-Dynamic SE',
        'X-Dynamic HSE',
        'HSE',
        'X',
        'V8',
        'OCTA'
    ],

    'Discovery': [
        'Series I',
        'Series II',
        '3',
        '4',
        '5',
        'S',
        'SE',
        'HSE',
        'Metropolitan'
    ],

    'Discovery Sport': [
        'S',
        'SE',
        'HSE',
        'R-Dynamic S',
        'R-Dynamic SE',
        'R-Dynamic HSE',
        'Metropolitan'
    ],

    'Range Rover': [
        'SE',
        'HSE',
        'Vogue',
        'Westminster',
        'Autobiography',
        'First Edition',
        'SV',
        'SV Autobiography',
        'SV Carmel Edition'
    ],

    'Range Rover Sport': [
        'S',
        'SE',
        'HSE',
        'HSE Dynamic',
        'Dynamic SE',
        'Dynamic HSE',
        'Autobiography',
        'SVR',
        'SV'
    ],

    'Range Rover Velar': [
        'S',
        'Dynamic SE',
        'Dynamic HSE',
        'R-Dynamic S',
        'R-Dynamic SE',
        'R-Dynamic HSE',
        'Autobiography'
    ],

    'Range Rover Evoque': [
        'S',
        'SE',
        'HSE',
        'Autobiography',
        'R-Dynamic S',
        'R-Dynamic SE',
        'R-Dynamic HSE'
    ],

    'Freelander': [
        '1',
        '2',
        'S',
        'SE',
        'HSE'
    ],

    'Discovery Vision': [
        'Concept'
    ],

    'Classic Range Rover': [
        '3.0',
        '3.5 V8',
        '3.9 V8',
        '4.2 LSE',
        '4.4 V8'
    ],

    'Range Rover Classic': [
        '2-Door',
        '4-Door'
    ]
},
    'Suzuki': {
    'Alto': [
        'Base',
        'L',
        'F',
        'S',
        'VXL',
        'Works',
        'Turbo RS',
        'Hybrid X',
        'Hybrid S'
    ],

    'Alto Lapin': [
        'L',
        'X',
        'Mode'
    ],

    'Swift': [
        'GA',
        'GL',
        'GL+',
        'GLX',
        'GX',
        'RS',
        'RS Hybrid',
        'Sport',
        'Sport Hybrid',
        'Hybrid MX',
        'Hybrid MZ'
    ],

    'Baleno': [
        'GL',
        'GLX',
        'Sigma',
        'Delta',
        'Zeta',
        'Alpha'
    ],

    'Celerio': [
        'Base',
        'GA',
        'GL',
        'GX',
        'ZXI',
        'VXI'
    ],

    'Dzire': [
        'GL',
        'GL+',
        'GLX',
        'LXi',
        'VXi',
        'ZXi',
        'ZXi+'
    ],

    'Jimny': [
        'JL',
        'JLX',
        'GL',
        'GLX',
        'Sierra',
        'XC',
        'XL',
        '5-Door'
    ],

    'Vitara': [
        'GL',
        'GL+',
        'GLX',
        'JLX',
        'SZ-T',
        'SZ5',
        'Hybrid'
    ],

    'Grand Vitara': [
        'JX',
        'LX',
        'GL',
        'GLX',
        'Sigma',
        'Delta',
        'Zeta',
        'Alpha',
        'Strong Hybrid',
        'AllGrip'
    ],

    'Escudo': [
        'XG',
        'XL',
        'Helly Hansen',
        'Nomade'
    ],

    'S-Cross': [
        'GL',
        'GL+',
        'GLX',
        'Motion',
        'Ultra',
        'Hybrid'
    ],

    'Ignis': [
        'GL',
        'GLX',
        'GX',
        'Hybrid MX',
        'Hybrid MZ'
    ],

    'Fronx': [
        'Sigma',
        'Delta',
        'Zeta',
        'Alpha',
        'Hybrid'
    ],

    'XL7': [
        'GLX',
        'Alpha',
        'Hybrid'
    ],

    'Ertiga': [
        'GA',
        'GL',
        'GLX',
        'GX',
        'Sport',
        'Hybrid'
    ],

    'APV': [
        'GA',
        'GLX',
        'Arena'
    ],

    'Carry': [
        'Pickup',
        'Truck',
        'Van'
    ],

    'Super Carry': [
        'Standard',
        'X'
    ],

    'Wagon R': [
        'FX',
        'FX-S',
        'FX Limited',
        'Stingray',
        'Hybrid FX',
        'Hybrid FZ'
    ],

    'Every': [
        'PA',
        'PC',
        'Join',
        'Join Turbo',
        'Van',
        'Wagon'
    ],

    'Spacia': [
        'Hybrid G',
        'Hybrid X',
        'Custom',
        'Custom Hybrid XS',
        'Gear'
    ],

    'Hustler': [
        'G',
        'X',
        'J Style',
        'Hybrid G',
        'Hybrid X'
    ],

    'Solio': [
        'G',
        'MX',
        'MZ',
        'Bandit',
        'Hybrid'
    ],

    'Splash': [
        'GL',
        'GLX'
    ],

    'Kizashi': [
        'SE',
        'Sport',
        'CVT'
    ],

    'SX4': [
        'GL',
        'GLX',
        'S-Cross',
        'Sedan'
    ],

    'Ciaz': [
        'GL',
        'GLX',
        'RS',
        'Alpha'
    ],

    'Liana': [
        'GL',
        'RX'
    ],

    'Cultus': [
        'VX',
        'VXR',
        'Euro II'
    ],

    'Esteem': [
        'GL',
        'GLX'
    ],

    'Cappuccino': [
        'Turbo'
    ],

    'Kei': [
        'A',
        'Works',
        'Sport'
    ]
},

   'Mitsubishi': {
    'Lancer': [
        'GL', 'GLX', 'GLXi',
        'ES', 'LS', 'SE',
        'EX',
        'Ralliart',
        'Evolution I', 'Evolution II',
        'Evolution III', 'Evolution IV',
        'Evolution V', 'Evolution VI',
        'Evolution VII', 'Evolution VIII',
        'Evolution IX', 'Evolution X',
        'EVO X'
    ],

    'Lancer Cargo': [
        '15M'
    ],

    'Galant': [
        'GL', 'GLS', 'VR-G',
        'VR-4'
    ],

    'Mirage': [
        'ES', 'GLX', 'LS',
        'Black Edition', 'G4'
    ],

    'Attrage': [
        'GLX', 'GLS', 'Black Series'
    ],

    'Outlander': [
        '20G', '24G',
        '2.0', '2.4', '2.5',
        'PHEV',
        'ES', 'SE',
        'SEL', 'GT',
        'Black Edition'
    ],

    'Outlander Sport': [
        'ES', 'SE', 'GT'
    ],

    'ASX': [
        '2WD', '4WD',
        'ES', 'LS', 'Aspire',
        'Exceed', 'Black Edition'
    ],

    'RVR': [
        'M', 'G',
        '2WD', '4WD'
    ],

    'Eclipse Cross': [
        'ES', 'LS',
        'Aspire',
        'Exceed',
        '2.0',
        'PHEV'
    ],

    'Pajero': [
        'SWB',
        'LWB',
        'Short Wheel Base',
        'Long Wheel Base',
        'GLS',
        'GLX',
        'VR-X',
        'Exceed',
        'Final Edition'
    ],

    'Pajero Sport': [
        'GLX',
        'GLS',
        'Dakar',
        'Exceed',
        'Elite Edition',
        'GSR'
    ],

    'Triton': [
        'Single Cab',
        'Club Cab',
        'Double Cab',
        'GL',
        'GLX',
        'GLS',
        'GLS Premium',
        'Athlete',
        'GSR',
        '4WD'
    ],

    'Delica D:5': [
        'M',
        'G',
        'P',
        'Urban Gear',
        'Premium'
    ],

    'Delica': [
        'Space Gear',
        'Star Wagon'
    ],

    'Canter': [
        'FE71',
        'FE84',
        'FE85',
        'Truck'
    ],

    'Minicab': [
        'Van',
        'Truck',
        'MiEV'
    ],

    'eK': [
        'eK Wagon',
        'eK X',
        'eK Space'
    ],

    'i-MiEV': [
        'Base',
        'G'
    ],

    '3000GT': [
        'SL',
        'VR-4'
    ],

    'Montero': [
        'GLS',
        'Limited'
    ]
},

'Isuzu': {
    'D-Max': [
        'Single Cab',
        'Space Cab',
        'Extended Cab',
        'Double Cab',
        'SX',
        'LS',
        'LS-M',
        'LS-U',
        'LS-T',
        'X-Terrain',
        'Blade',
        '4WD'
    ],

    'MU-X': [
        'LS-M',
        'LS-U',
        'LS-T',
        'Ultimate',
        'Premium',
        'X-Terrain'
    ],

    'MU-7': [
        '3.0',
        '3.0 VGS',
        '4x4'
    ],

    'Trooper': [
        '3.0D',
        '3.1D',
        'Citation',
        'Duty'
    ],

    'Wizard': [
        'XS',
        'Limited'
    ],

    'Bighorn': [
        'Handling by Lotus',
        'Irmscher'
    ],

    'VehiCROSS': [
        'Base'
    ],

    'N-Series': [
        'NHR',
        'NKR',
        'NLR',
        'NNR',
        'NPR',
        'NQR',
        'Truck'
    ],

    'F-Series': [
        'FRR',
        'FSR',
        'FTR',
        'FVR',
        'FVZ'
    ],

    'C-Series': [
        'CYZ',
        'CXZ'
    ],

    'Elf': [
        'NHR',
        'NKR',
        'NPR',
        'Truck'
    ],

    'Forward': [
        'FRR',
        'FTR',
        'FVR'
    ],

    'Giga': [
        'CXZ',
        'CYZ',
        'EXZ'
    ]
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
    
    fuel_economy_source = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Fuel Economy Source --')] + list(Car.FUEL_ECONOMY_SOURCE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fuel_economy_combined = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select Fuel Economy --')] + list(Car.FUEL_ECONOMY_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Car
        fields = ('title', 'make', 'model', 'variant', 'year', 'price', 'is_price_negotiable', 'mileage', 
                 'fuel_type', 'transmission', 'condition', 'color', 'exterior_color', 'interior_color', 'seat_material', 'interior_trim', 'seats',
                 'engine_size', 'doors', 'body_type', 'previous_owners', 'number_of_keys',
                 'fuel_economy_source', 'fuel_economy_combined',
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
            'is_price_negotiable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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

    NUMBER_OF_KEYS_CHOICES = [
        ('', '-- All Keys --'),
        ('1', '1 Key'),
        ('2', '2 Keys'),
        ('3', '3 Keys'),
        ('4', '4+ Keys'),
    ]

    number_of_keys = forms.ChoiceField(
        required=False,
        choices=NUMBER_OF_KEYS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fuel_economy_source = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Fuel Economy Sources --')] + list(Car.FUEL_ECONOMY_SOURCE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    FUEL_ECONOMY_FROM_CHOICES = [('', '--- Fuel Economy from ---')] + [
        (value, label) for value, label in Car.FUEL_ECONOMY_CHOICES if value
    ]

    FUEL_ECONOMY_TO_CHOICES = [('', '--- Fuel Economy to ---')] + [
        (value, label) for value, label in Car.FUEL_ECONOMY_CHOICES if value
    ]

    fuel_economy_from = forms.ChoiceField(
        required=False,
        choices=FUEL_ECONOMY_FROM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    fuel_economy_to = forms.ChoiceField(
        required=False,
        choices=FUEL_ECONOMY_TO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

   

    
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


