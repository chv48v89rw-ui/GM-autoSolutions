from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, Dealership, Car, Review, DealershipReview, Enquiry
from .models import Report

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
        fields = ('company_name', 'description', 'logo', 'website', 'email', 
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
        makes = Car.objects.values_list('make', flat=True).distinct().order_by('make')
        return [('', '-- All Makes --')] + [(make, make) for make in makes]
    
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


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 'description')
        widgets = {
            'report_type': forms.Select(choices=Report.REPORT_TYPES),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


