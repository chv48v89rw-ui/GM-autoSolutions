from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Exists, OuterRef
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import UserProfile, Dealership, Car, CarImage, Review, DealershipReview, Enquiry, Favorite
from .forms import (UserRegistrationForm, UserProfileForm, DealershipRegistrationForm,
                    CarForm, ReviewForm, DealershipReviewForm, EnquiryForm, CarSearchForm)
from django.conf import settings


def home(request):
    """Home page with search filters and featured cars"""
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.select_related('dealership').filter(is_sold=False, is_approved=True)  # Exclude sold cars and unapproved
    dealerships = Dealership.objects.filter(is_approved=True)  # Only show approved dealerships
    
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
        if form.cleaned_data.get('fuel_type'):
            cars = cars.filter(fuel_type=form.cleaned_data['fuel_type'])
        if form.cleaned_data.get('transmission'):
            cars = cars.filter(transmission=form.cleaned_data['transmission'])
        if form.cleaned_data.get('condition'):
            cars = cars.filter(condition=form.cleaned_data['condition'])
    
    # Get featured/recent cars
    featured_cars = cars[:12]
    
    context = {
        'form': form,
        'cars': cars,
        'featured_cars': featured_cars,
        'dealerships': dealerships,
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
            profile.save()
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'register.html', context)


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
    
    # Count enquiries for dealership's cars
    enquiries = Enquiry.objects.filter(car__dealership=dealership).order_by('-created_at')
    
    context = {
        'dealership': dealership,
        'cars': cars,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'enquiries': enquiries,
        'total_cars': cars.count(),
        'total_enquiries': enquiries.count(),
    }
    return render(request, 'dealership_dashboard.html', context)


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
                form.save()
                for image in images:
                    CarImage.objects.create(car=car, image=image)
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
        if form.cleaned_data.get('fuel_type'):
            cars = cars.filter(fuel_type=form.cleaned_data['fuel_type'])
        if form.cleaned_data.get('transmission'):
            cars = cars.filter(transmission=form.cleaned_data['transmission'])
        if form.cleaned_data.get('condition'):
            cars = cars.filter(condition=form.cleaned_data['condition'])
    
    context = {
        'form': form,
        'cars': cars,
    }
    return render(request, 'car_list.html', context)


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


def car_detail(request, car_id):
    """Car detail page"""
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    dealership = car.dealership
    dealership_reviews = dealership.reviews.all()
    dealership_rating = dealership_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.buyer = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
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
    gallery_images.extend([image.image for image in car.images.all()])

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, car=car).exists()

    car_features = [feature.strip() for feature in car.features.split(',')] if car.features else []
    
    context = {
        'car': car,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'dealership': dealership,
        'dealership_reviews': dealership_reviews,
        'dealership_rating': dealership_rating,
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'gallery_images': gallery_images,
        'is_favorited': is_favorited,
        'car_features': car_features,
    }
    return render(request, 'car_detail.html', context)


def dealership_detail(request, dealership_id):
    """Dealership detail page"""
    dealership = get_object_or_404(Dealership, id=dealership_id, is_approved=True)  # Only approved dealerships
    
    # Show all cars for dealership owner, only approved cars for others
    if request.user.is_authenticated and hasattr(request.user, 'dealership') and request.user.dealership == dealership:
        cars = dealership.cars.all()  # Show all cars including unapproved to owner
    else:
        cars = dealership.cars.filter(is_sold=False, is_approved=True)  # Exclude sold and unapproved cars for others
    
    reviews = dealership.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = DealershipReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dealership = dealership
            review.buyer = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('dealership_detail', dealership_id=dealership.id)
    else:
        form = DealershipReviewForm() if request.user.is_authenticated else None
    
    context = {
        'dealership': dealership,
        'cars': cars,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'dealership_detail.html', context)


def enquire_car(request, car_id):
    """Submit an enquiry for a car"""
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.car = car
            enquiry.save()
            messages.success(request, 'Your enquiry has been sent successfully!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = EnquiryForm()
    
    context = {'car': car, 'form': form}
    return render(request, 'enquire_car.html', context)


def dealerships_map(request):
    """Map view of all dealerships"""
    dealerships = Dealership.objects.filter(is_approved=True)  # Only approved dealerships
    context = {
        'dealerships': dealerships,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'dealerships_map.html', context)


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
                buyer_name=form.cleaned_data['buyer_name'],
                buyer_email=form.cleaned_data['buyer_email'],
                buyer_phone=form.cleaned_data['buyer_phone'],
                message=f"Subject: {request.POST.get('subject', 'General Inquiry')}\n\n{form.cleaned_data['message']}"
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
