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
    path('verify-email/', views.verify_email, name='verify_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
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
    
    # API endpoints
    path('api/subscription-request/', views.subscription_request, name='subscription_request'),
    path('api/models-for-make/', views.get_models_for_make, name='api_models_for_make'),
    path('api/dealerships/', views.get_dealerships_json, name='api_dealerships'),
    
    # Admin
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve-dealership/<int:dealership_id>/', views.approve_dealership, name='approve_dealership'),
    path('admin/reject-dealership/<int:dealership_id>/', views.reject_dealership, name='reject_dealership'),
    path('admin/update-report/<int:report_id>/', views.update_report_status, name='update_report_status'),
]
