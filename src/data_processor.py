import math

MOON_SCALED_DISTANCE_MIN = 0
MOON_SCALED_DISTANCE_MAX = 1


def process_data(planet_data):
    max_moon_distance = max([moon['orbit'] for moon in planet_data['moons']])
    scale_distance = build_rescale(0, max_moon_distance, MOON_SCALED_DISTANCE_MIN, MOON_SCALED_DISTANCE_MAX)

    moons = []
    for moon in planet_data['moons']:
        moons.append({
            'name': moon['name'],
            'orbit': scale_distance(moon['orbit']),
            'radius': scale_distance(moon['radius']),
            'original': moon
        })

    return {
        'planet': {
            'name': planet_data['planet'],
            'radius': scale_distance(planet_data['radius'])
        },
        'moons': moons
    }


def build_rescale(orig_min, orig_max, scaled_min, scaled_max):
    #return _build_log_rescale(orig_min, orig_max, scaled_min, scaled_max)
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
