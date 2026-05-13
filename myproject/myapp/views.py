from multiprocessing import context

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Exists, OuterRef
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
import secrets
from .models import UserProfile, Dealership, Car, CarImage, Review, DealershipReview, Enquiry, EnquiryMessage, Favorite, EmailVerification, Report, CarView, DealershipClick
from .forms import (UserRegistrationForm, UserProfileForm, DealershipRegistrationForm,
                    CarForm, ReviewForm, DealershipReviewForm, EnquiryForm, ConversationMessageForm, CarSearchForm, ReportForm)
from django.conf import settings
from .models import Dealership
from .utils import geocode_address


def send_verification_email(user, verification_code):
    """Send verification email to user"""
    subject = 'Verify Your Email - Car Dealership'
    message = f"""
    Hello {user.first_name},
    
    Welcome to Car Dealership! Please verify your email address using the code below:
    
    Verification Code: {verification_code}
    
    This code will expire in 24 hours.
    
    If you did not create this account, please ignore this email.
    
    Best regards,
    Car Dealership Team
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL or 'noreply@cardealership.com',
        [user.email],
        fail_silently=False,
    )


@login_required(login_url='login')
def home(request):
    """Home page with search filters and featured cars"""
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.select_related('dealership').filter(is_sold=False, is_approved=True)  # Exclude sold cars and unapproved
    dealerships = Dealership.objects.filter(is_approved=True)  # Only show approved dealerships
    premium_dealerships = dealerships.filter(is_premium=True).order_by('-rating')[:4]
    highlighted_dealerships = premium_dealerships if premium_dealerships.exists() else dealerships.order_by('-rating')[:4]
    premium_cars = Car.objects.select_related('dealership').filter(
        is_sold=False,
        is_approved=True,
        is_premium=True
    ).order_by('-created_at')[:8]
    
    # Search functionality
    if form.is_valid():
        if form.cleaned_data.get('make'):
            cars = cars.filter(make__icontains=form.cleaned_data['make'])
        if form.cleaned_data.get('model'):
            cars = cars.filter(model__icontains=form.cleaned_data['model'])
        if form.cleaned_data.get('year_from'):
            cars = cars.filter(year__gte=form.cleaned_data['year_from'])
        if form.cleaned_data.get('year_to'):
            cars = cars.filter(year__lte=form.cleaned_data['year_to'])
        if form.cleaned_data.get('price_from'):
            cars = cars.filter(price__gte=form.cleaned_data['price_from'])
        if form.cleaned_data.get('price_to'):
            cars = cars.filter(price__lte=form.cleaned_data['price_to'])
        if form.cleaned_data.get('mileage_from'):
            cars = cars.filter(mileage__gte=form.cleaned_data['mileage_from'])
        if form.cleaned_data.get('mileage_to'):
            cars = cars.filter(mileage__lte=form.cleaned_data['mileage_to'])
        if form.cleaned_data.get('fuel_type'):
            cars = cars.filter(fuel_type=form.cleaned_data['fuel_type'])
        if form.cleaned_data.get('transmission'):
            cars = cars.filter(transmission=form.cleaned_data['transmission'])
        if form.cleaned_data.get('condition'):
            cars = cars.filter(condition=form.cleaned_data['condition'])
        if form.cleaned_data.get('engine_size'):
            cars = cars.filter(engine_size=form.cleaned_data['engine_size'])
        if form.cleaned_data.get('doors'):
            cars = cars.filter(doors=form.cleaned_data['doors'])
        if form.cleaned_data.get('body_type'):
            cars = cars.filter(body_type=form.cleaned_data['body_type'])
        if form.cleaned_data.get('previous_owners'):
            cars = cars.filter(previous_owners=form.cleaned_data['previous_owners'])
        if form.cleaned_data.get('seats'):
            cars = cars.filter(seats__gte=form.cleaned_data['seats'])
    
    # Get featured/recent cars
    featured_cars = cars[:12]
    
    context = {
        'form': form,
        'cars': cars,
        'featured_cars': featured_cars,
        'dealerships': dealerships,
        'highlighted_dealerships': highlighted_dealerships,
        'best_cars': premium_cars,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'home.html', context)


def register(request):
    """User registration page"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Create user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_type = 'buyer'  # Explicitly set user type
            profile.save()
            
            # Send verification email for buyers
            try:
                verification_code = secrets.token_hex(3).upper()  # Generate 6-character code
                expires_at = timezone.now() + timedelta(hours=24)
                
                # Create or update verification record
                EmailVerification.objects.update_or_create(
                    user=user,
                    defaults={
                        'verification_code': verification_code,
                        'expires_at': expires_at
                    }
                )
                
                # Send email
                send_verification_email(user, verification_code)
                messages.success(request, 'Registration successful! A verification code has been sent to your email. Please verify your email to log in.')
                return redirect('verify_email')
            except Exception as e:
                messages.error(request, f'Registration successful, but failed to send verification email: {str(e)}. Please contact support.')
                return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'register.html', context)


def verify_email(request):
    """Email verification page"""
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code', '').strip()
        username = request.POST.get('username', '').strip()
        
        try:
            user = User.objects.get(username=username)
            email_verification = EmailVerification.objects.get(user=user)
            
            if email_verification.is_expired():
                messages.error(request, 'Verification code has expired. Please register again.')
                return redirect('register')
            
            if email_verification.verification_code == verification_code:
                # Mark user as verified
                profile = user.profile
                profile.is_verified = True
                profile.save()
                
                # Delete verification record
                email_verification.delete()
                
                messages.success(request, 'Email verified successfully! You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except EmailVerification.DoesNotExist:
            messages.error(request, 'No verification record found. Please register again.')
    
    return render(request, 'verify_email.html')


def dealership_register(request):
    """Dealership registration page"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        dealership_form = DealershipRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and dealership_form.is_valid():
            # Create user
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                user_type='dealership',
                phone_number=dealership_form.cleaned_data['phone_number']
            )
            
            # Create dealership
            dealership = dealership_form.save(commit=False)
            dealership.user = user
            dealership.is_approved = False  # Dealership needs approval
            
            # Try to geocode the address for precise coordinates
            # Build comprehensive address with area code for better precision
            address_parts = []
            if dealership.address:
                address_parts.append(dealership.address)
            if dealership.area_code:
                address_parts.append(f"Area Code: {dealership.area_code}")
            if dealership.location:
                address_parts.append(dealership.location)
            address_parts.append("Kenya")
            
            full_address = ", ".join(address_parts)
            lat, lon = geocode_address(full_address)
            if lat and lon:
                dealership.latitude = lat
                dealership.longitude = lon
                print(f"Geocoded '{dealership.company_name}' to coordinates: {lat}, {lon}")
            else:
                print(f"Failed to geocode address for '{dealership.company_name}': {full_address}")
            
            dealership.save()
            
            messages.success(request, 'Dealership registration successful! Your account will be reviewed and approved within 24 hours.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        dealership_form = DealershipRegistrationForm()
    
    context = {
        'user_form': user_form,
        'dealership_form': dealership_form,
    }
    return render(request, 'dealership_register.html', context)


def login_view(request):
    """Login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is a dealership and if they are approved
            try:
                if user.profile.user_type == 'dealership':
                    if not user.dealership.is_approved:
                        messages.error(request, 'Your dealership account is pending approval. Please contact the administrator.')
                        return redirect('login')
                # Check if buyer is verified
                elif user.profile.user_type == 'buyer':
                    if not user.profile.is_verified:
                        messages.error(request, 'Please verify your email first. Check your email for the verification code.')
                        return redirect('verify_email')
            except:
                pass
            
            login(request, user)
            # Redirect based on user type
            try:
                if user.profile.user_type == 'dealership':
                    return redirect('dealership_dashboard')
                else:
                    return redirect('buyer_dashboard')
            except:
                return redirect('buyer_dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def buyer_dashboard(request):
    """Buyer dashboard"""
    try:
        profile = request.user.profile
        if profile.user_type != 'buyer':
            return redirect('dealership_dashboard')
    except:
        messages.error(request, 'Profile not found. Please complete your registration.')
        return redirect('home')
    
    # Get user's enquiries
    enquiries = Enquiry.objects.filter(buyer_email=request.user.email).order_by('-created_at')
    
    # Get user's favorite cars
    favorites = Favorite.objects.filter(user=request.user).select_related('car__dealership').order_by('-created_at')
    
    context = {
        'enquiries': enquiries,
        'favorites': favorites,
        'profile': profile,
    }
    return render(request, 'buyer_dashboard.html', context)


@login_required(login_url='login')
def dealership_dashboard(request):
    """Dealership dashboard"""
    try:
        dealership = request.user.dealership
    except:
        messages.error(request, 'Dealership profile not found.')
        return redirect('home')
    
    cars = dealership.cars.all()
    reviews = dealership.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    enquiries = Enquiry.objects.filter(
        Q(dealership=dealership) | Q(car__dealership=dealership)
    ).order_by('-created_at')
    unread_enquiries = enquiries.filter(is_read=False).count()
    
    context = {
        'dealership': dealership,
        'cars': cars,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'enquiries': enquiries,
        'total_cars': cars.count(),
        'total_enquiries': enquiries.count(),
        'unread_enquiries': unread_enquiries,
    }
    return render(request, 'dealership_dashboard.html', context)


@login_required(login_url='login')
def dealership_analytics(request):
    """Dealership analytics dashboard"""
    try:
        dealership = request.user.dealership
    except:
        messages.error(request, 'Dealership profile not found.')
        return redirect('home')
    
    # Get dealership cars
    cars = dealership.cars.all()
    
    # Most viewed car analytics
    car_views = {}
    total_car_views = 0
    
    for car in cars:
        views_count = CarView.objects.filter(car=car).count()
        car_views[car.id] = {
            'car': car,
            'views': views_count,
            'percentage': 0  # Will calculate after getting total
        }
        total_car_views += views_count
    
    # Calculate percentages and find most viewed
    most_viewed_car = None
    max_views = 0
    
    for car_data in car_views.values():
        if total_car_views > 0:
            car_data['percentage'] = round((car_data['views'] / total_car_views) * 100, 1)
        
        if car_data['views'] > max_views:
            max_views = car_data['views']
            most_viewed_car = car_data['car']
    
    # Sort cars by views (descending)
    sorted_car_views = sorted(car_views.values(), key=lambda x: x['views'], reverse=True)
    
    # Click analytics
    click_stats = {}
    total_clicks = 0
    
    # Get all click types
    click_types = dict(DealershipClick.CLICK_TYPES)
    
    for click_type, display_name in click_types.items():
        count = DealershipClick.objects.filter(dealership=dealership, click_type=click_type).count()
        click_stats[click_type] = {
            'name': display_name,
            'count': count,
            'percentage': 0  # Will calculate after getting total
        }
        total_clicks += count
    
    # Calculate percentages
    for click_data in click_stats.values():
        if total_clicks > 0:
            click_data['percentage'] = round((click_data['count'] / total_clicks) * 100, 1)
    
    # Recent activity (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    recent_views = CarView.objects.filter(
        car__dealership=dealership,
        viewed_at__gte=thirty_days_ago
    ).count()
    
    recent_clicks = DealershipClick.objects.filter(
        dealership=dealership,
        clicked_at__gte=thirty_days_ago
    ).count()
    
    # Top performing cars (by views) - last 30 days
    top_cars_30_days = []
    for car in cars:
        views_30_days = CarView.objects.filter(
            car=car,
            viewed_at__gte=thirty_days_ago
        ).count()
        if views_30_days > 0:
            top_cars_30_days.append({
                'car': car,
                'views': views_30_days
            })
    
    top_cars_30_days.sort(key=lambda x: x['views'], reverse=True)
    top_cars_30_days = top_cars_30_days[:5]  # Top 5
    
    context = {
        'dealership': dealership,
        'most_viewed_car': most_viewed_car,
        'max_views': max_views,
        'total_car_views': total_car_views,
        'sorted_car_views': sorted_car_views,
        'click_stats': click_stats,
        'total_clicks': total_clicks,
        'recent_views': recent_views,
        'recent_clicks': recent_clicks,
        'top_cars_30_days': top_cars_30_days,
        'total_cars': cars.count(),
    }
    
    return render(request, 'dealership_analytics.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def submit_cars_for_review(request):
    """Submit selected cars for admin review"""
    try:
        dealership = request.user.dealership
    except:
        messages.error(request, 'Only dealerships can submit cars for review.')
        return redirect('home')
    
    # Get selected car IDs from POST data
    selected_car_ids = request.POST.getlist('selected_cars[]')
    
    if not selected_car_ids:
        messages.warning(request, 'Please select at least one car to submit.')
        return redirect('dealership_dashboard')
    
    try:
        # Update the selected cars
        cars = Car.objects.filter(id__in=selected_car_ids, dealership=dealership)
        count = cars.update(submitted_for_review=True, submitted_at=timezone.now())
        
        messages.success(request, f'{count} car(s) submitted for admin review. The admin team will review and approve them shortly.')
    except Exception as e:
        messages.error(request, f'Error submitting cars: {str(e)}')
    
    return redirect('dealership_dashboard')


@login_required(login_url='login')
def add_car(request):
    """Add new car listing (dealership only)"""
    try:
        dealership = request.user.dealership
    except:
        messages.error(request, 'Only dealerships can add cars.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if form.is_valid():
            if len(images) > 15:
                form.add_error('images', 'You can upload up to 15 images only.')
            else:
                car = form.save(commit=False)
                car.dealership = dealership
                car.is_approved = True
                car.save()

                for image in images:
                    CarImage.objects.create(car=car, image=image)

                messages.success(request, 'Car added successfully!')
                return redirect('dealership_dashboard')
    else:
        form = CarForm()
    
    context = {'form': form}
    return render(request, 'add_car.html', context)


@login_required(login_url='login')
def edit_car(request, car_id):
    """Edit car listing (dealership only)"""
    car = get_object_or_404(Car, id=car_id)
    
    # Check if user owns this car
    if car.dealership.user != request.user:
        messages.error(request, 'You cannot edit this car.')
        return redirect('dealership_dashboard')
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        images = request.FILES.getlist('images')
        if form.is_valid():
            if len(images) > 15:
                form.add_error('images', 'You can upload up to 15 images only.')
            else:
                updated_car = form.save(commit=False)
                updated_car.is_approved = True
                updated_car.save()
                for image in images:
                    CarImage.objects.create(car=updated_car, image=image)
                messages.success(request, 'Car updated successfully!')
                return redirect('dealership_dashboard')
    else:
        form = CarForm(instance=car)
    
    context = {'form': form, 'car': car}
    return render(request, 'edit_car.html', context)


@login_required(login_url='login')
def delete_car(request, car_id):
    """Delete car listing (dealership only)"""
    car = get_object_or_404(Car, id=car_id)
    
    if car.dealership.user != request.user:
        messages.error(request, 'You cannot delete this car.')
        return redirect('dealership_dashboard')
    
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car deleted successfully!')
        return redirect('dealership_dashboard')
    
    context = {'car': car}
    return render(request, 'confirm_delete.html', context)


@login_required(login_url='login')
def car_list(request):
    """List all cars with filters"""
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.select_related('dealership').filter(is_sold=False, is_approved=True)  # Exclude sold cars and unapproved
    
    if request.user.is_authenticated:
        cars = cars.annotate(is_favorited=Exists(Favorite.objects.filter(user=request.user, car=OuterRef('pk'))))
    
    if form.is_valid():
        if form.cleaned_data.get('make'):
            cars = cars.filter(make__icontains=form.cleaned_data['make'])
        if form.cleaned_data.get('model'):
            cars = cars.filter(model__icontains=form.cleaned_data['model'])
        if form.cleaned_data.get('year_from'):
            cars = cars.filter(year__gte=form.cleaned_data['year_from'])
        if form.cleaned_data.get('year_to'):
            cars = cars.filter(year__lte=form.cleaned_data['year_to'])
        if form.cleaned_data.get('price_from'):
            cars = cars.filter(price__gte=form.cleaned_data['price_from'])
        if form.cleaned_data.get('price_to'):
            cars = cars.filter(price__lte=form.cleaned_data['price_to'])
        if form.cleaned_data.get('mileage_from'):
            cars = cars.filter(mileage__gte=form.cleaned_data['mileage_from'])
        if form.cleaned_data.get('mileage_to'):
            cars = cars.filter(mileage__lte=form.cleaned_data['mileage_to'])
        if form.cleaned_data.get('fuel_type'):
            cars = cars.filter(fuel_type=form.cleaned_data['fuel_type'])
        if form.cleaned_data.get('transmission'):
            cars = cars.filter(transmission=form.cleaned_data['transmission'])
        if form.cleaned_data.get('condition'):
            cars = cars.filter(condition=form.cleaned_data['condition'])
        if form.cleaned_data.get('engine_size'):
            cars = cars.filter(engine_size=form.cleaned_data['engine_size'])
        if form.cleaned_data.get('doors'):
            cars = cars.filter(doors=form.cleaned_data['doors'])
        if form.cleaned_data.get('body_type'):
            cars = cars.filter(body_type=form.cleaned_data['body_type'])
        if form.cleaned_data.get('previous_owners'):
            cars = cars.filter(previous_owners=form.cleaned_data['previous_owners'])
        if form.cleaned_data.get('seats'):
            cars = cars.filter(seats__gte=form.cleaned_data['seats'])
    
    context = {
        'form': form,
        'cars': cars,
    }
    return render(request, 'car_list.html', context)

@login_required(login_url='login')

def terms(request):
    return render(request, 'terms.html')
@login_required(login_url='login')


@login_required(login_url='login')
def privacy(request):
    return render(request, 'privacy.html')


@login_required(login_url='login')
def report_car(request, car_id):
    """Report a car listing"""
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.car = car
            report.save()
            messages.success(request, 'Your report has been submitted successfully. Our team will review it.')
            return redirect('car_detail', car_id=car_id)
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'car': car,
        'report_type': 'car',
    }
    return render(request, 'report.html', context)


@login_required(login_url='login')
def report_dealership(request, dealership_id):
    """Report a dealership"""
    dealership = get_object_or_404(Dealership, id=dealership_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.dealership = dealership
            report.save()
            messages.success(request, 'Your report has been submitted successfully. Our team will review it.')
            return redirect('dealership_detail', dealership_id=dealership_id)
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'dealership': dealership,
        'report_type': 'dealership',
    }
    return render(request, 'report.html', context)


@login_required(login_url='login')
def report_user(request, user_id):
    """Report a user"""
    reported_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.save()
            messages.success(request, 'Your report has been submitted successfully. Our team will review it.')
            return redirect('home')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'reported_user': reported_user,
        'report_type': 'user',
    }
    return render(request, 'report.html', context)

def general_report(request):
    """General reporting interface for all types of issues"""
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            
            # Set the appropriate item based on selection
            item_type = form.cleaned_data.get('item_type')
            if item_type == 'car':
                car_id = form.cleaned_data.get('car_id')
                if car_id:
                    report.car = Car.objects.get(id=car_id)
            elif item_type == 'dealership':
                dealership_id = form.cleaned_data.get('dealership_id')
                if dealership_id:
                    report.dealership = Dealership.objects.get(id=dealership_id)
            elif item_type == 'user':
                username = form.cleaned_data.get('reported_user_username')
                if username:
                    from django.contrib.auth.models import User
                    try:
                        reported_user = User.objects.get(username=username)
                        report.reported_user = reported_user
                    except User.DoesNotExist:
                        messages.error(request, 'User not found with that username.')
                        return render(request, 'report.html', {
                            'form': form,
                            'cars': Car.objects.all(),
                            'dealerships': Dealership.objects.all(),
                            'report_type': 'general'
                        })
            
            report.save()
            messages.success(request, 'Your report has been submitted successfully! Our admin team will review it.')
            return redirect('home')
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'cars': Car.objects.all(),
        'dealerships': Dealership.objects.all(),
        'report_type': 'general'
    }
    return render(request, 'report.html', context)


@login_required(login_url='login')
def my_reports(request):
    """View user's submitted reports"""
    reports = Report.objects.filter(reporter=request.user).order_by('-created_at')
    
    context = {
        'reports': reports,
    }
    return render(request, 'my_reports.html', context)


def pricing_page(request):
    """Pricing page with dealership-only access control"""
    # Check if user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view pricing plans.')
        return redirect('login')
    
    # Check if user has dealership profile
    try:
        dealership = request.user.dealership
        context = {
            'dealership': dealership,
        }
        return render(request, 'pricing.html', context)
    except:
        # User doesn't have dealership profile
        messages.error(request, 'Pricing plans are only available for dealership accounts.')
        return redirect('dealership-register')


def pricing_subscribe(request, plan):
    """Create a quick subscription request from the pricing page."""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to request a subscription plan.')
        return redirect('login')

    try:
        dealership = request.user.dealership
    except:
        messages.error(request, 'Only dealership accounts can request subscription plans.')
        return redirect('dealership-register')

    if request.method != 'POST':
        messages.error(request, 'Invalid request method for subscription plan selection.')
        return redirect('pricing')

    from .models import SubscriptionRequest

    contact_person = request.user.get_full_name() or request.user.username
    subscription_type = plan
    message = 'Subscription request created from pricing page quick link.'

    SubscriptionRequest.objects.create(
        company_name=dealership.company_name,
        contact_person=contact_person,
        email=dealership.email,
        phone=dealership.phone_number,
        subscription_type=subscription_type,
        message=message,
        dealership=dealership
    )

    messages.success(request, 'Your subscription request has been received and will be reviewed. We will get back to you within 24 hours.')
    return redirect('pricing')


def subscription_request(request):
    """Handle subscription requests from users"""
    from .models import SubscriptionRequest
    
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subscription_type = request.POST.get('subscription_type')
        message = request.POST.get('message', '')
        terms = request.POST.get('terms')
        
        # Validate required fields
        if not all([company_name, contact_person, email, phone, subscription_type, terms]):
            return JsonResponse({'success': False, 'error': 'Please fill in all required fields.'})
        
        # Create subscription request record
        subscription_request = SubscriptionRequest.objects.create(
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            subscription_type=subscription_type,
            message=message
        )
        
        return JsonResponse({
            'success': True, 
            'message': 'Your subscription request has been received and is currently under review. Please wait 24 hours for processing. We will contact you at your provided email address with the decision.'
        })
    
    return JsonResponse({'success': False, 'error': 'Only POST requests allowed.'})


def get_models_for_make(request):
    """API endpoint to get models for a selected make"""
    from .models import Car
    
    make = request.GET.get('make', '')
    if make:
        models = Car.objects.filter(make=make).values_list('model', flat=True).distinct().order_by('model')
        model_list = [{'value': model, 'label': model} for model in models]
        return JsonResponse({'models': model_list})
    else:
        return JsonResponse({'models': []})


def get_dealerships_json(request):
    dealerships = Dealership.objects.filter(is_approved=True).values(
        'id',
        'company_name',
        'location',
        'latitude',
        'longitude',
        'rating'
    )
    data = []
    for dealership in dealerships:
        data.append({
            'id': dealership['id'],
            'name': dealership['company_name'],
            'location': dealership['location'],
            'lat': dealership['latitude'],
            'lng': dealership['longitude'],
            'rating': dealership['rating'] or 0,
            'url': f"/dealership/{dealership['id']}/",
        })
    return JsonResponse(data, safe=False)


@login_required(login_url='login')
def your_view_name(request):
    return JsonResponse(data, safe=False)


@login_required(login_url='login')
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Track car view for analytics
    CarView.objects.create(
        car=car,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    reviews = car.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    dealership = car.dealership
    dealership_reviews = dealership.reviews.filter(is_approved=True)
    dealership_rating = dealership_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.buyer = request.user
            review.save()
            messages.success(request, 'Review submitted successfully! It will be visible to other users once approved by our admin team.')
            return redirect('car_detail', car_id=car.id)
    else:
        form = ReviewForm() if request.user.is_authenticated else None

    gallery_images = []
    if car.main_image:
        gallery_images.append(car.main_image)
    if car.image2:
        gallery_images.append(car.image2)
    if car.image3:
        gallery_images.append(car.image3)
    if car.image4:
        gallery_images.append(car.image4)

    gallery_images += [img.image for img in car.images.all()]

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, car=car).exists()

    car_features = car.features.split(',') if car.features else []

    context = {
        'car': car,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'dealership': dealership,
        'dealership_reviews': dealership_reviews,
        'dealership_rating': dealership_rating,
        'form': form,
        'gallery_images': gallery_images,
        'is_favorited': is_favorited,
        'car_features': car_features,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    return render(request, 'car_detail.html', context)


def dealership_detail(request, dealership_id):
    dealership = get_object_or_404(Dealership, id=dealership_id, is_approved=True)

    if request.user.is_authenticated and hasattr(request.user, 'dealership') and request.user.dealership == dealership:
        cars = dealership.cars.all()
    else:
        cars = dealership.cars.filter(is_sold=False, is_approved=True)

    reviews = dealership.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    form = None
    if request.user.is_authenticated:
        form = DealershipReviewForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            review = form.save(commit=False)
            review.dealership = dealership
            review.buyer = request.user
            review.save()
            messages.success(request, 'Review submitted successfully! It will be visible to other users once approved by our admin team.')
            return redirect('dealership_detail', dealership_id=dealership.id)

    context = {
        'dealership': dealership,
        'cars': cars,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    return render(request, 'dealership_detail.html', context)


def track_dealership_click(request, dealership_id):
    """Track dealership clicks for analytics"""
    dealership = get_object_or_404(Dealership, id=dealership_id)
    click_type = request.GET.get('type', 'contact')

    # Validate click type
    valid_types = [choice[0] for choice in DealershipClick.CLICK_TYPES]
    if click_type not in valid_types:
        click_type = 'contact'

    # Create click record
    DealershipClick.objects.create(
        dealership=dealership,
        click_type=click_type,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    # Return appropriate response based on click type
    if click_type == 'phone':
        return JsonResponse({'success': True, 'phone': dealership.phone_number})
    elif click_type == 'email':
        return JsonResponse({'success': True, 'email': dealership.email})
    elif click_type == 'website':
        return JsonResponse({'success': True, 'website': dealership.website})
    else:
        return JsonResponse({'success': True})


def enquire_car(request, car_id):
    """Submit an enquiry for a car"""
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.dealership = car.dealership
            enquiry.save()
            EnquiryMessage.objects.create(
                enquiry=enquiry,
                sender_type='buyer',
                sender_name=enquiry.buyer_name,
                message=enquiry.message,
            )
            messages.success(request, 'Your enquiry has been sent successfully!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = EnquiryForm()
    
    context = {'car': car, 'form': form}
    return render(request, 'enquire_car.html', context)


@login_required(login_url='login')
def enquiry_conversation(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    user = request.user
    is_dealership = hasattr(user, 'dealership') and (
        (enquiry.dealership and enquiry.dealership.user == user) or
        (enquiry.car and enquiry.car.dealership.user == user)
    )
    is_buyer = hasattr(user, 'profile') and user.profile.user_type == 'buyer' and enquiry.buyer_email == user.email

    if not (is_dealership or is_buyer):
        return redirect('home')

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message_text = form.cleaned_data['message']
            sender_name = enquiry.dealership.company_name if is_dealership else enquiry.buyer_name
            EnquiryMessage.objects.create(
                enquiry=enquiry,
                sender_type='dealership' if is_dealership else 'buyer',
                sender_name=sender_name,
                message=message_text,
            )

            if is_dealership:
                enquiry.dealership_response = message_text
                enquiry.responded_at = timezone.now()
                enquiry.is_read = True
            else:
                enquiry.is_read = False

            enquiry.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('view_enquiry', enquiry_id=enquiry.id)
    else:
        form = ConversationMessageForm()

    messages_list = enquiry.messages.order_by('created_at')
    last_message = messages_list.last()
    is_waiting_reply = last_message and last_message.sender_type == 'buyer'

    context = {
        'enquiry': enquiry,
        'messages': messages_list,
        'form': form,
        'is_dealership': is_dealership,
        'is_buyer': is_buyer,
        'is_waiting_reply': is_waiting_reply,
    }
    return render(request, 'view_enquiry.html', context)


@login_required(login_url='login')
@login_required(login_url='login')
def view_enquiry(request, enquiry_id):
    return enquiry_conversation(request, enquiry_id)




@login_required(login_url='login')
def dealerships_map(request):
    dealerships = Dealership.objects.filter(is_approved=True).only(
        'id', 'company_name', 'location', 'address', 'phone_number', 'email',
        'area_code', 'latitude', 'longitude', 'is_premium'
    )

    # Convert to JSON for JavaScript
    dealerships_json = json.dumps([
        {
            'id': d.id,
            'company_name': d.company_name,
            'location': d.location,
            'address': d.address,
            'phone_number': d.phone_number,
            'email': d.email,
            'area_code': d.area_code,
            'latitude': float(d.latitude) if d.latitude else None,
            'longitude': float(d.longitude) if d.longitude else None,
            'is_premium': d.is_premium
        } for d in dealerships
    ])

    return render(request, 'dealerships_map.html', {
        'dealerships': dealerships,
        'dealerships_json': dealerships_json
    })



def contact_dealership(request, dealership_id):
    """Contact page for a specific dealership"""
    dealership = get_object_or_404(Dealership, id=dealership_id, is_approved=True)  # Only approved dealerships
    reviews = dealership.reviews.all()
    dealership_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            # Create a general enquiry (not tied to a specific car)
            enquiry = Enquiry.objects.create(
                car=None,  # No specific car for general contact
                dealership=dealership,
                buyer_name=form.cleaned_data['buyer_name'],
                buyer_email=form.cleaned_data['buyer_email'],
                buyer_phone=form.cleaned_data['buyer_phone'],
                message=f"Subject: {request.POST.get('subject', 'General Inquiry')}\n\n{form.cleaned_data['message']}"
            )
            EnquiryMessage.objects.create(
                enquiry=enquiry,
                sender_type='buyer',
                sender_name=enquiry.buyer_name,
                message=enquiry.message,
            )
            messages.success(request, f'Your message has been sent to {dealership.company_name}! They will get back to you soon.')
            return redirect('contact_dealership', dealership_id=dealership.id)
    else:
        form = EnquiryForm()
    
    context = {
        'dealership': dealership,
        'reviews': reviews,
        'dealership_rating': dealership_rating,
        'form': form,
    }
    return render(request, 'contact.html', context)


@login_required(login_url='login')
def add_to_favorites(request, car_id):
    """Add car to user's favorites"""
    car = get_object_or_404(Car, id=car_id)
    
    # Check if already favorited
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        car=car
    )
    
    if created:
        messages.success(request, f'{car.year} {car.make} {car.model} added to your favorites!')
    else:
        messages.info(request, 'This car is already in your favorites.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def remove_from_favorites(request, car_id):
    """Remove car from user's favorites"""
    car = get_object_or_404(Car, id=car_id)
    
    try:
        favorite = Favorite.objects.get(user=request.user, car=car)
        favorite.delete()
        messages.success(request, f'{car.year} {car.make} {car.model} removed from your favorites.')
    except Favorite.DoesNotExist:
        messages.error(request, 'This car is not in your favorites.')
    
    return redirect(request.META.get('HTTP_REFERER', 'buyer_dashboard'))


@login_required(login_url='login')
def mark_car_sold(request, car_id):
    """Mark car as sold (dealership only)"""
    car = get_object_or_404(Car, id=car_id)
    
    # Check if user owns this car
    if car.dealership.user != request.user:
        messages.error(request, 'You cannot modify this car.')
        return redirect('dealership_dashboard')
    
    if request.method == 'POST':
        car.is_sold = True
        car.save()
        messages.success(request, f'{car.year} {car.make} {car.model} marked as sold!')
    
    return redirect('dealership_dashboard')


# Admin views for dealership approval
@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard for managing dealership approvals"""
    # Check if user is admin (you may want to add an is_admin field to User model)
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Dealership data
    pending_dealerships = Dealership.objects.filter(is_approved=False).order_by('-created_at')
    approved_dealerships = Dealership.objects.filter(is_approved=True).order_by('-created_at')
    
    # Reports data
    reports = Report.objects.all().order_by('-created_at')
    pending_reports = reports.filter(status='pending')
    
    # Subscription requests data
    from .models import SubscriptionRequest
    subscription_requests = SubscriptionRequest.objects.all().order_by('-created_at')
    pending_subscriptions = subscription_requests.filter(status='pending')
    
    context = {
        'pending_dealerships': pending_dealerships,
        'approved_dealerships': approved_dealerships,
        'pending_count': pending_dealerships.count(),
        'approved_count': approved_dealerships.count(),
        'reports': reports,
        'pending_reports_count': pending_reports.count(),
        'subscription_requests': subscription_requests,
        'pending_subscriptions_count': pending_subscriptions.count(),
    }
    return render(request, 'admin/dashboard.html', context)


@login_required(login_url='login')
def approve_dealership(request, dealership_id):
    """Approve a dealership registration"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    dealership = get_object_or_404(Dealership, id=dealership_id)
    dealership.is_approved = True
    dealership.save()
    
    messages.success(request, f'{dealership.company_name} has been approved!')
    return redirect('admin_dashboard')


@login_required(login_url='login')
def reject_dealership(request, dealership_id):
    """Reject a dealership registration"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    dealership = get_object_or_404(Dealership, id=dealership_id)
    dealership_name = dealership.company_name
    dealership.delete()  # Delete the dealership and associated user
    
    messages.success(request, f'{dealership_name} has been rejected and removed.')
    return redirect('admin_dashboard')

# Report management views
@login_required(login_url='login')
def update_report_status(request, report_id):
    """Update report status (AJAX endpoint)"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    try:
        report = Report.objects.get(id=report_id)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'under_review', 'resolved']:
            report.status = new_status
            report.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)
            
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
