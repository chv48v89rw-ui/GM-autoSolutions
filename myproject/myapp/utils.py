try:
    import requests
except ImportError:
    requests = None

from django.conf import settings

def geocode_address(address):
    """
    Convert address to latitude and longitude using OpenStreetMap Nominatim API
    Returns (latitude, longitude) or (None, None) if not found
    """
    if not requests:
        print("Requests module not available. Geocoding disabled.")
        return None, None
        
    try:
        # Using Nominatim API (free OpenStreetMap geocoding)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'ke'  # Kenya country code
        }
        
        headers = {
            'User-Agent': 'GM autoSolutions Car Dealership'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        return None, None
        
    except Exception as e:
        print(f"Geocoding error for address '{address}': {e}")
        return None, None

def reverse_geocode(lat, lon):
    """
    Convert latitude and longitude to address using OpenStreetMap Nominatim API
    Returns formatted address or None if not found
    """
    if not requests:
        print("Requests module not available. Reverse geocoding disabled.")
        return None
        
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        
        headers = {
            'User-Agent': 'GM autoSolutions Car Dealership'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data and 'display_name' in data:
            return data['display_name']
        return None
        
    except Exception as e:
        print(f"Reverse geocoding error for coordinates {lat}, {lon}: {e}")
        return None
