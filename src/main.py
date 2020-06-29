import sys, json


def get_planet_data(planet_name):
    with open('data/moon-data.json') as f:
        data = json.load(f)
        for planet in data:
            if planet['planet'].lower() == planet_name.lower():
                return planet

if len(sys.argv) == 2:
    planet_name = sys.argv[1]
    planet_data = get_planet_data(planet_name)
    if planet_data:
        print(planet_data)
    else:
        print('Unknown planet:', planet_name)