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
        'Land Cruiser': ['Prado', '70 Series', '200 Series', '300 Series', 'V8'],
        'Hilux': ['Single Cab', 'Extra Cab', 'Double Cab', '2WD', '4WD', 'Revo'],
        'Probox': ['DX', 'GL'],
        'Succeed': ['UL', 'UL-X'],
        'Noah': ['X', 'G', 'Hybrid'],
        'Voxy': ['X', 'ZS', 'Hybrid'],
        'Esquire': ['Gi', 'Hybrid'],
        'Alphard': ['240S', '350S', 'Executive Lounge'],
        'Vellfire': ['2.4Z', '3.5Z', 'Executive Lounge'],
        'Hiace': ['Commuter', 'DX', 'GL'],
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
    },

    'BMW': {
        '1 Series': ['116i', '118i'],
        '3 Series': ['318i', '320i', '330i', 'M Sport'],
        '5 Series': ['520i', '530i', '540i', 'M Sport'],
        '7 Series': ['730i', '740i'],
        'X1': ['sDrive18i', 'xDrive20i'],
        'X3': ['xDrive20i', 'xDrive30i'],
        'X5': ['xDrive30d', 'xDrive40i'],
        'X6': ['xDrive40i', 'M50i'],
        'M Models': ['M2', 'M3', 'M4', 'M5'],
    },

    'Mercedes-Benz': {
        'A-Class': ['A180', 'A200'],
        'C-Class': ['C180', 'C200', 'C220d', 'C300'],
        'E-Class': ['E200', 'E250', 'E300'],
        'S-Class': ['S350', 'S450', 'S500', 'Maybach'],
        'GLA': ['GLA180', 'GLA200'],
        'GLB': ['GLB200'],
        'GLC': ['GLC200', 'GLC300'],
        'GLE': ['GLE350', 'GLE400'],
        'GLS': ['GLS350', 'GLS450'],
        'G-Class': ['G350d', 'G63 AMG'],
        'CLA': ['CLA180', 'CLA200'],
        'CLS': ['CLS350'],
        'Vito': ['111 CDI'],
        'Sprinter': ['313 CDI'],
    },

    'Audi': {
        'A1': ['Sportback'],
        'A3': ['30 TFSI', '35 TFSI'],
        'A4': ['30 TFSI', '40 TFSI'],
        'A5': ['40 TFSI'],
        'A6': ['40 TFSI', '45 TFSI'],
        'Q2': ['30 TFSI'],
        'Q3': ['35 TFSI'],
        'Q5': ['40 TFSI', '45 TDI'],
        'Q7': ['45 TFSI', '50 TDI'],
        'Q8': ['55 TFSI'],
    },

    'Lexus': {
        'IS': ['250', '300h F Sport'],
        'ES': ['250', '300h'],
        'GS': ['350'],
        'LS': ['460', '600h'],
        'NX': ['200t', '300h', '350h'],
        'RX': ['270', '350', '450h'],
        'LX': ['570', '600'],
        'GX': ['460'],
    },

    'Volkswagen': {
        'Golf': ['TSI', 'GTI', 'R'],
        'Polo': ['TSI', 'GTI'],
        'Passat': ['TSI', 'TDI'],
        'Tiguan': ['TSI', '4Motion'],
        'Touareg': ['V6 TDI'],
        'Amarok': ['TDI'],
        'Jetta': ['TSI'],
    },

    'Ford': {
        'Ranger': ['2.2 TDCi', '3.2 TDCi', 'Wildtrak'],
        'Everest': ['Trend', 'Titanium'],
        'Focus': ['S', 'SE'],
        'Kuga': ['EcoBoost'],
        'Explorer': ['Limited'],
        'Mustang': ['GT V8'],
    },

    'Chevrolet': {
        'Cruze': ['LS', 'LT'],
        'Captiva': ['LS', 'LT'],
        'Trailblazer': ['LT'],
        'Malibu': ['LT'],
    },

    'Hyundai': {
        'i10': ['Base'],
        'i20': ['Base'],
        'Accent': ['GLS'],
        'Elantra': ['SE', 'SEL'],
        'Sonata': ['SE', 'SEL'],
        'Tucson': ['GLS', 'Limited'],
        'Santa Fe': ['Sport', 'Limited'],
        'Kona': ['Base'],
        'Palisade': ['Calligraphy'],
    },

    'Kia': {
        'Picanto': ['Base'],
        'Rio': ['Base'],
        'Cerato': ['S', 'EX'],
        'Sportage': ['LX', 'EX', 'GT-Line'],
        'Sorento': ['LX', 'EX'],
        'Seltos': ['EX'],
    },

    'Nissan': {
        'March': ['Base'],
        'Note': ['e-Power', 'X'],
        'Juke': ['Base'],
        'Tiida': ['Latio'],
        'X-Trail': ['20S', '20X', 'Hybrid', '4WD'],
        'Qashqai': ['2WD', '4WD'],
        'Patrol': ['Y61', 'Y62'],
        'Navara': ['King Cab', 'Double Cab', '4WD'],
        'Serena': ['Highway Star'],
    },

    'Mazda': {
        'Demio': ['13S', '15S'],
        'Axela': ['15S', '20S'],
        'Atenza': ['20S', '25S'],
        'CX-3': ['20S'],
        'CX-5': ['20S', '25S', '2.2D'],
        'CX-9': ['25T'],
        'BT-50': ['Double Cab'],
    },

    'Subaru': {
        'Impreza': ['1.6i', '2.0i'],
        'Legacy': ['2.5i'],
        'Outback': ['2.5i'],
        'Forester': ['2.0i', '2.0XT', 'Premium'],
        'XV': ['1.6i', '2.0i'],
        'WRX': ['STI', 'Turbo'],
    },

    'Volvo': {
        'S60': ['T5', 'T6'],
        'S90': ['T5', 'T6'],
        'V40': ['T4'],
        'XC40': ['T4', 'T5'],
        'XC60': ['T5', 'T6'],
        'XC90': ['T6'],
    },

    'Land Rover': {
        'Discovery': ['3', '4', '5'],
        'Discovery Sport': ['S', 'SE', 'HSE'],
        'Defender': ['90', '110', '130'],
    },

    'Range Rover': {
        'Range Rover': ['Vogue', 'Autobiography', 'SV'],
        'Range Rover Sport': ['HSE', 'SE', 'SVR'],
        'Velar': ['S', 'SE', 'R-Dynamic'],
        'Evoque': ['S', 'SE', 'HSE'],
    }
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
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))
    
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





class DealershipRegistrationForm(forms.ModelForm):
    class Meta:
        model = Dealership
        fields = ('company_name', 'description', 'logo', 'business_certificate', 'website', 'email', 
                 'phone_number', 'location', 'area_code', 'address')
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
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
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'business_certificate': forms.FileInput(attrs={'class': 'form-control'}),
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

    class Meta:
        model = Car
        fields = ('title', 'make', 'model', 'variant', 'year', 'price', 'mileage', 
                 'fuel_type', 'transmission', 'condition', 'color', 'seats',
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
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
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
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
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
 
    engine_size = forms.ChoiceField(
        required=False,
        choices=[('', '-- All Engine Sizes --')] + list(Car.ENGINE_SIZE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
 
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


