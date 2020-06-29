HEIGHT=400
WIDTH=800
class SvgWrapper:
    def __init__(self, svg):
        self.svg = svg

    def set_planet(self, planet):
        pass

    def add_moon(self, moon):
        self.svg.add_circle(0, HEIGHT/2, moon['x'] * WIDTH, 'moonOrbit')
        self.svg.add_circle(moon['x'] * WIDTH, HEIGHT/2, moon['r'] * WIDTH, 'moon')

    def save(self, out_file):
        self.svg.save(out_file)
