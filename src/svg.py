import codecs, random, math

class Svg:
    def __init__(self):
        self.template = open('template.svg').read()
        self.styles = []
        self.defs = []
        self.content = []

    def add_circle(self, x, y, r, css_class, clip_path, randomise_opacity=False, opacity=None):
        style_attribute = ''
        if randomise_opacity:
            style_attribute = 'style="stroke-opacity: {}"'.format(0.1 + random.random()/10)
        elif opacity:
            style_attribute = 'style="stroke-opacity: {}"'.format(opacity)

        self.content.append(u'<circle cx="{}" cy="{}" r="{}" class="{}" clip-path="url(#{})" {} />'.format(
            x, y, r, css_class, clip_path, style_attribute
        ))

    def add_ellipse(self, cx, cy, rx, ry, angle, css_class, clip_path='', randomise_lightness=False, rotation_x=None, rotation_y=None, opacity=1):
        self.content.append(u'<g clip-path="url(#{4})" ><ellipse cx="{0}" cy="{1}" rx="{2}" ry="{3}" transform="rotate({5},{6},{7})" class="{8}" {9}/></g>'.format(
            cx, cy, rx, ry, clip_path,
            angle * 180 / math.pi, cx if rotation_x is None else rotation_x, cy if rotation_y is None else rotation_y,
            css_class, 'style="stroke: hsla(0, 0%,{}%,{})"'.format(75 + random.random() * 25, opacity) if randomise_lightness else 'style="stroke-opacity: {}"'.format(opacity))
        )

    def _get_circle_arc_path(self, cx, cy, r, start_angle, end_angle):
        start_x = cx + r * math.sin(start_angle)
        start_y = cy + r * math.cos(start_angle)
        end_x = cx + r * math.sin(end_angle)
        end_y = cy + r * math.cos(end_angle)
        return 'M {0} {1} A {2} {2} 0 0 0 {3} {4}'.format(start_x, start_y, r, end_x, end_y)

    def _get_line_path(self, x1, y1, x2, y2):
        return 'M {} {} L {} {}'.format(x1, y1, x2, y2)

    def add_circle_text(self, x, y, r, css_class, text, start_angle=3*math.pi/2, end_angle=math.pi/2, clip_path=''):
        path_id = 'p{}_{}_{}'.format(x, y, r)
        path_d = self._get_circle_arc_path(x, y, r, start_angle, end_angle)
        self.defs.append('<path id="{}" d="{}" />'.format(path_id, path_d))
        self.content.append('<text class="{}" {}><textPath href="#{}" text-anchor="middle" startOffset="50%">{}</textPath></text>'.format(css_class, 'clip-path="url(#{})"'.format(clip_path) if clip_path else '', path_id, text))

    def add_line_text(self, x1, y1, x2, y2, css_class, text, text_anchor='end', start_offset='100%'):
        path_id = 'p{}_{}_{}_{}'.format(x1, y1, x2, y2)
        path_d = self._get_line_path(x1, y1, x2, y2)
        self.defs.append('<path id="{}" d="{}" />'.format(path_id, path_d))
        self.content.append('<text class="{}"><textPath href="#{}" text-anchor="{}" startOffset="{}">{}</textPath></text>'.format(css_class, path_id, text_anchor, start_offset, text))

    def add_rectangle(self, x, y, w, h, css_class):
        self.content.append(u'<rect x="{}" y="{}" width="{}" height="{}" class="{}"/>'.format(x, y, w, h, css_class))

    def add_line(self, x1, y1, x2, y2, css_class):
        self.content.append(u'<line x1="{}" y1="{}" x2="{}" y2="{}" class="{}"/>'.format(x1, y1, x2, y2, css_class))

    def add_clip_path_rect(self, x, y, w, h, id):
        self.content.append(u'<clipPath id="{}"><rect x="{}" y="{}" width="{}" height="{}"/></clipPath>'.format(id, x, y, w, h))

    def add_centered_text(self, y, text, css_class):
        self.content.append(u'<text x="50%" y="{}" text-anchor="middle" startOffset="50%" class="{}">{}</text>'.format(y, css_class, text))

    def add_text(self, x, y, text, css_class):
        self.content.append(u'<text x="{}" y="{}" class="{}">{}</text>'.format(x, y, css_class, text))

    def add_right_aligned_text(self, x, y, text, css_class):
        self.content.append(u'<text x="{}" y="{}" text-anchor="end" class="{}">{}</text>'.format(x, y, css_class, text))

    def add_radial_gradient(self, id, css_class):
        self.defs.append(u'<radialGradient id="{}" class="{}" r="50%" cx="50%" cy="50%"><stop offset="0.9" stop-opacity="1"/><stop offset="1" stop-opacity="0"/></radialGradient>'.format(id, css_class))

    def add_substitutions(self, substitutions):
        for key, value in substitutions.items():
            self.template = self.template.replace('%{}%'.format(key), str(value))

    def save(self, out_file):
        part1, tmp = self.template.split('%style%')
        part2, tmp = self.template.split('%defs%')
        part3, part4 = tmp.split('%substance%')

        with codecs.open(out_file, 'w', 'utf-8') as f:
            f.write(part1)
            for style in self.styles:
                f.write(style + '\n')
            f.write(part2)
            for defn in self.defs:
                f.write(defn + '\n')
            f.write(part3)
            for content in self.content:
                f.write(content + '\n')
            f.write(part4)
