from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Dealership, Car, Review, DealershipReview, Enquiry


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
        fields = ('user_type', 'phone_number', 'profile_picture')
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-select'}),
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
                 'phone_number', 'location', 'latitude', 'longitude', 'address')
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
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude (e.g. -1.2921)'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude (e.g. 36.8219)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Full address',
                'rows': 3
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
    make = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Make'
    }))
    model = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Model'
    }))
    year_from = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Year from'
    }))
    year_to = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Year to'
    }))
    price_from = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Price from'
    }))
    price_to = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Price to'
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
