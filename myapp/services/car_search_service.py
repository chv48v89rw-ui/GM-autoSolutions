from django.db.models import Q
from ..models import Car


def search_cars_by_criteria(criteria=None):
    """
    Search cars in the database based on provided criteria.
    
    Args:
        criteria: dict with search parameters (make, model, price_range, etc.)
    
    Returns:
        QuerySet of matching cars
    """
    cars = Car.objects.select_related('dealership').filter(
        is_sold=False, 
        is_approved=True
    )
    
    if not criteria:
        return cars[:10]  # Return 10 random cars if no criteria
    
    # Apply filters based on criteria
    if criteria.get('make'):
        cars = cars.filter(make__icontains=criteria['make'])
    
    if criteria.get('model'):
        cars = cars.filter(model__icontains=criteria['model'])
    
    if criteria.get('year_from'):
        cars = cars.filter(year__gte=criteria['year_from'])
    
    if criteria.get('year_to'):
        cars = cars.filter(year__lte=criteria['year_to'])
    
    if criteria.get('price_from'):
        cars = cars.filter(price__gte=criteria['price_from'])
    
    if criteria.get('price_to'):
        cars = cars.filter(price__lte=criteria['price_to'])
    
    if criteria.get('fuel_type'):
        cars = cars.filter(fuel_type=criteria['fuel_type'])
    
    if criteria.get('transmission'):
        cars = cars.filter(transmission=criteria['transmission'])
    
    if criteria.get('body_type'):
        cars = cars.filter(body_type=criteria['body_type'])
    
    if criteria.get('condition'):
        cars = cars.filter(condition=criteria['condition'])

    if criteria.get('inventory_code'):
        cars = cars.filter(inventory_code__iexact=criteria['inventory_code'])
    
    return cars[:10]  # Limit to 10 results


def format_car_for_ai(car):
    """
    Format a car object for AI consumption.
    
    Args:
        car: Car model instance
    
    Returns:
        dict with car details
    """
    features_text = car.features or ''
    features_list = [feature.strip() for feature in features_text.split(',') if feature.strip()]

    return {
        'id': car.id,
        'inventory_code': car.inventory_code or 'Not Assigned',
        'title': f"{car.inventory_code or 'GM0000'} - {car.year} {car.make} {car.model}{' ' + car.variant if car.variant else ''}",
        'make': car.make,
        'model': car.model,
        'variant': car.variant or 'Not specified',
        'year': car.year,
        'price': float(car.price),
        'mileage': car.mileage,
        'fuel_type': car.get_fuel_type_display(),
        'transmission': car.get_transmission_display(),
        'condition': car.get_condition_display(),
        'body_type': car.get_body_type_display() if car.body_type else 'Not specified',
        'color': car.color,
        'exterior_color': car.exterior_color or car.color or 'Not specified',
        'interior_color': car.interior_color or 'Not specified',
        'seat_material': car.seat_material or 'Not specified',
        'interior_trim': car.interior_trim or 'Not specified',
        'seats': car.seats,
        'doors': car.doors or 'Not specified',
        'number_of_keys': car.number_of_keys or 0,
        'engine_size': car.get_engine_size_display() if car.engine_size else 'Not specified',
        'features': features_list,
        'feature_summary': ', '.join(features_list) if features_list else 'Not Listed',
        'dealership': car.dealership.company_name,
        'dealership_rating': car.dealership.rating,
        'dealership_verified': car.dealership.is_verified,
        'dealership_location': car.dealership.location,
        'description': car.description[:200] if car.description else '',
    }


def get_car_recommendations_context(user_message):
    """
    Analyze user message and extract car search criteria.
    Returns formatted car data for AI context.
    
    Args:
        user_message: str - user's message
    
    Returns:
        str - formatted context with car recommendations
    """
    # Simple keyword-based criteria extraction
    criteria = {}
    
    message_lower = user_message.lower()
    
    # Extract make
    makes = ['toyota', 'bmw', 'mercedes', 'audi', 'honda', 'nissan', 'mazda', 'subaru', 
             'volkswagen', 'ford', 'chevrolet', 'hyundai', 'kia', 'mitsubishi', 'suzuki', 'land rover']
    for make in makes:
        if make in message_lower:
            criteria['make'] = make
            break
    
    # Extract model (common ones)
    models = ['corolla', 'camry', 'rav4', 'prado', 'land cruiser', 'x5', '3 series', '5 series',
              'c-class', 'e-class', 'a4', 'a6', 'civic', 'accord', 'cr-v', 'qashqai', 'x-trail',
              'cx-5', 'forester', 'outback', 'golf', 'passat', 'focus', 'escape', 'elantra', 'sportage']
    for model in models:
        if model in message_lower:
            criteria['model'] = model
            break
    
    # Extract price range
    import re
    price_matches = re.findall(r'(\d+)\s*(k|ksh|kes|shillings)?', message_lower)
    if price_matches:
        prices = [int(match[0]) for match in price_matches]
        if len(prices) >= 2:
            criteria['price_from'] = min(prices) * 1000
            criteria['price_to'] = max(prices) * 1000
        elif len(prices) == 1:
            criteria['price_to'] = prices[0] * 1000
    
    # Extract fuel type
    if 'diesel' in message_lower:
        criteria['fuel_type'] = 'diesel'
    elif 'petrol' in message_lower:
        criteria['fuel_type'] = 'petrol'
    elif 'hybrid' in message_lower:
        criteria['fuel_type'] = 'hybrid'
    elif 'electric' in message_lower:
        criteria['fuel_type'] = 'electric'
    
    # Extract transmission
    if 'automatic' in message_lower:
        criteria['transmission'] = 'automatic'
    elif 'manual' in message_lower:
        criteria['transmission'] = 'manual'
    
    # Extract body type
    if 'suv' in message_lower:
        criteria['body_type'] = 'suv'
    elif 'sedan' in message_lower:
        criteria['body_type'] = 'sedan'
    elif 'hatchback' in message_lower:
        criteria['body_type'] = 'hatchback'
    
    # Extract condition
    if 'new' in message_lower:
        criteria['condition'] = 'brand_new'
    elif 'used' in message_lower or 'second hand' in message_lower:
        criteria['condition'] = 'used_locally'
    
    inventory_code_match = re.search(r'\bGM\d{4}\b', user_message, re.IGNORECASE)
    if inventory_code_match:
        criteria['inventory_code'] = inventory_code_match.group(0).upper()

    # Search for cars
    cars = search_cars_by_criteria(criteria)
    
    if inventory_code_match:
        cars = cars.filter(inventory_code__iexact=criteria['inventory_code'])

    if not cars.exists():
        return "No cars found matching your criteria. Try adjusting your preferences or browse all available cars."
    
    # Format cars for AI
    car_list = [format_car_for_ai(car) for car in cars]
    
    # Build context string
    context = f"Found {len(car_list)} cars matching your criteria:\n\n"
    for i, car in enumerate(car_list, 1):
        context += f"{i}. {car['title']}\n"
        context += f"   Inventory Code: {car['inventory_code']}\n"
        context += f"   Year: {car['year']}\n"
        context += f"   Make: {car['make']} | Model: {car['model']} | Variant: {car['variant']}\n"
        context += f"   Price: KES {int(car['price']):,}\n"
        context += f"   Mileage: {car['mileage']:,} km\n"
        context += f"   Fuel: {car['fuel_type']} | Transmission: {car['transmission']} | Body: {car['body_type']}\n"
        context += f"   Condition: {car['condition']} | Exterior Colour: {car['exterior_color']} | Interior Colour: {car['interior_color']}\n"
        context += f"   Seat Material: {car['seat_material']} | Interior Trim: {car['interior_trim']} | Seats: {car['seats']} | Doors: {car['doors']} | Keys: {car['number_of_keys']}\n"
        context += f"   Features: {car['feature_summary']}\n"
        context += f"   Dealership: {car['dealership']} (Rating: {car['dealership_rating']}/5"
        if car['dealership_verified']:
            context += ", ✓ Verified"
        context += f")\n"
        context += f"   Location: {car['dealership_location']}\n"
        context += f"   Description: {car['description']}...\n\n"
    
    context += "\nYou can provide more details about these cars or help the user compare them. "
    context += "For full details and images, direct users to the car listing pages."
    
    return context
