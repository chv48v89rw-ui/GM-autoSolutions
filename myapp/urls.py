from django.urls import path
from . import views

urlpatterns = [
    # Home and general
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('dealerships/', views.dealerships_map, name='dealerships_map'),
    path('dealership/<int:dealership_id>/', views.dealership_detail, name='dealership_detail'),
    path('dealership/<int:dealership_id>/contact/', views.contact_dealership, name='contact_dealership'),
    path('dealership/<int:dealership_id>/track-click/', views.track_dealership_click, name='track_dealership_click'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('dealership-register/', views.dealership_register, name='dealership_register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('edit-dealership/', views.edit_dealership_profile, name='edit_dealership'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    
    # Dashboards
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/dealership/', views.dealership_dashboard, name='dealership_dashboard'),
    path('dashboard/dealership/analytics/', views.dealership_analytics, name='dealership_analytics'),
    path('dashboard/dealership/submit-cars/', views.submit_cars_for_review, name='submit_cars_for_review'),
    
    # Car management
    path('car/add/', views.add_car, name='add_car'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('car/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('car/<int:car_id>/mark-sold/', views.mark_car_sold, name='mark_car_sold'),
    
    # Favorites
    path('car/<int:car_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('car/<int:car_id>/unfavorite/', views.remove_from_favorites, name='remove_from_favorites'),
    
    # Enquiry and reviews
    path('car/<int:car_id>/enquire/', views.enquire_car, name='enquire_car'),
    path('enquiry/<int:enquiry_id>/reply/', views.enquiry_conversation, name='reply_enquiry'),
    path('enquiry/<int:enquiry_id>/view/', views.view_enquiry, name='view_enquiry'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    
    # Reporting
    path('report/', views.general_report, name='general_report'),
    path('car/<int:car_id>/report/', views.report_car, name='report_car'),
    path('dealership/<int:dealership_id>/report/', views.report_dealership, name='report_dealership'),
    path('user/<int:user_id>/report/', views.report_user, name='report_user'),
    path('my-reports/', views.my_reports, name='my_reports'),
    
    # Pricing
    path('pricing/', views.pricing_page, name='pricing'),
    path('pricing/subscribe/<str:plan>/', views.pricing_subscribe, name='pricing_subscribe'),
    path('pricing/choose-car/', views.pricing_choose_car, name='pricing_choose_car'),
    
    # API endpoints
    path('api/subscription-request/', views.subscription_request, name='subscription_request'),
    path('api/models-for-make/', views.get_models_for_make, name='api_models_for_make'),
    path('api/dealerships/', views.get_dealerships_json, name='api_dealerships'),
    
    # Admin
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve-dealership/<int:dealership_id>/', views.approve_dealership, name='approve_dealership'),
    path('admin/reject-dealership/<int:dealership_id>/', views.reject_dealership, name='reject_dealership'),
    path('admin/update-report/<int:report_id>/', views.update_report_status, name='update_report_status'),
    
    # Feature #5: Advanced Search & Filters
    path('saved-searches/', views.saved_searches, name='saved_searches'),
    path('saved-search/<int:search_id>/apply/', views.apply_saved_search, name='apply_saved_search'),
    path('saved-search/<int:search_id>/delete/', views.delete_saved_search, name='delete_saved_search'),
    
    # Feature #6: Car Comparison
    path('comparison/add/<int:car_id>/', views.add_to_comparison, name='add_to_comparison'),
    path('comparison/remove/<int:car_id>/', views.remove_from_comparison, name='remove_from_comparison'),
    path('comparison/', views.view_comparison, name='view_comparison'),
    
    # Feature #7: Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/preferences/', views.notification_preferences, name='notification_preferences'),

    # AI Chat Assistant
    path('api/ai-chat/', views.ai_chat),
    path('aichat/', views.chat_page, name='aichat'),
    path('chat/', views.chat_page, name='chat_page'),

]

