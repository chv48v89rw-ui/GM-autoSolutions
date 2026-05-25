from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Report, 
                     SavedSearch, CarComparison, Notification, NotificationPreference)

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


class EmailVerificationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    verification_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter verification code',
            'maxlength': '6'
        })
    )


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
    class Meta:
        model = Car
        fields = ('title', 'make', 'model', 'year', 'price', 'mileage', 
                 'fuel_type', 'transmission', 'condition', 'color', 'seats',
                 'engine_size', 'doors', 'body_type', 'previous_owners',
                 'description', 'main_image', 'features')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Car title'
            }),
            'make': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Make (Toyota, BMW, etc.)'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model (Camry, 3 Series, etc.)'
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
    # Get unique makes from database
    from .models import Car
    
    def get_make_choices():
        # Popular car makes in Kenya
        popular_makes = [
            'Toyota',
            'Nissan',
            'BMW',
            'Mercedes-Benz',
            'Honda',
            'Hyundai',
            'Subaru',
            'Isuzu',
            'Suzuki',
            'Mitsubishi',
            'Ford',
            'Daihatsu',
            'Mazda',
            'Kia',
            'Volkswagen',
            'Audi',
            'Lexus',
            'Range Rover',
            'Land Rover',
            'Chevrolet',
            'Peugeot',
            'Renault',
            'Fiat',
            'Tata',
            'MG',
            'Geely',
            'JAC',
            'BAIC',
            'Volvo',
            'Porsche',
            'Jaguar',
            'Jeep',
            'Chery',
            'BYD',
            'Haval',
            'Jetour',
            'Dongfeng',
            'Foton',
        ]
        # Get additional makes from database
        db_makes = set(Car.objects.values_list('make', flat=True).distinct())
        all_makes = sorted(set(popular_makes) | db_makes)
        return [('', '-- All Makes --')] + [(make, make) for make in all_makes]
    
    make = forms.ChoiceField(required=False, choices=get_make_choices(), widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    model = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Model'
    }))
    
        
    # Generate year choices from 1990 to current year with blank option
    current_year = timezone.now().year
    YEAR_CHOICES = [('', '--- Year from ---')] + [(year, str(year)) for year in range(current_year, 1989, -1)]
    
    year_from = forms.ChoiceField(required=False, choices=YEAR_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    
    # Generate year choices for year_to with blank option
    YEAR_TO_CHOICES = [('', '--- Year to ---')] + [(year, str(year)) for year in range(current_year, 1989, -1)]
    
    year_to = forms.ChoiceField(required=False, choices=YEAR_TO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    # Price range choices from 100,000 to 50,000,000 KSH with 500K increments
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
    
    # Price to choices with higher range - 500K increments up to 500M
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
    ]
    
    price_from = forms.ChoiceField(required=False, choices=PRICE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    
    # Price to choices with higher range - 500K increments up to 500M
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
    
    # Mileage choices from 1,000 to 400,000 km with 10,000 km increments
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
    
    # Mileage to choices - same as from but starting from 10,000
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
    
    fuel_type = forms.ChoiceField(required=False, choices=[('', '-- All Fuel Types --')] + list(Car.FUEL_CHOICES), 
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    transmission = forms.ChoiceField(required=False, choices=[('', '-- All Transmissions --')] + list(Car.TRANSMISSION_CHOICES),
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    condition = forms.ChoiceField(required=False, choices=[('', '-- All Conditions --')] + list(Car.CONDITION_CHOICES),
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    engine_size = forms.ChoiceField(required=False, choices=[('', '-- All Engine Sizes --')] + list(Car.ENGINE_SIZE_CHOICES),
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    doors = forms.ChoiceField(required=False, choices=[('', '-- All Doors --')] + list(Car.DOORS_CHOICES),
                             widget=forms.Select(attrs={'class': 'form-select'}))
    body_type = forms.ChoiceField(required=False, choices=[('', '-- All Body Types --')] + list(Car.BODY_TYPE_CHOICES),
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    previous_owners = forms.ChoiceField(required=False, choices=[('', '-- All Owners --')] + list(Car.OWNERS_CHOICES),
                                       widget=forms.Select(attrs={'class': 'form-select'}))
    seats = forms.ChoiceField(required=False, choices=[
        ('', '-- All Seats --'),
        ('2', '2 Seats'),
        ('4', '4 Seats'),
        ('5', '5 Seats'),
        ('7', '7 Seats'),
        ('8', '8+ Seats'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    
    # Additional filters
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


