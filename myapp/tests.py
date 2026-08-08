from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Car, Dealership
from .services.car_search_service import get_car_recommendations_context
from django.contrib.auth.models import User


class CarSearchServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dealer', email='dealer@example.com', password='pass1234')
        self.dealership = Dealership.objects.create(
            user=self.user,
            company_name='GM Motors',
            description='Reliable dealership',
            email='info@gmmotors.example',
            phone_number='0712345678',
            location='Nairobi',
            address='Nairobi CBD',
            business_certificate=SimpleUploadedFile('certificate.pdf', b'certificate', content_type='application/pdf'),
            is_approved=True,
            is_verified=True,
            rating=4.8,
        )

    def test_get_car_recommendations_context_matches_feature_and_inventory_code(self):
        Car.objects.create(
            dealership=self.dealership,
            title='2021 Toyota Prado',
            inventory_code='GM1234',
            make='Toyota',
            model='Prado',
            variant='TX',
            year=2021,
            price=Decimal('4500000.00'),
            mileage=12000,
            fuel_type='diesel',
            transmission='automatic',
            condition='used_locally',
            color='White',
            exterior_color='Pearl White',
            interior_color='Black',
            seat_material='Leather',
            interior_trim='Wood',
            seats=7,
            engine_size='2.8',
            doors=4,
            body_type='suv',
            previous_owners=1,
            number_of_keys=2,
            fuel_economy_combined='12',
            description='Very clean family SUV with full service history.',
            features='Sunroof, Leather Seats, Parking Sensors, Reverse Camera',
            is_approved=True,
            is_sold=False,
        )

        context = get_car_recommendations_context('sunroof and inventory code GM1234')

        self.assertIn('GM1234', context)
        self.assertIn('Sunroof', context)
        self.assertIn('Toyota', context)
        self.assertIn('Prado', context)
