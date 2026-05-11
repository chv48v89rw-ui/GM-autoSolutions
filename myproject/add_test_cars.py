#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('c:\\Users\\M.K.T\\Desktop\\FUTURE PLAN\\myproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Dealership, Car
import random

def add_test_cars():
    """Add 100 test cars with varied data"""
    
    # Get dealerships
    dealerships = list(Dealership.objects.all())
    
    if not dealerships:
        print("No dealerships found. Please create a dealership first.")
        return
    
    # Car data
    makes = ['Toyota', 'Honda', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Mazda', 'Nissan', 'Hyundai', 'Kia', 'Ford', 'Chevrolet', 'Tesla', 'Subaru', 'Lexus']
    models = ['Corolla', 'Civic', '3 Series', 'C-Class', 'A4', 'Golf', 'CX-5', 'Altima', 'Elantra', 'Sportage', 'Focus', 'Malibu', 'Model 3', 'Outback', 'RX']
    colors = ['White', 'Black', 'Silver', 'Gray', 'Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Brown']
    fuel_types = ['petrol', 'diesel', 'hybrid', 'electric']
    transmissions = ['manual', 'automatic']
    conditions = ['new', 'used']
    
    descriptions = [
        'Well-maintained vehicle with excellent condition',
        'Perfect for city driving and commuting',
        'Low mileage, one owner vehicle',
        'Recently serviced, ready to go',
        'Great fuel efficiency, reliable car',
        'Spacious interior, comfortable ride',
        'Advanced safety features',
        'Modern technology and infotainment',
        'Excellent performance and handling',
        'Family-friendly vehicle with ample space',
    ]
    
    features_list = [
        'Air conditioning, Power steering, Electric windows',
        'ABS, Power steering, Air conditioning, Central locking',
        'Power steering, Electric windows, Sunroof, Leather seats',
        'Air conditioning, Bluetooth, USB port, Cruise control',
        'Power steering, Electric windows, Backup camera, Navigation',
        'ABS, Power steering, Electric windows, Keyless entry',
        'Air conditioning, Bluetooth, Navigation, Sunroof',
        'Power steering, Electric windows, Heated seats, Parking sensors',
        'Air conditioning, Bluetooth, Lane assist, Cruise control',
        'Power steering, Electric windows, Panoramic roof, Premium audio',
    ]
    
    cars = []
    
    print(f"Creating 100 cars across {len(dealerships)} dealership(s)...")
    
    for i in range(1, 101):
        dealership = random.choice(dealerships)
        make = random.choice(makes)
        model = random.choice(models)
        year = random.randint(2015, 2024)
        price = random.randint(500000, 20000000)
        mileage = random.randint(5000, 250000)
        fuel_type = random.choice(fuel_types)
        transmission = random.choice(transmissions)
        condition = random.choice(conditions)
        color = random.choice(colors)
        seats = random.choice([5, 7, 8])
        description = random.choice(descriptions)
        features = random.choice(features_list)
        
        car = Car(
            dealership=dealership,
            title=f"{year} {make} {model}",
            make=make,
            model=model,
            year=year,
            price=price,
            mileage=mileage,
            fuel_type=fuel_type,
            transmission=transmission,
            condition=condition,
            color=color,
            seats=seats,
            description=description,
            features=features,
            is_approved=True,  # Approve all test cars so they appear on the site
            is_sold=False
        )
        cars.append(car)
        
        if i % 10 == 0:
            print(f"  Generated {i} cars...")
    
    # Bulk create all cars
    Car.objects.bulk_create(cars)
    
    print(f"\nSuccessfully created 100 test cars!")
    print(f"Total cars in database: {Car.objects.count()}")

if __name__ == "__main__":
    add_test_cars()
