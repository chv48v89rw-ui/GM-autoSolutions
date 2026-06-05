from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime
import secrets


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('dealership', 'Dealership'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    phone_number = models.CharField(max_length=15, blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )

    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)

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
    area_code = models.CharField(max_length=20, blank=True, help_text="Area code (e.g., 00100 for Nairobi CBD)")
    latitude = models.FloatField(null=True, blank=True)  # For Google Maps
    longitude = models.FloatField(null=True, blank=True)  # For Google Maps
    address = models.TextField()
    business_certificate = models.FileField(upload_to='dealership_certificates/', null=True, blank=False)
    is_approved = models.BooleanField(default=False)  # Dealership must be approved to be active
    is_premium = models.BooleanField(default=False)  # Premium dealerships appear as top picks on the home page
    RESPONSE_TIME_CHOICES = [
        ('10_min', '10 min'),
        ('1_hr', '1 hr'),
        ('3_hr', '3 hr'),
        ('6_hr', '6 hr'),
        ('24_hr', '24 hr'),
    ]
    response_time_badge_enabled = models.BooleanField(default=False)
    response_time_badge_choice = models.CharField(
        max_length=20,
        choices=RESPONSE_TIME_CHOICES,
        blank=True,
        default=''
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def response_time_badge_label(self):
        if self.response_time_badge_enabled and self.response_time_badge_choice:
            return dict(self.RESPONSE_TIME_CHOICES).get(self.response_time_badge_choice, '')
        return ''

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
        ('brand_new', 'Brand New'),
        ('used_locally', 'Locally Used'),
        ('used_foreignly', 'Foreignly Used'),
    ]
    
    ENGINE_SIZE_CHOICES = [
        ('1.0', '1.0L'),
        ('1.2', '1.2L'),
        ('1.4', '1.4L'),
        ('1.5', '1.5L'),
        ('1.6', '1.6L'),
        ('1.8', '1.8L'),
        ('2.0', '2.0L'),
        ('2.5', '2.5L'),
        ('3.0', '3.0L'),
        ('other', 'Other'),
    ]
    
    DOORS_CHOICES = [
        (2, '2 Doors'),
        (3, '3 Doors'),
        (4, '4 Doors'),
        (5, '5 Doors'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Wagon'),
        ('pickup', 'Pickup'),
        ('van', 'Van'),
        ('other', 'Other'),
    ]
    
    OWNERS_CHOICES = [
        (0, '0 Owners'),
        (1, '1 Owner'),
        (2, '2 Owners'),
        (3, '3+ Owners'),
    ]
    
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='cars')
    title = models.CharField(max_length=255)
    make = models.CharField(max_length=100)  # Toyota, BMW, etc.
    model = models.CharField(max_length=100)  # Camry, 3 Series, etc.
    variant = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(datetime.now().year + 1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.IntegerField()  # in kilometers
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    color = models.CharField(max_length=50)
    exterior_color = models.CharField(max_length=100, blank=True, help_text="Exterior paint color (e.g., Pearl White, Jet Black)")
    interior_color = models.CharField(max_length=100, blank=True, help_text="Interior color scheme (e.g., Black, Beige, Two-Tone)")
    seat_material = models.CharField(max_length=100, blank=True, help_text="Seat material type (e.g., Leather, Cloth, Nappa Leather)")
    interior_trim = models.CharField(max_length=100, blank=True, help_text="Interior trim material (e.g., Piano Black, Carbon Fiber, Wood Trim)")
    seats = models.IntegerField(default=5)
    engine_size = models.CharField(max_length=10, choices=ENGINE_SIZE_CHOICES, blank=True)
    doors = models.IntegerField(choices=DOORS_CHOICES, blank=True, null=True)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    previous_owners = models.IntegerField(choices=OWNERS_CHOICES, blank=True, null=True)
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
    is_premium = models.BooleanField(default=False)  # Premium cars appear in best cars section on home page
    submitted_for_review = models.BooleanField(default=False)  # Dealership submitted for admin review
    submitted_at = models.DateTimeField(null=True, blank=True)  # When car was submitted for review
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        variant_text = f" {self.variant}" if self.variant else ""
        return f"{self.year} {self.make} {self.model}{variant_text}"


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
    is_approved = models.BooleanField(default=False)  # Admin approval required
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.car} by {self.buyer.username}"


class DealershipReview(models.Model):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)  # Admin approval required
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.dealership} by {self.buyer.username}"


class Enquiry(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='enquiries', null=True, blank=True)
    dealership = models.ForeignKey('Dealership', on_delete=models.CASCADE, related_name='enquiries', null=True, blank=True)
    buyer_name = models.CharField(max_length=255)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=15)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    dealership_response = models.TextField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        car_label = f" for {self.car}" if self.car else ""
        return f"Enquiry from {self.buyer_name}{car_label}"

    @property
    def last_message_sender(self):
        last_message = self.messages.order_by('-created_at').first()
        return last_message.sender_type if last_message else None


class EnquiryMessage(models.Model):
    SENDER_CHOICES = [
        ('buyer', 'Buyer'),
        ('dealership', 'Dealership'),
    ]

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=20, choices=SENDER_CHOICES)
    sender_name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_sender_type_display()} message for {self.enquiry}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'car')  # Prevent duplicate favorites
    
    def __str__(self):
        return f"{self.user.username} favorited {self.car}"



class Report(models.Model):
    REPORT_TYPES = [
        ('inappropriate_content', 'Inappropriate Content'),
        ('fraud', 'Fraud or Scam'),
        ('fake_listing', 'Fake Listing'),
        ('harassment', 'Harassment'),
        ('spam', 'Spam'),
        ('duplicate', 'Duplicate Listing'),
        ('other', 'Other Issue'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='car_reports')
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null=True, blank=True, related_name='dealership_reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_reports')
    report_type = models.CharField(max_length=25, choices=REPORT_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reporter.username} - {self.get_report_type_display()}"
        report_of = self.car or self.dealership or self.reported_user
        return f"Report by {self.reporter.username} - {self.get_report_type_display()} ({self.get_status_display()})"


class Subscription(models.Model):
    SUBSCRIPTION_TYPES = [
        ('monthly', 'Monthly Subscription'),
        ('half_yearly', 'Half-Yearly Subscription'),
        ('yearly', 'Yearly Subscription'),
        ('per_car', 'Per Car Listing'),
        ('premium', 'Premium Dealership'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Payment'),
    ]
    
    dealership = models.OneToOneField(Dealership, on_delete=models.CASCADE, related_name='subscription')
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, blank=True)
    is_premium = models.BooleanField(default=False)  # For premium checkmark
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.dealership.company_name} - {self.get_subscription_type_display()}"
    
    def is_active(self):
        return self.status == 'active' and (self.end_date is None or self.end_date > timezone.now())


class SubscriptionRequest(models.Model):
    SUBSCRIPTION_TYPES = [
        ('monthly', 'Monthly Subscription'),
        ('half_yearly', 'Half-Yearly Subscription'),
        ('yearly', 'Yearly Subscription'),
        ('premium_monthly', 'Premium Monthly'),
        ('premium_yearly', 'Premium Yearly'),
        ('per_car', 'Per Car Listing'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null=True, blank=True, related_name='subscription_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.get_subscription_type_display()}"


class CarView(models.Model):
    """Track car page views for analytics"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Track logged-in users
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['car', 'viewed_at']),
            models.Index(fields=['car', 'user']),
        ]
    
    def __str__(self):
        return f"View of {self.car.title} at {self.viewed_at}"


class DealershipClick(models.Model):
    """Track clicks from dealership pages for analytics"""
    CLICK_TYPES = [
        ('phone', 'Phone Number Click'),
        ('email', 'Email Click'),
        ('website', 'Website Visit'),
        ('directions', 'Directions Click'),
        ('car_view', 'Car Detail View'),
        ('contact', 'Contact Form Submission'),
    ]
    
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name='clicks')
    click_type = models.CharField(max_length=20, choices=CLICK_TYPES)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, related_name='dealership_clicks')  # For car-related clicks
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['dealership', 'click_type', 'clicked_at']),
            models.Index(fields=['dealership', 'clicked_at']),
        ]
    
    def __str__(self):
        return f"{self.get_click_type_display()} on {self.dealership.company_name} at {self.clicked_at}"


class SavedSearch(models.Model):
    """User's saved car search preferences"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100, help_text="Name for this search (e.g., 'Toyota under 500k')")
    
    # Search parameters
    make = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    year_from = models.IntegerField(null=True, blank=True)
    year_to = models.IntegerField(null=True, blank=True)
    price_from = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_to = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    mileage_from = models.IntegerField(null=True, blank=True)
    mileage_to = models.IntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=20, blank=True)
    transmission = models.CharField(max_length=20, blank=True)
    condition = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)
    body_type = models.CharField(max_length=20, blank=True)
    features = models.TextField(blank=True, help_text="Comma-separated features to search for")
    
    # Notification settings for this search
    alert_on_new = models.BooleanField(default=True, help_text="Send alert for new matching cars")
    alert_on_price_drop = models.BooleanField(default=False, help_text="Send alert when prices drop")
    price_drop_percentage = models.IntegerField(default=5, help_text="Alert when price drops by this percentage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_alerted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class CarComparison(models.Model):
    """Tool for comparing multiple cars side-by-side"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comparisons')
    name = models.CharField(max_length=255, blank=True)
    cars = models.ManyToManyField(Car, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Comparison by {self.user.username} - {self.cars.count()} cars"
    
    def get_cars_list(self):
        return self.cars.all()[:10]  # Max 10 cars for comparison


class Notification(models.Model):
    """Notification system for users"""
    NOTIFICATION_TYPES = [
        ('new_car', 'New Car Matching Search'),
        ('price_drop', 'Price Drop Alert'),
        ('enquiry_response', 'Dealership Response to Enquiry'),
        ('review_approved', 'Your Review Was Approved'),
        ('dealership_message', 'New Message from Dealership'),
        ('new_listing', 'New Listing from Followed Dealership'),
        ('promotion', 'Special Promotion'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    
    # Channels
    is_sent_email = models.BooleanField(default=False)
    is_sent_sms = models.BooleanField(default=False)
    is_sent_push = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} to {self.user.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    
    # Email preferences
    email_on_new_car = models.BooleanField(default=True)
    email_on_price_drop = models.BooleanField(default=True)
    email_on_enquiry_response = models.BooleanField(default=True)
    email_on_review_approved = models.BooleanField(default=True)
    email_on_promotions = models.BooleanField(default=False)
    
    # SMS preferences (requires phone number)
    sms_on_new_car = models.BooleanField(default=False)
    sms_on_price_drop = models.BooleanField(default=False)
    sms_on_enquiry_response = models.BooleanField(default=True)
    sms_phone_number = models.CharField(max_length=15, blank=True)
    
    # Push preferences
    push_on_new_car = models.BooleanField(default=False)
    push_on_price_drop = models.BooleanField(default=False)
    push_on_enquiry_response = models.BooleanField(default=True)
    
    # Notification frequency
    FREQUENCY_CHOICES = [
        ('instant', 'Instant'),
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Digest'),
    ]
    notification_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='instant')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"

