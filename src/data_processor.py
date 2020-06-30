import math

MOON_SCALED_RADIUS_MIN = 0
MOON_SCALED_RADIUS_MAX = 0.02

MOON_SCALED_DISTANCE_MIN = 0.1
MOON_SCALED_DISTANCE_MAX = 0.9

def process_data(planet_data):
    moon_radii = [moon['radius'] for planet in planet_data for moon in planet['moons']]
    min_moon_radius = min(moon_radii)
    max_moon_radius = max(moon_radii)
    scale_radius = _build_rescale(min_moon_radius, max_moon_radius, MOON_SCALED_RADIUS_MIN, MOON_SCALED_RADIUS_MAX)

    moon_distances = [moon['orbit'] for planet in planet_data for moon in planet['moons']]
    min_moon_distance = min(moon_distances)
    max_moon_distance = max(moon_distances)
    scale_distance = _build_rescale(min_moon_distance, max_moon_distance, MOON_SCALED_DISTANCE_MIN, MOON_SCALED_DISTANCE_MAX)

    processed = []
    for planet in planet_data:
        moons = []
        for moon in planet['moons']:
            moons.append({
                'x': scale_distance(moon['orbit']),
                'r': scale_radius(moon['radius'])
            })

        processed.append({
            'planet': {
                'name': planet['planet'],
                'radius': scale_radius(planet['radius'])
            },
            'moons': moons
        })

    return processed

def _build_rescale(orig_min, orig_max, scaled_min, scaled_max):
    # return _build_log_rescale(orig_min, orig_max, scaled_min, scaled_max)
    return _build_linear_rescale(orig_min, orig_max, scaled_min, scaled_max)

def _build_log_rescale(orig_min, orig_max, scaled_min, scaled_max):
    log_min = math.log(1+orig_min)
    log_max = math.log(1+orig_max)
    scaled_range = scaled_max - scaled_min

    def log_rescale(value):
        log_value = math.log(1+value)
        return scaled_min + scaled_range * (log_value - log_min)/(log_max - log_min)

    return log_rescale

def _build_linear_rescale(orig_min, orig_max, scaled_min, scaled_max):
    scaled_range = scaled_max - scaled_min

    def linear_rescale(value):
        return scaled_min + scaled_range * (value - orig_min)/(orig_max - orig_min)

    return linear_rescale
