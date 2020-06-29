import math

MOON_SCALED_RADIUS_MIN = 0.001
MOON_SCALED_RADIUS_MAX = 0.01

MOON_SCALED_DISTANCE_MIN = 0.1
MOON_SCALED_DISTANCE_MAX = 0.9

def process_data(planet_data):
    planet_radius = planet_data['radius']

    moon_radii = [moon['radius'] for moon in planet_data['moons']]
    min_moon_radius = min(moon_radii)
    max_moon_radius = max(moon_radii)
    scale_radius = _build_log_rescale(min_moon_radius, max_moon_radius, MOON_SCALED_RADIUS_MIN, MOON_SCALED_RADIUS_MAX)

    moon_distances = [moon['orbit'] for moon in planet_data['moons']]
    min_moon_distance = min(moon_distances)
    max_moon_distance = max(moon_distances)
    scale_distance = _build_log_rescale(min_moon_distance, max_moon_distance, MOON_SCALED_DISTANCE_MIN, MOON_SCALED_DISTANCE_MAX)

    moons = []
    for moon in planet_data['moons']:
        moons.append({
            'x': scale_distance(moon['orbit']),
            'r': scale_radius(moon['radius'])
        })

    return {
        'planet': {},
        'moons': moons
    }

def _build_log_rescale(orig_min, orig_max, scaled_min, scaled_max):
    log_min = math.log(1+orig_min)
    log_max = math.log(1+orig_max)
    scaled_range = scaled_max - scaled_min

    def log_rescale(value):
        log_value = math.log(1+value)
        return scaled_min + scaled_range * (log_value - log_min)/(log_max - log_min)

    return log_rescale
