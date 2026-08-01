import json
from .forms import get_combined_car_hierarchy


def car_hierarchy(request):
    return {
        'car_hierarchy_json': json.dumps(get_combined_car_hierarchy())
    }
