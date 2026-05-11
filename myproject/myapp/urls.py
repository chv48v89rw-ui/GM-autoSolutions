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
    
    # Authentication
    path('register/', views.register, name='register'),
    path('dealership-register/', views.dealership_register, name='dealership_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/dealership/', views.dealership_dashboard, name='dealership_dashboard'),
    
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
    
    # API endpoints
    path('api/dealerships/', views.get_dealerships_json, name='api_dealerships'),
]
