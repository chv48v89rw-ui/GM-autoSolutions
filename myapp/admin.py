from django.contrib import admin
from .models import UserProfile, Dealership, Car, Review, DealershipReview, Enquiry, Favorite, Report, Subscription, SubscriptionRequest 

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'location', 'is_approved', 'is_verified', 'is_premium', 'rating', 'created_at')
    list_display_links = ('company_name',)
    list_editable = ('rating',)
    list_filter = ('location', 'is_approved', 'is_verified', 'is_premium', 'created_at')
    search_fields = ('company_name', 'email')
    actions = ('approve_dealerships', 'reject_dealerships', 'verify_dealerships', 'unverify_dealerships', 'mark_premium', 'unmark_premium',
               'set_rating_5', 'set_rating_4', 'set_rating_3', 'set_rating_2', 'set_rating_1', 'clear_ratings')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Company Information', {'fields': ('company_name', 'description', 'logo', 'website')}),
        ('Contact', {'fields': ('email', 'phone_number')}),
        ('Location', {'fields': ('location', 'address', 'latitude', 'longitude')}),
        ('Status & Rating', {'fields': ('is_approved', 'is_verified', 'is_premium', 'rating')}),
    )

    @admin.action(description='Approve selected dealerships')
    def approve_dealerships(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} dealership(s) approved.")

    @admin.action(description='Reject selected dealerships')
    def reject_dealerships(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} dealership(s) set to not approved.")

    @admin.action(description='Verify selected dealerships')
    def verify_dealerships(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} dealership(s) verified.")

    @admin.action(description='Remove verification from selected dealerships')
    def unverify_dealerships(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} dealership(s) unverified.")

    @admin.action(description='Mark selected dealerships as Premium')
    def mark_premium(self, request, queryset):
        updated = queryset.update(is_premium=True)
        self.message_user(request, f"{updated} dealership(s) marked as premium.")

    @admin.action(description='Remove Premium status from selected dealerships')
    def unmark_premium(self, request, queryset):
        updated = queryset.update(is_premium=False)
        self.message_user(request, f"{updated} dealership(s) removed from premium status.")

    @admin.action(description='Set rating to 5 for selected dealerships')
    def set_rating_5(self, request, queryset):
        updated = queryset.update(rating=5.0)
        self.message_user(request, f"{updated} dealership(s) rating set to 5.")

    @admin.action(description='Set rating to 4 for selected dealerships')
    def set_rating_4(self, request, queryset):
        updated = queryset.update(rating=4.0)
        self.message_user(request, f"{updated} dealership(s) rating set to 4.")

    @admin.action(description='Set rating to 3 for selected dealerships')
    def set_rating_3(self, request, queryset):
        updated = queryset.update(rating=3.0)
        self.message_user(request, f"{updated} dealership(s) rating set to 3.")

    @admin.action(description='Set rating to 2 for selected dealerships')
    def set_rating_2(self, request, queryset):
        updated = queryset.update(rating=2.0)
        self.message_user(request, f"{updated} dealership(s) rating set to 2.")

    @admin.action(description='Set rating to 1 for selected dealerships')
    def set_rating_1(self, request, queryset):
        updated = queryset.update(rating=1.0)
        self.message_user(request, f"{updated} dealership(s) rating set to 1.")

    @admin.action(description='Clear ratings for selected dealerships')
    def clear_ratings(self, request, queryset):
        updated = queryset.update(rating=0.0)
        self.message_user(request, f"{updated} dealership(s) ratings cleared.")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'dealership', 'price', 'year', 'mileage', 'condition', 'is_approved', 'is_premium', 'is_top_pick', 'submitted_for_review', 'is_sold', 'created_at')
    list_filter = ('dealership', 'year', 'fuel_type', 'condition', 'transmission', 'is_approved', 'is_premium', 'is_top_pick', 'submitted_for_review', 'is_sold', 'created_at')
    list_editable = ('is_top_pick',)
    search_fields = ('title', 'make', 'model')
    actions = ('approve_cars', 'reject_cars', 'mark_premium', 'unmark_premium', 'mark_top_pick', 'unmark_top_pick', 'mark_submission_reviewed')
    fieldsets = (
        ('Dealership', {'fields': ('dealership',)}),
        ('Basic Info', {'fields': ('title', 'make', 'model', 'year')}),
        ('Pricing & Condition', {'fields': ('price', 'mileage', 'condition', 'is_sold', 'is_approved', 'is_premium', 'is_top_pick')}),
        ('Review Status', {'fields': ('submitted_for_review', 'submitted_at')}),
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

    @admin.action(description='Mark selected cars as Premium')
    def mark_premium(self, request, queryset):
        updated = queryset.update(is_premium=True)
        self.message_user(request, f"{updated} car(s) marked as premium.")

    @admin.action(description='Remove Premium status from selected cars')
    def unmark_premium(self, request, queryset):
        updated = queryset.update(is_premium=False)
        self.message_user(request, f"{updated} car(s) removed from premium status.")

    @admin.action(description='Mark selected cars as Top Pick')
    def mark_top_pick(self, request, queryset):
        updated = queryset.update(is_top_pick=True)
        self.message_user(request, f"{updated} car(s) marked as top pick.")

    @admin.action(description='Remove Top Pick status from selected cars')
    def unmark_top_pick(self, request, queryset):
        updated = queryset.update(is_top_pick=False)
        self.message_user(request, f"{updated} car(s) removed from top pick status.")

    @admin.action(description='Mark submission as reviewed (clear submitted_for_review flag)')
    def mark_submission_reviewed(self, request, queryset):
        updated = queryset.update(submitted_for_review=False)
        self.message_user(request, f"{updated} car submission(s) marked as reviewed.")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'buyer', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('car__title', 'buyer__username', 'comment')
    actions = ('approve_reviews', 'reject_reviews')
    readonly_fields = ('car', 'buyer', 'rating', 'comment', 'created_at')

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved and now visible to users.")

    @admin.action(description='Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} review(s) rejected and hidden from users.")


@admin.register(DealershipReview)
class DealershipReviewAdmin(admin.ModelAdmin):
    list_display = ('dealership', 'buyer', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('dealership__company_name', 'buyer__username', 'comment')
    actions = ('approve_reviews', 'reject_reviews')
    readonly_fields = ('dealership', 'buyer', 'rating', 'comment', 'created_at')

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved and now visible to users.")

    @admin.action(description='Reject selected reviews')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} review(s) rejected and hidden from users.")


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


# EmailVerification model removed from admin


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
    list_display = ('company_name', 'contact_person', 'email', 'subscription_type', 'status', 'dealership', 'car', 'created_at')
    list_filter = ('subscription_type', 'status', 'created_at')
    search_fields = ('company_name', 'email', 'contact_person')
    fieldsets = (
        ('Request Info', {'fields': ('company_name', 'contact_person', 'email', 'phone', 'subscription_type')}),
        ('Additional Info', {'fields': ('message', 'dealership', 'car', 'status')}),
        ('Admin Notes', {'fields': ('admin_notes',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_approved', 'mark_rejected', 'mark_completed']
    
    @admin.action(description='Mark selected requests as Approved')
    def mark_approved(self, request, queryset):
        for subscription_request in queryset:
            if subscription_request.dealership:
                if 'premium' in subscription_request.subscription_type:
                    subscription_request.dealership.is_premium = True
                    subscription_request.dealership.save()
                subscription_request.status = 'approved'
                subscription_request.save()
        self.message_user(request, f"{queryset.count()} subscription request(s) approved.")
    
    @admin.action(description='Mark selected requests as Rejected')
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} subscription request(s) rejected.")
    
    @admin.action(description='Mark selected requests as Completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} subscription request(s) completed.")
