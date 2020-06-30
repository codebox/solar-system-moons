import sys, json

from svg import Svg
from svg_wrapper import SvgWrapper
from data_processor import process_data

def get_planet_data():
    with open('data/moon-data.json') as f:
        return json.load(f)

planet_data = get_planet_data()
processed_planet_data = process_data(planet_data)[2:3]
svg = Svg()
svg_wrapper = SvgWrapper(svg)
svg_wrapper.render(processed_planet_data)

svg_wrapper.save('moons.svg')
