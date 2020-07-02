import sys, json

from svg import Svg
from svg_wrapper import SvgWrapper
from data_processor import process_data

def get_planet_data(planet_name):
    with open('data/moon-data.json') as f:
        data = json.load(f)
        for planet in data:
            if planet['planet'].lower() == planet_name.lower():
                return planet

if len(sys.argv) == 2:
    planet_name = sys.argv[1]
    planet_data = get_planet_data(planet_name)
    processed_planet_data = process_data(planet_data)
    if planet_data:
        svg = Svg()
        svg_wrapper = SvgWrapper(svg)
        svg_wrapper.render(processed_planet_data)
        svg_wrapper.save('{}.svg'.format(planet_name))

    else:
        print('Unknown planet:', planet_name)
else:
    print("Usage: python {} <planet name>".format(sys.argv[0]))