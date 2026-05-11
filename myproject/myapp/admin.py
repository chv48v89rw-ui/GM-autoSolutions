from django.contrib import admin
from .models import UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Favorite


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
