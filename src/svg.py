import codecs, random, math, uuid
from abc import ABC, abstractmethod


class ElementBuilder(ABC):
    def __init__(self, name):
        self.name = name
        self.content = ''
        self.defs = ''
        self.attributes = {}

    def set_content(self, content):
        self.content = content
        return self

    def attribute(self, name, value):
        self.attributes[name] = value.replace('"', '&#34;') if isinstance(value, str) else value
        return self

    def with_class(self, css_class):
        self.attribute('class', css_class)
        return self

    def with_clip_path(self, path_id):
        self.attribute('clip-path', 'url(#{})'.format(path_id))
        return self

    def with_opacity(self, opacity):
        self.attribute('style', 'stroke-opacity: {}'.format(opacity))
        return self

    def get_element(self):
        attribute_values = ' '.join(['{}="{}"'.format(key, self.attributes[key]) for key in self.attributes.keys()])

        if self.content:
            result = '<{0} {1}>{2}</{0}>'.format(self.name, attribute_values, self.content)
        else:
            result = '<{0} {1}/>'.format(self.name, attribute_values)

        return result

    def get_defs(self):
        return self.defs


class CircleBuilder(ElementBuilder):
    def __init__(self, cx, cy, r):
        super().__init__('circle')
        self.attribute('cx', cx).attribute('cy', cy).attribute('r', r)

    def with_random_opacity(self, min_opacity=0.1, max_opacity=0.2):
        self.with_opacity(min_opacity + random.random() * (max_opacity - min_opacity))
        return self


class RectangleBuilder(ElementBuilder):
    def __init__(self, x, y, w, h):
        super().__init__('rect')
        self.attribute('x', x).attribute('y', y).attribute('w', w).attribute('h', h)


class LineBuilder(ElementBuilder):
    def __init__(self, x1, y1, x2, y2):
        super().__init__('line')
        self.attribute('x1', x1).attribute('y1', y1).attribute('x2', x2).attribute('y2', y2)


class EllipseBuilder(ElementBuilder):
    def __init__(self, cx, cy, rx, ry):
        super().__init__('ellipse')
        self.clip_path = None
        self.attribute('cx', cx).attribute('cy', cy).attribute('rx', rx).attribute('ry', ry)

    def with_clip_path(self, path_id):
        self.clip_path = path_id
        return self

    def with_rotation(self, cx, cy, angle):
        self.attribute('transform', 'rotate({},{},{})'.format(angle, cx, cy))
        return self

    def with_random_lightness(self, is_random=True, min_lightness=75, max_lightness=100):
        if is_random:
            lightness = min_lightness + random.random() * (max_lightness - min_lightness)
            self.attribute('style', 'stroke: hsl(0, 0%,{}%)'.format(lightness))
        return self

    def get_element(self):
        ellipse_source = super().get_element()
        if self.clip_path:
            return '<g clip-path="url(#{})">{}</g>'.format(self.clip_path, ellipse_source)
        else:
            return ellipse_source


class ClipPathBuilder(RectangleBuilder):
    def __init__(self, id, x, y, w, h):
        super().__init__(x, y, w, h)
        self.id = id

    def get_element(self):
        rect_source = super().get_element()
        return '<clipPath id="{}">{}</clipPath>'.format(self.id, rect_source)

class TextPathBuilder(ElementBuilder):
    def __init__(self, text):
        super().__init__('textPath')
        self.set_content(text)
        self.path_id = uuid.uuid4().hex
        path_d = self._get_path()
        self.defs = '<path id="{}" d="{}" />'.format(self.path_id, path_d)
        self.attribute('href', '#' + self.path_id)

    @abstractmethod
    def _get_path(self):
        pass

    def align_start(self):
        self.attribute('text-anchor', 'start').attribute('start-offset', '0%')
        return self

    def align_middle(self):
        self.attribute('text-anchor', 'middle').attribute('start-offset', '50%')
        return self

    def align_end(self):
        self.attribute('text-anchor', 'end').attribute('start-offset', '100%')
        return self


class CircleTextBuilder(TextPathBuilder):
    def __init__(self, cx, cy, r, text):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.start_angle = 3 * math.pi / 2
        self.end_angle = math.pi / 2
        super().__init__(text)

    def _get_path(self):
        start_x = self.cx + self.r * math.sin(self.start_angle)
        start_y = self.cy + self.r * math.cos(self.start_angle)
        end_x = self.cx + self.r * math.sin(self.end_angle)
        end_y = self.cy + self.r * math.cos(self.end_angle)
        return 'M {0} {1} A {2} {2} 0 0 0 {3} {4}'.format(start_x, start_y, self.r, end_x, end_y)

    def with_angle(self, start_angle, end_angle):
        self.start_angle = start_angle
        self.end_angle = end_angle
        return self


class LineTextBuilder(TextPathBuilder):
    def __init__(self, x1, y1, x2, y2, text):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        super().__init__(text)

    def _get_path(self):
        return 'M {} {} L {} {}'.format(self.x1, self.y1, self.x2, self.y2)


class TextBuilder(ElementBuilder):
    def __init__(self, x, y, text):
        super().__init__('text')
        self.attribute('x', x).attribute('y', y)
        self.set_content(text)

    def align_middle(self):
        self.attribute('text-anchor', 'middle').attribute('start-offset', '50%')
        return self

    def align_end(self):
        self.attribute('text-anchor', 'end').attribute('start-offset', '100%')
        return self


class RadialGradientBuilder(ElementBuilder):
    def __init__(self, id):
        super().__init__('radialGradient')
        self.attribute('id', id).attribute('r', '50%').attribute('cx', '50%').attribute('cy', '50%')
        self.stops = []

    def add_stop(self, offset, opacity):
        self.stops.append({'offset': offset, 'opacity': opacity})
        return self

    def get_element(self):
        return None
    
    def get_defs(self):
        stops = ''.join(map(lambda s: '<stop offset="{}" stop-opacity="{}"/>'.format(s['offset'], s['opacity']), self.stops))
        self.set_content(stops)
        return super().get_element()


class Svg:
    def __init__(self):
        self.template = open('template.svg').read()
        self.builders = []

    def add_circle(self, x, y, r):
        circle_builder = CircleBuilder(x, y, r)
        self.builders.append(circle_builder)
        return circle_builder

    def add_ellipse(self, cx, cy, rx, ry):
        ellipse_builder = EllipseBuilder(cx, cy, rx, ry)
        self.builders.append(ellipse_builder)
        return ellipse_builder

    def add_circle_text(self, x, y, r, text):
        circle_text_builder = CircleTextBuilder(x, y, r, text)
        self.builders.append(circle_text_builder)
        return circle_text_builder

    def add_line_text(self, x1, y1, x2, y2, text):
        line_text_builder = LineTextBuilder(x1, y1, x2, y2, text)
        self.builders.append(line_text_builder)
        return line_text_builder

    def add_rectangle(self, x, y, w, h):
        rectangle_builder = RectangleBuilder(x, y, w, h)
        self.builders.append(rectangle_builder)
        return rectangle_builder

    def add_line(self, x1, y1, x2, y2):
        line_builder = LineBuilder(x1, y1, x2, y2)
        self.builders.append(line_builder)
        return line_builder

    def add_clip_path_rect(self, x, y, w, h, id):
        clip_path_builder = ClipPathBuilder(id, x, y, w, h)
        self.builders.append(clip_path_builder)
        return clip_path_builder

    def add_text(self, x, y, text):
        text_builder = TextBuilder(x, y, text)
        self.builders.append(text_builder)
        return text_builder

    def add_radial_gradient(self, id, css_class):
        radial_gradient_builder = RadialGradientBuilder(id).with_class(css_class)
        self.builders.append(radial_gradient_builder)
        return radial_gradient_builder

    def add_substitutions(self, substitutions):
        for key, value in substitutions.items():
            self.template = self.template.replace('%{}%'.format(key), str(value))

    def save(self, out_file):
        part1, tmp = self.template.split('%defs%')
        part2, part3 = tmp.split('%substance%')

        with codecs.open(out_file, 'w', 'utf-8') as f:
            f.write(part1)
            for builder in self.builders:
                defn = builder.get_defs()
                if defn:
                    f.write(defn + '\n')
            f.write(part2)
            for builder in self.builders:
                el = builder.get_element()
                if el:
                    f.write(el + '\n')
            f.write(part3)
