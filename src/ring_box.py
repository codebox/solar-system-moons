import math
from data_processor import build_rescale

PADDING = -30
TEXT_OFFSET = 3

class RingBox:
    def __init__(self, planet_data, w, h, x_margin, y_margin):
        self.title = planet_data['planet']['name']
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.x_margin = x_margin
        self.y_margin = y_margin
        self.rings = planet_data['rings'][:]
        self.planet_radius = planet_data['planet']['radius']
        self.rings.sort(key=lambda r: r['radius'] + r['width'], reverse=True)

    def render(self, svg, x, y):
        self.x = x
        self.y = y
        max_ring_radius = max(map(lambda r: r['radius'] + r['width'], self.rings))
        min_dimension = min(self.h - 2 * self.y_margin, self.w - 2 * self.x_margin)

        rescale = build_rescale(0, max_ring_radius, 0, min_dimension/2 - 2 * PADDING)

        self._render_outer(svg, rescale)
        self._render_inner(svg, rescale)
        self._render_rectangle(svg)

    def _render_outer(self, svg, rescale):
        clip_path_id = self._get_outer_clip_path()
        svg.add_clip_path_rect(self.x, self.y, self.w, self.h, clip_path_id)

        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        for ring in self.rings:
            inner_edge_radius = rescale(ring['radius'])
            outer_edge_radius = max(inner_edge_radius + 1, rescale(ring['radius'] + ring['width']))
            svg.add_circle(cx, cy, outer_edge_radius).with_class('ringBoxRing ' + self.title).with_clip_path(clip_path_id)

    def _render_inner(self, svg, rescale):
        clip_path_id = self._get_inner_clip_path()
        svg.add_clip_path_rect(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin, clip_path_id)

        cx = self.x + self.w / 2
        cy = self.y + self.h / 2

        for ring in self.rings:
            inner_edge_radius = rescale(ring['radius'])
            outer_edge_radius = max(inner_edge_radius + 1, rescale(ring['radius'] + ring['width']))
            for r in range(int(inner_edge_radius), int(outer_edge_radius)):
                svg.add_circle(cx, cy, r).with_class('ringBoxRing ' + self.title).with_clip_path(clip_path_id).with_random_opacity()
            svg.add_circle(cx, cy, outer_edge_radius).with_class('ringBoxRing ' + self.title).with_clip_path(clip_path_id)

        angular_offset = 0
        for ring in self.rings:
            inner_edge_radius = rescale(ring['radius'])
            outer_edge_radius = max(inner_edge_radius + 1, rescale(ring['radius'] + ring['width']))
            svg.add_circle_text(cx, cy, TEXT_OFFSET + (inner_edge_radius + outer_edge_radius)/2, ring['name'])\
                .with_class('ringBoxRingName ' + self.title)\
                .with_angle(angular_offset + 3 * math.pi / 2, angular_offset + math.pi / 2)\
                .with_clip_path(clip_path_id)
            angular_offset += 2 * (math.pi * 2 / len(self.rings))

        svg.add_radial_gradient('ringBoxPlanetGradient', self.title)
        svg.add_circle(cx, cy, rescale(self.planet_radius)).with_class('ringBoxPlanetDisc ' + self.title).with_clip_path(clip_path_id)

    def _render_rectangle(self, svg):
        svg.add_rectangle(self.x + self.x_margin, self.y + self.y_margin, self.w - 2 * self.x_margin, self.h - 2 * self.y_margin).with_class('ringBox ' + self.title)

    def _get_inner_clip_path(self):
        return 'ring_clip_inner_' + self.title

    def _get_outer_clip_path(self):
        return 'ring_clip_outer_' + self.title
