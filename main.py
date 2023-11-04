import math
import time
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.units import Unit
from neoscore.western.notehead import Notehead


class CircleReticle:
    def __init__(self, origin, ul, ur, bl, br, order=2):
        self.origin = origin
        self.init_time = time.time()
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = (ul[1] - bl[1]).base_value
        self.objects = []
        self.pen = Pen("000000", thickness=Unit(2))
        self.order = order
        self.top_dist = origin[1] - ul[1]
        self.bottom_dist = bl[1] - origin[1]
        self.right_dist = ur[0] - origin[0]
        self.left_dist = origin[0] - ul[0]
        self.drum_positions = []
        self.prev_rad = 0
        self.tick = 1
        self.distances = []

    def animate(self):
        radius = (time.time() - self.init_time) * 200 + 1
        for i in self.objects:
            i.remove()
        self.objects = []
        if radius < 3000:
            # 0th order circle
            if self.order >= 0:
                self.pen = Pen("000000", thickness=Unit(2))
                self.objects.append(Path.ellipse_from_center(self.origin, None, Unit(radius), Unit(radius),
                                                             Brush.no_brush(), self.pen))
            # 1st order reflections
            if self.order >= 1:
                self.pen = Pen("444444", thickness=Unit(2))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist, self.origin[1]), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist, self.origin[1]), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0], self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0], self.origin[1] + 2 * self.bottom_dist), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
            # 2nd order reflections
            if self.order >= 2:
                self.pen = Pen("888888", thickness=Unit(2))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
            # 3rd order reflections
            if self.order >= 3:
                self.pen = Pen("cccccc", thickness=Unit(2))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0],
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0],
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
            if self.tick == 1:
                self.distances = self._calculate_reticle_to_drums()
                self.tick = 2
            self._check_for_contact(radius, self.distances)
        self.prev_rad = radius

    def _calculate_reticle_to_drums(self):
        distances = []
        for i in self.objects:
            for j in self.drum_positions:
                distances.append(math.sqrt((i.x.base_value - j[0]) ** 2 + (i.y.base_value - j[1]) ** 2))
        return distances

    def _check_for_contact(self, radius, distances):
        for i in distances:
            if self.prev_rad / 2 < i < radius / 2:
                MusicText((Unit(40 * (time.time() - self.init_time)), Unit(100)), None, "noteheadBlack",
                          MusicFont("Bravura", Unit(6)))

    def set_drum_locations(self, drums_array):
        self.drum_positions = []
        for i in drums_array:
            self.drum_positions.append((i.x.base_value, i.y.base_value))


class LineReticle:
    def __init__(self, ul, ur, bl, br, direction):
        self.init_time = time.time()
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = abs((ul[1] - bl[1]).base_value)
        self.objects = []
        self.pen = Pen("000000", thickness=Unit(4))
        self.drum_positions = []
        self.tick = 1
        self.distances = []
        self.direction = direction
        match self.direction:
            case "right":
                self.prev_pos = 0
            case "left":
                self.prev_pos = self.box_width
            case "down":
                self.prev_pos = 0
            case "up":
                self.prev_pos = self.box_height

    def animate(self):
        match self.direction:
            case "right":
                pos = (time.time() - self.init_time) * 200
            case "left":
                pos = self.box_width - (time.time() - self.init_time) * 200
            case "down":
                pos = (time.time() - self.init_time) * 200
            case "up":
                pos = self.box_height - (time.time() - self.init_time) * 200
        for i in self.objects:
            i.remove()
        self.objects = []
        if 0 < pos < self.box_width:
            if self.direction == "right" or self.direction == "left":
                self.objects.append(Path.straight_line((Unit(pos), Unit(0)), None,
                                                       (Unit(0), Unit(self.box_height)), None,
                                                       Brush.no_brush(), self.pen))
            if self.direction == "up" or self.direction == "down":
                self.objects.append(Path.straight_line((Unit(0), Unit(pos)), None,
                                                       (Unit(self.box_width), Unit(0)), None,
                                                       Brush.no_brush(), self.pen))
            self._check_for_contact(pos)
        self.prev_pos = pos

    def _check_for_contact(self, pos):
        for i in self.drum_positions:
            match self.direction:
                case "right" | "down":
                    if self.prev_pos < i[0] < pos:
                        MusicText((Unit(40 * (time.time() - self.init_time)), Unit(100)), None, "noteheadBlack",
                                  MusicFont("Bravura", Unit(6)))
                case "left" | "up":
                    if self.prev_pos > i[0] > pos:
                        MusicText((Unit(40 * (time.time() - self.init_time)), Unit(100)), None, "noteheadBlack",
                                  MusicFont("Bravura", Unit(6)))

    def set_drum_locations(self, drums_array):
        self.drum_positions = []
        for i in drums_array:
            self.drum_positions.append((i.x.base_value, i.y.base_value))


class Drum:
    def __init__(self, location):
        self.loc = location
        self.init_time = time.time()
        self.x = location[0]
        self.y = location[1]
        self.pen = Pen("000000", thickness=Unit(2))
        self.objects = []
        self.rad = 25
        Path.ellipse_from_center(self.loc, None, Unit(self.rad), Unit(self.rad), Brush.no_brush(), pen=self.pen)

    def animate(self):
        radius = (time.time() - self.init_time) * 30
        for i in self.objects:
            i.remove()
        self.objects = []
        if radius < self.rad:
            self.objects.append(Path.ellipse_from_center(self.loc, None, Unit(radius), Unit(radius),
                                                         brush=Brush("#11111166"), pen=self.pen))
        elif self.rad < radius < (self.rad * (6 / 5)):
            shrink_rad = self.rad + (24 / 5) * (self.rad - radius)
            self.objects.append(Path.ellipse_from_center(self.loc, None, Unit(shrink_rad), Unit(shrink_rad),
                                                         brush=Brush("#e8fc03ff"), pen=self.pen))

    def reset_animation(self):
        self.init_time = time.time()


def redraw_top_layer():
    global top_layer
    for i in top_layer:
        i.remove()
    top_layer = []
    top_layer.append(Path.rect(ULP, None, Unit(2000), -Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    top_layer.append(Path.rect(URP, None, Unit(2000), Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    top_layer.append(Path.rect(BRP, None, -Unit(2000), Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    top_layer.append(Path.rect(BLP, None, -Unit(2000), -Unit(2000), Brush("#eeeeee"), Pen.no_pen()))


def refresh_func(current_time: float) -> Optional[neoscore.RefreshFuncResult]:
    global reticles
    for i in reticles:
        i.animate()
    for i in drums:
        i.animate()
    redraw_top_layer()


def key_handler(event):
    if event.event_type == KeyEventType.PRESS:
        if event.code == 16777236:
            reticles.append(LineReticle(ULP, URP, BLP, BRP, "right"))
            reticles[-1].set_drum_locations(drums)
        if event.code == 16777234:
            reticles.append(LineReticle(ULP, URP, BLP, BRP, "left"))
            reticles[-1].set_drum_locations(drums)
        if event.code == 16777235:
            reticles.append(LineReticle(ULP, URP, BLP, BRP, "up"))
            reticles[-1].set_drum_locations(drums)
        if event.code == 16777237:
            reticles.append(LineReticle(ULP, URP, BLP, BRP, "down"))
            reticles[-1].set_drum_locations(drums)
        for i in drums:
            i.reset_animation()


def mouse_handler(event):
    if event.event_type == MouseEventType.PRESS:
        x, y = event.document_pos
        if ULP[0] < x < URP[0] and ULP[1] < y < BLP[1]:
            reticles.append(CircleReticle((x, y), ULP, URP, BLP, BRP))
            reticles[-1].set_drum_locations(drums)


def initialize():
    upper_left_point = (Unit(0), Unit(0))
    upper_right_point = (Unit(500), Unit(0))
    bottom_left_point = (Unit(0), Unit(500))
    bottom_right_point = (Unit(500), Unit(500))
    upper_left = Path.ellipse(upper_left_point, None, Unit(0), Unit(0), pen=pen)
    upper_right = Path.ellipse(upper_right_point, None, Unit(0), Unit(0), pen=pen)
    bottom_left = Path.ellipse(bottom_left_point, None, Unit(0), Unit(0), pen=pen)
    bottom_right = Path.ellipse(bottom_right_point, None, Unit(0), Unit(0), pen=pen)
    zero = (Unit(0), Unit(0))
    Path.straight_line(zero, upper_left, zero, upper_right, pen=pen)
    Path.straight_line(zero, upper_right, zero, bottom_right, pen=pen)
    Path.straight_line(zero, bottom_right, zero, bottom_left, pen=pen)
    Path.straight_line(zero, bottom_left, zero, upper_left, pen=pen)
    return upper_left_point, upper_right_point, bottom_left_point, bottom_right_point, \
        upper_left, upper_right, bottom_left, bottom_right, zero


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    neoscore.setup()

    pen = Pen("000000", thickness=Unit(2))
    ULP, URP, BLP, BRP, UL, UR, BL, BR, Zero = initialize()
    top_layer = []
    reticles = []
    drums = []
    drums.append(Drum((Unit(100), Unit(100))))
    drums.append(Drum((Unit(200), Unit(200))))
    MusicText((Unit(-20), Unit(100)), None, "noteheadBlack",
              MusicFont("Bravura", Unit(6)))

    neoscore.set_key_event_handler(key_handler)
    neoscore.set_mouse_event_handler(mouse_handler)
    neoscore.show(refresh_func, display_page_geometry=False, auto_viewport_interaction_enabled=False)
