from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('dealership', 'Dealership'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


class Dealership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dealership')
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='dealership_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)  # City/Area in Kenya
    latitude = models.FloatField(null=True, blank=True)  # For Google Maps
    longitude = models.FloatField(null=True, blank=True)  # For Google Maps
    address = models.TextField()
    is_approved = models.BooleanField(default=False)  # Dealership must be approved to be active
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name


class Car(models.Model):
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=255)
    make = models.CharField(max_length=100)  # Toyota, BMW, etc.
    model = models.CharField(max_length=100)  # Camry, 3 Series, etc.
    year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(datetime.now().year + 1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.IntegerField()  # in kilometers
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    color = models.CharField(max_length=50)
    seats = models.IntegerField(default=5)
    description = models.TextField()
    
    # Images
    main_image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    
    # Features
    features = models.TextField(help_text="Comma-separated list of features")  # e.g., "ABS, Power Steering, AC, etc."
    is_sold = models.BooleanField(default=False)  # Mark car as sold
    is_approved = models.BooleanField(default=False)  # Must be approved by admin to appear
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car}"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.car} by {self.buyer.username}"


class DealershipReview(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.dealership} by {self.buyer.username}"


class Enquiry(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='enquiries', null=True, blank=True)
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        car_label = f" for {self.car}" if self.car else ""
        return f"Enquiry from {self.buyer_name}{car_label}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'car')  # Prevent duplicate favorites
    
    def __str__(self):
        return f"{self.user.username} favorited {self.car}"
