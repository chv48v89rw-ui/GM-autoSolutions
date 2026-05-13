from django.contrib import admin
from .models import UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Favorite, EmailVerification, Report, Subscription, SubscriptionRequest 

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'location', 'is_approved', 'rating', 'created_at')
    list_filter = ('location', 'is_approved', 'rating', 'created_at')
    search_fields = ('company_name', 'email')
    actions = ('approve_dealerships', 'reject_dealerships')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Company Information', {'fields': ('company_name', 'description', 'logo', 'website')}),
        ('Contact', {'fields': ('email', 'phone_number')}),
        ('Location', {'fields': ('location', 'address', 'latitude', 'longitude')}),
        ('Status & Rating', {'fields': ('is_approved', 'rating')}),
    )

    @admin.action(description='Approve selected dealerships')
    def approve_dealerships(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} dealership(s) approved.")

    @admin.action(description='Reject selected dealerships')
    def reject_dealerships(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} dealership(s) set to not approved.")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'dealership', 'price', 'year', 'mileage', 'condition', 'is_approved', 'is_sold', 'created_at')
    list_filter = ('dealership', 'year', 'fuel_type', 'condition', 'transmission', 'is_approved', 'is_sold', 'created_at')
    search_fields = ('title', 'make', 'model')
    actions = ('approve_cars', 'reject_cars')
    fieldsets = (
        ('Dealership', {'fields': ('dealership',)}),
        ('Basic Info', {'fields': ('title', 'make', 'model', 'year')}),
        ('Pricing & Condition', {'fields': ('price', 'mileage', 'condition', 'is_sold', 'is_approved')}),
        ('Vehicle Details', {'fields': ('fuel_type', 'transmission', 'color', 'seats')}),
        ('Description', {'fields': ('description', 'features')}),
        ('Images', {'fields': ('main_image', 'image2', 'image3', 'image4')}),
    )

    @admin.action(description='Approve selected cars')
    def approve_cars(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} car(s) approved.")

    @admin.action(description='Reject selected cars')
    def reject_cars(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} car(s) set to not approved.")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('car__title', 'buyer__username')


@admin.register(DealershipReview)
class DealershipReviewAdmin(admin.ModelAdmin):
    list_display = ('dealership', 'buyer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('dealership__company_name', 'buyer__username')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer_name', 'buyer_email', 'created_at')
    list_filter = ('created_at', 'car__dealership')
    search_fields = ('buyer_name', 'buyer_email', 'car__title')
    readonly_fields = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at', 'car__dealership')
    search_fields = ('user__username', 'car__title', 'car__make', 'car__model')


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('reporter__username', 'description')
    actions = ('mark_under_review', 'mark_resolved', 'mark_dismissed')
    fieldsets = (
        ('Report Info', {'fields': ('reporter', 'report_type', 'description')}),
        ('Related Item', {'fields': ('car', 'dealership', 'reported_user')}),
        ('Status & Resolution', {'fields': ('status',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.action(description='Mark selected reports as under review')
    def mark_under_review(self, request, queryset):
        updated = queryset.update(status='under_review')
        self.message_user(request, f"{updated} report(s) marked as under review.")

    @admin.action(description='Mark selected reports as resolved')
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='resolved')
        self.message_user(request, f"{updated} report(s) marked as resolved.")

    @admin.action(description='Mark selected reports as dismissed')
    def mark_dismissed(self, request, queryset):
        updated = queryset.update(status='dismissed')
        self.message_user(request, f"{updated} report(s) dismissed.")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('dealership', 'subscription_type', 'status', 'amount_paid', 'start_date', 'end_date')
    list_filter = ('subscription_type', 'status', 'start_date', 'end_date')
    search_fields = ('dealership__company_name', 'payment_reference')
    fieldsets = (
        ('Subscription Info', {'fields': ('dealership', 'subscription_type', 'status', 'is_premium')}),
        ('Payment Details', {'fields': ('amount_paid', 'payment_reference', 'start_date', 'end_date')}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'subscription_type', 'status', 'created_at')
    list_filter = ('subscription_type', 'status', 'created_at')
    search_fields = ('company_name', 'email', 'contact_person')
    fieldsets = (
        ('Request Info', {'fields': ('company_name', 'contact_person', 'email', 'phone', 'subscription_type')}),
        ('Additional Info', {'fields': ('message', 'status')}),
        ('Admin Notes', {'fields': ('admin_notes',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_approved', 'mark_rejected', 'mark_completed']
    
    @admin.action(description='Mark selected requests as Approved')
    def mark_approved(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} subscription request(s) approved.")
        return updated
    
    @admin.action(description='Mark selected requests as Rejected')
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} subscription request(s) rejected.")
        return updated
    
    @admin.action(description='Mark selected requests as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} subscription request(s) completed.")
        return updated
