import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import Car, Dealership

class Command(BaseCommand):
    help = 'Generate 100 test cars for development and filtering testing'

    def handle(self, *args, **options):
        # Get all dealerships or create one if none exist
        dealerships = Dealership.objects.all()
        if not dealerships.exists():
            self.stdout.write(self.style.WARNING('No dealerships found. Please create a dealership first.'))
            return

        makes = ['Toyota', 'Honda', 'BMW', 'Mercedes-Benz', 'Audi', 'Lexus', 'Volkswagen', 
                 'Ford', 'Chevrolet', 'Hyundai', 'Kia', 'Nissan', 'Mazda', 'Subaru', 'Volvo']
        
        models_by_make = {
            'Toyota': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Yaris', 'Vios', 'Matrix'],
            'Honda': ['Accord', 'Civic', 'CR-V', 'Pilot', 'Jazz', 'Odyssey', 'HR-V'],
            'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series', 'M3', '1 Series'],
            'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'A-Class'],
            'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5', 'Q7', 'A1'],
            'Lexus': ['ES', 'IS', 'RX', 'NX', 'UX', 'GS'],
            'Volkswagen': ['Jetta', 'Passat', 'Tiguan', 'Golf', 'Polo', 'Beetle'],
            'Ford': ['Focus', 'Fusion', 'Escape', 'Edge', 'Ranger', 'F-150'],
            'Chevrolet': ['Cruze', 'Malibu', 'Equinox', 'Traverse', 'Colorado', 'Silverado'],
            'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Accent', 'i10'],
            'Kia': ['Optima', 'Cerato', 'Sorento', 'Sportage', 'Picanto', 'Niro'],
            'Nissan': ['Altima', 'Sentra', 'Rogue', 'Qashqai', 'X-Trail', 'Versa'],
            'Mazda': ['Mazda3', 'Mazda6', 'CX-5', 'CX-3', 'MX-5', 'Mazda2'],
            'Subaru': ['Outback', 'Legacy', 'Forester', 'XV', 'Impreza'],
            'Volvo': ['S60', 'S90', 'XC60', 'XC90', 'V60', 'V90'],
        }

        fuel_types = ['petrol', 'diesel', 'hybrid', 'electric']
        transmissions = ['manual', 'automatic']
        conditions = ['brand_new', 'used_locally', 'used_foreignly']
        body_types = ['sedan', 'suv', 'hatchback', 'coupe', 'wagon', 'pickup', 'van']
        engine_sizes = ['1.0', '1.2', '1.4', '1.5', '1.6', '1.8', '2.0', '2.5', '3.0']
        doors_list = [2, 3, 4, 5]
        previous_owners_list = [0, 1, 2, 3]
        colors = ['Black', 'White', 'Silver', 'Red', 'Blue', 'Gray', 'Gold', 'Beige', 'Green', 'Brown']
        
        features_list = [
            'ABS, Power Steering, Air Conditioning, Power Windows',
            'Sunroof, Leather Seats, Cruise Control, Bluetooth',
            'Backup Camera, Navigation System, Heated Seats, USB Port',
            'All-Wheel Drive, Traction Control, Electronic Stability, Hill Start',
            'Lane Departure Warning, Blind Spot Monitor, Adaptive Cruise Control',
            'Panoramic Sunroof, Premium Sound System, Memory Seats',
            'Android Auto, Apple CarPlay, WiFi Hotspot, Wireless Charging',
            'Keyless Entry, Smart Key, Push Start, Auto Headlights',
            '360 Degree Camera, Parking Sensors, Automatic Parking',
            'Airbags, Stability Control, Anti-Lock Brakes, Traction Control',
        ]

        descriptions = [
            'Well-maintained vehicle with excellent service history.',
            'Low mileage, one owner, regularly serviced.',
            'Recent full service, new tires, excellent condition.',
            'Perfect family car, spacious and comfortable.',
            'Fuel-efficient, great for city driving.',
            'Luxury sedan with all modern features.',
            'Sporty and fun to drive, well-equipped.',
            'Reliable SUV, great for outdoor adventures.',
            'Excellent value for money, great deals.',
            'Premium vehicle, showroom condition, like new.',
        ]

        cars_created = 0
        current_year = timezone.now().year

        for i in range(100):
            make = random.choice(makes)
            model = random.choice(models_by_make.get(make, ['Default']))
            year = random.randint(2010, current_year)
            price = random.randint(500000, 10000000)  # KES prices
            mileage = random.randint(1000, 250000)
            
            car = Car(
                dealership=random.choice(dealerships),
                title=f'{year} {make} {model}',
                make=make,
                model=model,
                year=year,
                price=price,
                mileage=mileage,
                fuel_type=random.choice(fuel_types),
                transmission=random.choice(transmissions),
                condition=random.choice(conditions),
                color=random.choice(colors),
                seats=random.choice([4, 5, 7, 8]),
                engine_size=random.choice(engine_sizes),
                doors=random.choice(doors_list),
                body_type=random.choice(body_types),
                previous_owners=random.choice(previous_owners_list),
                description=random.choice(descriptions),
                features=random.choice(features_list),
                is_approved=True,  # Auto-approve for testing
                is_sold=random.choice([False, False, False, True]),  # 25% chance of being sold
                is_premium=random.choice([False, False, False, False, True]),  # 20% chance of premium
                submitted_for_review=True,
                submitted_at=timezone.now(),
            )
            car.save()
            cars_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {cars_created} test cars'))
