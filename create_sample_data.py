#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append('c:\\Users\\M.K.T\\Desktop\\FUTURE PLAN\\myproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Dealership, Car, UserProfile
from django.contrib.auth.models import User

def create_sample_data():
    # Create a sample user for the dealership
    try:
        user = User.objects.create_user(
            username="nairobi_auto",
            email="info@nairobiautohub.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )

        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            user_type="dealership",
            phone_number="+254 700 123 456"
        )

        # Create a sample dealership
        dealership = Dealership.objects.create(
            user=user,
            company_name="Nairobi Auto Hub",
            description="Your trusted partner for quality vehicles in Nairobi. We offer a wide range of cars with excellent customer service.",
            location="Nairobi",
            address="123 Moi Avenue, Nairobi, Kenya",
            phone_number="+254 700 123 456",
            email="info@nairobiautohub.com",
            website="https://nairobiautohub.com",
            latitude=-1.2864,
            longitude=36.8172
        )
        print(f"Created dealership: {dealership.company_name}")

        # Create a sample car
        car = Car.objects.create(
            dealership=dealership,
            make="Toyota",
            model="Corolla",
            year=2020,
            price=2500000,
            mileage=45000,
            fuel_type="petrol",
            transmission="automatic",
            condition="used",
            color="White",
            description="Well maintained Toyota Corolla with low mileage. Perfect for city driving.",
            features="Air conditioning, Power steering, Electric windows, Central locking"
        )
        print(f"Created car: {car.year} {car.make} {car.model}")

        print("Sample data created successfully!")
        print(f"Contact page URL: http://127.0.0.1:8000/dealership/{dealership.id}/contact/")

    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == "__main__":
    create_sample_data()