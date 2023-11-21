# TO DO
# Variable velocity reticles
# Make top area a darker color (so I don't have to change brush color between areas...)

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
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.text import Text
from neoscore.core.units import Unit

from config import *


class CircleReticle:
    def __init__(self, origin, ul, ur, bl, br, id, order=num_reflections, pen=None, velocity=200, now=0):
        self.origin = origin
        self.id = id
        self.init_time = now
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = (ul[1] - bl[1]).base_value
        self.objects = []
        self.pen = pen
        self.order = order
        self.top_dist = origin[1] - ul[1]
        self.bottom_dist = bl[1] - origin[1]
        self.right_dist = ur[0] - origin[0]
        self.left_dist = origin[0] - ul[0]
        self.drum_positions = []
        self.prev_rad = 0
        self.tick = 1
        self.velocity = velocity
        self.distances = []
        with open(data_file, 'a') as df:
            to_write = "reticle, " + "circle" + ", atk_time, " + str(now+scroll_time) + \
                        ", pen_pattern, " + str(pen.pattern) + ", dynamic, " + str(pen.color) + \
                        ", id, " + str(self.id) + "\n"
            df.write(to_write)

    def animate(self, now):
        trash2 = None
        trash1, drum_hit = self._animate_trace(now)
        if (now - self.init_time) > scroll_time:
            trash2 = self._animate_actual(now)
        return trash1, trash2, drum_hit

    def _animate_trace(self, now):
        radius = (now - self.init_time) * self.velocity + 1
        for i in self.objects:
            i.remove()
        self.objects = []
        if radius <= screen_width * 5:
            # 0th order circle
            if self.order >= 0:
                self.objects.append(Path.ellipse_from_center(self.origin, None, Unit(radius), Unit(radius),
                                                             Brush.no_brush(), Pen.no_pen()))
            # 1st order reflections
            if self.order >= 1:
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist, self.origin[1]), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), Pen.no_pen()))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist, self.origin[1]), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), Pen.no_pen()))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0], self.origin[1] - 2 * self.top_dist), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), Pen.no_pen()))
                self.objects.append(
                    Path.ellipse_from_center((self.origin[0], self.origin[1] + 2 * self.bottom_dist), None,
                                             Unit(radius), Unit(radius), Brush.no_brush(), Pen.no_pen()))
            # 2nd order reflections
            if self.order >= 2:
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
            # 3rd order reflections
            if self.order >= 3:
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0],
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0],
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] + 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * Unit(self.box_width),
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist,
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * Unit(self.box_width),
                                                              self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist,
                                                              self.origin[1] - 2 * Unit(self.box_height)), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(),
                                                             Pen.no_pen()))
            if self.tick == 1:
                self.distances = self._calculate_reticle_to_drums()
                self.tick = 2
            drum_hit = self._check_for_contact(radius, self.distances, now)
            self.prev_rad = radius
            return None, drum_hit
        else:
            return self.id

    def _animate_actual(self, now):
        radius = (now - self.init_time - scroll_time) * self.velocity + 1
        for i in self.objects:
            i.remove()
        self.objects = []
        if 0 < radius <= screen_width * 4:
            # 0th order circle
            if self.order >= 0:
                # self.pen.color = "ffffff"
                self.objects.append(Path.ellipse_from_center(self.origin, None, Unit(radius), Unit(radius),
                                                             Brush.no_brush(), self.pen))
            # 1st order reflections
            if self.order >= 1:
                # self.pen.color = "dddddd"
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
                # self.pen.color = "bbbbbb"
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
                # self.pen.color = "999999"
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
            # self._check_for_contact(radius, self.distances)
        else:
            return self.id
        # self.prev_rad = radius

    def _calculate_reticle_to_drums(self):
        distances = []
        for i in self.objects:
            for j in self.drum_positions:
                distances.append((math.sqrt((i.x.base_value - j[0]) ** 2 + (i.y.base_value - j[1]) ** 2), j[2]))
        return distances

    def _check_for_contact(self, radius, distances, now):
        global scrollers
        for idx, i in enumerate(distances):
            if self.drum_positions[idx % len(self.drum_positions)][3]:
                if self.prev_rad / 2 < i[0] < radius / 2:
                    id = get_id()
                    scrollers[id] = Scroller(i[1], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                             self.pen.__getattribute__("color"), now)
                    return self.drum_positions[idx % len(self.drum_positions)][2]

    def set_drum_locations(self, drums_array):
        self.drum_positions = []
        for i in drums_array:
            self.drum_positions.append((drums_array[i].x.base_value, drums_array[i].y.base_value,
                                        drums_array[i].drum_num, drums_array[i].reveal))


class LineReticle:
    def __init__(self, ul, ur, bl, br, direction, id=0, pen=None, velocity=200, now=0):
        self.id = id
        self.init_time = now
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = abs((ul[1] - bl[1]).base_value)
        self.objects = []
        self.pen = pen
        self.drum_positions = []
        self.tick = 1
        self.velocity = velocity
        self.distances = []
        self.direction = direction
        match self.direction:
            case "right":
                self.prev_pos = 0
            case "left":
                self.prev_pos = self.box_width
            case "down":
                self.prev_pos = hud_height
            case "up":
                self.prev_pos = self.box_height
        with open(data_file, 'a') as df:
            to_write = "reticle, " + "line" + ", atk_time, " + str(now+scroll_time) + \
                        ", pen_pattern, " + str(pen.pattern) + ", dynamic, " + str(pen.color) + \
                        ", id, " + str(self.id) + "\n"
            df.write(to_write)

    def animate(self, now):
        trash2 = None
        trash1, drum_hit = self._animate_trace(now)
        if (now - self.init_time) > scroll_time:
            trash2 = self._animate_actual(now)
        return trash1, trash2, drum_hit

    def _animate_trace(self, now):
        match self.direction:
            case "right":
                pos = (now - self.init_time) * self.velocity
            case "left":
                pos = self.box_width - (now - self.init_time) * self.velocity
            case "down":
                pos = (now - self.init_time) * self.velocity + hud_height
            case "up":
                pos = self.box_height - (now - self.init_time) * self.velocity + hud_height
        for i in self.objects:
            i.remove()
        self.objects = []
        if -(3 * self.box_width) <= pos <= (self.box_width * 3):
            if self.direction == "right" or self.direction == "left":
                self.objects.append(Path.straight_line((Unit(pos), self.ul[1]), None,
                                                       (Unit(0), Unit(self.box_height)), None,
                                                       Brush.no_brush(), Pen.no_pen()))
            if self.direction == "up" or self.direction == "down":
                self.objects.append(Path.straight_line((Unit(0), Unit(pos) + self.ul[1]), None,
                                                       (Unit(self.box_width), Unit(0)), None,
                                                       Brush.no_brush(), Pen.no_pen()))
            drum_hit = self._check_for_contact(pos, now)
            self.prev_pos = pos
            return None, drum_hit
        else:
            return self.id, None

    def _animate_actual(self, now):
        match self.direction:
            case "right":
                pos = (now - self.init_time - scroll_time) * self.velocity
            case "left":
                pos = self.box_width - (now - self.init_time - scroll_time) * self.velocity
            case "down":
                pos = (now - self.init_time - scroll_time) * self.velocity
            case "up":
                pos = self.box_height - (now - self.init_time - scroll_time) * self.velocity
        for i in self.objects:
            i.remove()
        self.objects = []
        if 0 <= pos <= self.box_width:
            if self.direction == "right" or self.direction == "left":
                self.objects.append(Path.straight_line((Unit(pos), self.ul[1]), None,
                                                       (Unit(0), Unit(self.box_height)), None,
                                                       Brush.no_brush(), self.pen))
            if self.direction == "up" or self.direction == "down":
                self.objects.append(Path.straight_line((Unit(0), Unit(pos) + self.ul[1]), None,
                                                       (Unit(self.box_width), Unit(0)), None,
                                                       Brush.no_brush(), self.pen))
            # self._check_for_contact(pos)
        else:
            return self.id

    def _check_for_contact(self, pos, now):
        global scrollers
        for i in self.drum_positions:
            if i[3]:
                match self.direction:
                    case "right":
                        if self.prev_pos < i[0] < pos:
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now=now)
                            return i[2]
                    case "down":
                        if self.prev_pos < i[1] < pos:
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now=now)
                            return i[2]
                    case "left":
                        if self.prev_pos > i[0] > pos:
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now=now)
                            return i[2]
                    case "up":
                        if self.prev_pos > i[1] > pos:
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now=now)
                            return i[2]

    def set_drum_locations(self, drums_array):
        self.drum_positions = []
        for i in drums_array:
            self.drum_positions.append((drums_array[i].x.base_value, drums_array[i].y.base_value,
                                        drums_array[i].drum_num, drums_array[i].reveal))


class RadarReticle:
    def __init__(self, ul, ur, bl, br, direction, id=0, pen=None, velocity=0.5, now=0):
        self.id = id
        self.init_time = now
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = abs((ul[1] - bl[1]).base_value)
        self.origin = (Unit(self.box_width / 2), Unit(4 * self.box_height / 5))
        self.length = 1000
        self.objects = []
        self.pen = pen
        self.drum_positions = []
        self.tick = 1
        self.velocity = velocity
        self.angles = []
        self.direction = direction
        self.prev_angle = 0
        with open(data_file, 'a') as df:
            to_write = "reticle, " + "radar" + ", atk_time, " + str(now+scroll_time) + \
                        ", pen_pattern, " + str(pen.pattern) + ", dynamic, " + str(pen.color) + \
                        ", id, " + str(self.id) + "\n"
            df.write(to_write)

    def animate(self, now):
        trash2 = None
        trash1, drum_hit = self._animate_trace(now)
        if (now - self.init_time) > scroll_time:
            trash2 = self._animate_actual(now)
        return trash1, trash2, drum_hit

    def _animate_trace(self, now):
        match self.direction:
            case "cw":
                angle = (now - self.init_time) * self.velocity
            case "ccw":
                angle = - (now - self.init_time) * self.velocity
        for i in self.objects:
            i.remove()
        self.objects = []
        if abs(angle) < 2 * math.pi:
            self.objects.append(Path.straight_line(self.origin, None,
                                                   (self.length * Unit(math.cos(angle)),
                                                    self.length * Unit(math.sin(angle))),
                                                   brush=Brush.no_brush(), pen=Pen.no_pen()))
            if self.tick == 1:
                self.angles = self._calculate_reticle_to_drums()
                self.tick = 2
            drum_hit = self._check_for_contact(angle, now)
            self.prev_angle = angle
            return None, drum_hit
        elif abs(angle) < 4 * math.pi:
            self.prev_angle = angle
        else:
            return self.id

    def _animate_actual(self, now):
        match self.direction:
            case "cw":
                angle = (now - self.init_time - scroll_time) * self.velocity
            case "ccw":
                angle = - (now - self.init_time - scroll_time) * self.velocity
        for i in self.objects:
            i.remove()
        self.objects = []
        if abs(angle) < 2 * math.pi:
            self.objects.append(Path.straight_line(self.origin, None,
                                                   (self.length * Unit(math.cos(angle)),
                                                    self.length * Unit(math.sin(angle))),
                                                   brush=Brush.no_brush(), pen=self.pen))
        else:
            return self.id

    def _calculate_reticle_to_drums(self):
        angles = []
        for i in self.objects:
            for j in self.drum_positions:
                origin_to_drum = math.sqrt((self.origin[0].base_value - j[0]) ** 2 +
                                           (self.origin[1].base_value - j[1]) ** 2)
                angle_to_drum = math.acos((j[0] - self.origin[0].base_value) / origin_to_drum)
                if j[1] < self.origin[1].base_value:
                    angle_to_drum = (-angle_to_drum) % (2 * math.pi)
                angles.append(angle_to_drum)
        return angles

    def _check_for_contact(self, angle, now):
        global scrollers
        for idx, i in enumerate(self.drum_positions):
            if i[3]:
                match self.direction:
                    case "cw":
                        if self.prev_angle < self.angles[idx] < angle:
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now)
                            return i[2]
                    case "ccw":
                        if self.prev_angle % (2 * math.pi) > self.angles[idx] > angle % (2 * math.pi):
                            id = get_id()
                            scrollers[id] = Scroller(i[2], scroll_time, id, str(self.pen.__getattribute__("pattern")),
                                                     self.pen.__getattribute__("color"), now)
                            return i[2]

    def set_drum_locations(self, drums_array):
        self.drum_positions = []
        for i in drums_array:
            self.drum_positions.append((drums_array[i].x.base_value, drums_array[i].y.base_value,
                                        drums_array[i].drum_num, drums_array[i].reveal))


class Drum:
    def __init__(self, location, drum_num, reveal=True):
        self.loc = location
        self.init_time = time.time()
        self.x = location[0]
        self.y = location[1]
        self.objects = []
        self.rad = 25
        self.drum_num = drum_num
        self.reveal = reveal
        if self.reveal:
            self.pen = Pen("ffffff", thickness=Unit(2))
        else:
            self.pen = Pen.no_pen()
        self.objects.append(
            Path.ellipse_from_center(self.loc, None, Unit(self.rad), Unit(self.rad), Brush.no_brush(), pen=self.pen))
        self.objects.append(Text(self.loc, None, str(drum_num), pen=self.pen))

    def animate(self):
        radius = (time.time() - self.init_time) * 30
        for i in self.objects:
            i.remove()
        self.objects = []
        self.objects.append(
            Path.ellipse_from_center(self.loc, None, Unit(self.rad), Unit(self.rad), Brush.no_brush(), pen=self.pen))
        self.objects.append(Text(self.loc, None, str(self.drum_num), pen=self.pen))
        if radius < self.rad:
            self.objects.append(Path.ellipse_from_center(self.loc, None, Unit(radius), Unit(radius),
                                                         brush=Brush("#11111166"), pen=self.pen))
        elif self.rad < radius < (self.rad * (6 / 5)):
            shrink_rad = self.rad + (24 / 5) * (self.rad - radius)
            self.objects.append(Path.ellipse_from_center(self.loc, None, Unit(shrink_rad), Unit(shrink_rad),
                                                         brush=Brush("#e8fc03ff"), pen=self.pen))

    def reset_animation(self):
        self.init_time = time.time()

    def toggle(self):
        self.reveal = not self.reveal
        print(self.reveal)
        if self.reveal:
            self.pen = Pen("ffffff", thickness=Unit(2))
        else:
            self.pen = Pen.no_pen()
        self.reset_animation()


class Scroller:
    def __init__(self, drum_num, time_to_hit=2, id=0,
                 ret_pattern="PenPattern.SOLID", brush=Brush("666666"), now=0):
        self.init_time = now
        self.drum_num = drum_num
        self.objects = []
        self.time_to_hit = time_to_hit
        self.travel_to_hit = screen_width - 50
        self.rate = self.travel_to_hit / self.time_to_hit
        self.id = id
        match ret_pattern:
            case "PenPattern.SOLID":
                self.dynamic = "dynamicForte"
                self.brush = brush
                self.note_head = "noteheadBlack"
            case "PenPattern.DASH":
                self.dynamic = "dynamicMezzo"
                self.brush = brush
                self.note_head = "noteheadHeavyX"
            case "PenPattern.DOT":
                self.dynamic = "dynamicPiano"
                self.brush = brush
                self.note_head = "noteheadLargeArrowDownBlack"
        with open(data_file, 'a') as df:
            to_write = "drum_num, " + str(self.drum_num) + ", atk_time, " + str(now+scroll_time) + \
                        ", pen_pattern, " + str(ret_pattern) + ", dynamic, " + str(self.dynamic) + \
                        ", id, " + str(self.id) + "\n"
            df.write(to_write)

    def get_staff_pos(self):
        match self.drum_num:
            case 0:
                return 0
            case 1:
                return 2
            case 2:
                return 4
            case 3:
                return 1
            case 4:
                return 3
            case 5:
                return 5
            case 6:
                return 6
            case 7:
                return 8
            case 8:
                return 10
            case 9:
                return 7
            case 10:
                return 9
            case 11:
                return 11

    def animate(self, now):
        for i in self.objects:
            i.remove()
        self.objects = []
        pos = (now - self.init_time) * self.rate
        if pos < screen_width:
            if self.drum_num == 11:
                pen = Pen("999999", Unit(2))
                self.objects.append(Path.straight_line((Unit(screen_width - pos - 5), Unit(70)), None,
                                                       (Unit(20), Unit(0)), pen=pen))
            self.objects.append(MusicText((Unit(screen_width - pos), Unit(5 * (self.get_staff_pos() + 1) + 10)),
                                          None, self.note_head, MusicFont("Bravura", Unit(8)), brush=self.brush))
        else:
            return self.id


def get_id():
    global count
    count = count + 1
    return count


def cleanup(dict_name, trash):
    global reticles, scrollers
    for i in trash:
        if type(i) == int or type(i) == tuple:
            if dict_name == "reticles":
                try:
                    del reticles[i[0]]
                    del reticles[i[1]]
                except:
                    pass
            elif dict_name == "scrollers":
                del scrollers[i]


def redraw_top_layer(top_layer_list, ulp, urp, brp, blp, width):
    for i in top_layer_list:
        i.remove()
    top_layer_list = []
    top_layer_list.append(Path.rect(ulp, None, Unit(2000), -Unit(2000), Brush("#222222"), Pen.no_pen()))
    top_layer_list.append(Path.rect(urp, None, Unit(2000), Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    top_layer_list.append(Path.rect(brp, None, -Unit(2000), Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    top_layer_list.append(Path.rect(blp, None, -Unit(2000), -Unit(2000), Brush("#eeeeee"), Pen.no_pen()))
    for i in range(5):
        top_layer_list.append(Path.straight_line((Unit(0), Unit(20 + (i * 10))), None, (Unit(width), Unit(0)),
                                                 pen=Pen("888888", thickness=Unit(3), pattern=PenPattern.SOLID)))
    top_layer_list.append(Path.straight_line((Unit(50), Unit(0)), None, (Unit(0), Unit(hud_height)),
                                            pen=Pen("ffffff", thickness=Unit(4))))
    return top_layer_list


def refresh_func(global_time: float) -> Optional[neoscore.RefreshFuncResult]:
    global reticles, top_layer, piece_time
    piece_time = global_time - start_time
    # sequence_reticles(piece_time, my_sequence)
    trash = []
    for i in reticles:
        trash.append(reticles[i].animate(piece_time))
    cleanup("reticles", trash)
    for i in drums:
        drums[i].animate()
    top_layer = redraw_top_layer(top_layer, ULP, URP, BRP, BLP, screen_width)
    trash = []
    for i in scrollers:
        trash.append(scrollers[i].animate(piece_time))
    cleanup("scrollers", trash)


def key_handler(event):
    global ret_pen, velo
    if event.event_type == KeyEventType.PRESS:
        print(event.code)
        if event.code == 16777236:  # right arrow
            id = get_id()
            reticles[id] = LineReticle(ULP, URP, BLP, BRP, "right", id, ret_pen, velocity=velo, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 16777234:  # left arrow
            id = get_id()
            reticles[id] = LineReticle(ULP, URP, BLP, BRP, "left", id, ret_pen, velocity=velo, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 16777235:  # up arrow
            id = get_id()
            reticles[id] = LineReticle(ULP, URP, BLP, BRP, "up", id, ret_pen, velocity=velo, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 16777237:  # down arrow
            id = get_id()
            reticles[id] = LineReticle(ULP, URP, BLP, BRP, "down", id, ret_pen, velocity=velo, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 91:  # [
            id = get_id()
            reticles[id] = RadarReticle(ULP, URP, BLP, BRP, "cw", id, ret_pen, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 93:  # ]
            id = get_id()
            reticles[id] = RadarReticle(ULP, URP, BLP, BRP, "ccw", id, ret_pen, now=piece_time)
            reticles[id].set_drum_locations(drums)
        if event.code == 48:  # 0
            velo = 10
        if event.code == 49:  # 1
            velo = 20
        if event.code == 50:  # 2
            velo = 40
        if event.code == 51:  # 3
            velo = 60
        if event.code == 52:  # 4
            velo = 80
        if event.code == 53:  # 5
            velo = 100
        if event.code == 54:  # 6
            velo = 150
        if event.code == 55:  # 7
            velo = 200
        if event.code == 56:  # 8
            velo = 250
        if event.code == 57:  # 9
            velo = 300
        if event.code == 81:  # Q
            drums[0].toggle()
        if event.code == 65:  # A
            drums[1].toggle()
        if event.code == 90:  # Z
            drums[2].toggle()
        if event.code == 87:  # W
            drums[3].toggle()
        if event.code == 83:  # S
            drums[4].toggle()
        if event.code == 88:  # X
            drums[5].toggle()
        if event.code == 69:  # E
            drums[6].toggle()
        if event.code == 68:  # D
            drums[7].toggle()
        if event.code == 67:  # C
            drums[8].toggle()
        if event.code == 82:  # R
            drums[9].toggle()
        if event.code == 70:  # F
            drums[10].toggle()
        if event.code == 86:  # V
            drums[11].toggle()
        if event.code == 44:  # ,
            ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=Unit(2), pattern=PenPattern.DASH)
        if event.code == 46:  # .
            ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=Unit(2), pattern=PenPattern.DOT)
        if event.code == 47:  # /
            ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=Unit(2), pattern=PenPattern.SOLID)
        if event.code == 74:  # J
            ret_pen = Pen("ffffff", thickness=Unit(2), pattern=ret_pen.__getattribute__("pattern"))
        if event.code == 75:  # K
            ret_pen = Pen("ff0000", thickness=Unit(2), pattern=ret_pen.__getattribute__("pattern"))
        if event.code == 76:  # L
            ret_pen = Pen("00ff00", thickness=Unit(2), pattern=ret_pen.__getattribute__("pattern"))
        if event.code == 59:  # ;
            ret_pen = Pen("0000ff", thickness=Unit(2), pattern=ret_pen.__getattribute__("pattern"))
        # for i in drums:
        #     i.reset_animation()


def mouse_handler(event):
    if event.event_type == MouseEventType.PRESS:
        x, y = event.document_pos
        if ULP[0] < x < URP[0] and ULP[1] < y < BLP[1]:
            id = get_id()
            reticles[id] = CircleReticle((x, y), ULP, URP, BLP, BRP, id, pen=ret_pen, velocity=velo, now=piece_time)
            reticles[id].set_drum_locations(drums)


def sequence_reticles(piece_time, collection):
    if len(collection) > 0:
        done = collection[0][1](collection[0][2], collection[0][0], piece_time, collection[0][3])
        if done:
            collection.pop(0)


def circle(pos, onset_time, piece_time, drum_dict):
    if piece_time > onset_time:
        x, y = pos
        id = get_id()
        reticles[id] = CircleReticle((x, y), ULP, URP, BLP, BRP, id, pen=ret_pen, velocity=velo, now=piece_time)
        reticles[id].set_drum_locations(drum_dict)
        return True
    else:
        return False


def line(direction, onset_time, piece_time, drum_dict):
    global reticles
    if piece_time > onset_time:
        id = get_id()
        reticles[id] = LineReticle(ULP, URP, BLP, BRP, direction, id, ret_pen, velocity=velo, now=piece_time)
        reticles[id].set_drum_locations(drum_dict)
        return True
    else:
        return False


def radar(direction, onset_time, piece_time, drum_dict):
    if piece_time > onset_time:
        id = get_id()
        reticles[id] = RadarReticle(ULP, URP, BLP, BRP, direction, id, ret_pen, now=piece_time)
        reticles[id].set_drum_locations(drum_dict)
        return True
    else:
        return False


def set_color(color, onset_time, piece_time, null=None):
    global ret_pen
    if piece_time > onset_time:
        match color:
            case "black":
                ret_pen = Pen("ffffff", thickness=ret_pen.__getattribute__("thickness"),
                              pattern=ret_pen.__getattribute__("pattern"))
            case "red":
                ret_pen = Pen("ff0000", thickness=ret_pen.__getattribute__("thickness"),
                              pattern=ret_pen.__getattribute__("pattern"))
            case "green":
                ret_pen = Pen("00ff00", thickness=ret_pen.__getattribute__("thickness"),
                              pattern=ret_pen.__getattribute__("pattern"))
            case "blue":
                ret_pen = Pen("0000ff", thickness=ret_pen.__getattribute__("thickness"),
                              pattern=ret_pen.__getattribute__("pattern"))
            case _:
                ret_pen = Pen(color, thickness=ret_pen.__getattribute__("thickness"),
                              pattern=ret_pen.__getattribute__("pattern"))
        return True
    else:
        return False


def set_pattern(pattern, onset_time, piece_time, null=None):
    global ret_pen
    if piece_time > onset_time:
        match pattern:
            case "SOLID":
                ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=ret_pen.__getattribute__("thickness"),
                              pattern=PenPattern.SOLID)
            case "DOT":
                ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=ret_pen.__getattribute__("thickness"),
                              pattern=PenPattern.DOT)
            case "DASH":
                ret_pen = Pen(ret_pen.__getattribute__("color"), thickness=ret_pen.__getattribute__("thickness"),
                              pattern=PenPattern.DASH)
        return True
    else:
        return False


def set_velo(velocity, onset_time, piece_time, null=None):
    global velo
    if piece_time > onset_time:
        velo = velocity
        return True
    else:
        return False


def make_sequencable_collection():
    collection = []
    for i in range(10):
        collection.append((3 * i, line, "right", drums))
    for i in range(10):
        collection.append((2.75 * i + 30, line, "down", drums))
    for i in range(5):
        collection.append((2.5 * i + 57.5, line, "left", drums))
    for i in range(4):
        collection.append((20 * i - 0.1, set_velo, 80 + 10 * i, drums))
    collection.append((1, circle, (Unit(200), Unit(300)), drums))
    collection.append((2, line, "left", drums))
    collection.append((1.75, set_color, "blue", drums))
    collection.append((1.750001, set_pattern, "DOT", drums))
    collection.append((1.5, radar, "ccw", drums))
    collection.sort()
    return collection


if __name__ == '__main__':
    my_sequence = make_sequencable_collection()
    data_file = "interactive.data"
    open(data_file, 'w').close()

    w = screen_width / 13
    h = (screen_height - 160) / 13
    drums[0] = Drum((Unit(1 * w), Unit(1 * h + 160)), 0)
    drums[1] = Drum((Unit(2 * w), Unit(5 * h + 160)), 1)
    drums[2] = Drum((Unit(3 * w), Unit(9 * h + 160)), 2)
    drums[3] = Drum((Unit(4 * w), Unit(2 * h + 160)), 3)
    drums[4] = Drum((Unit(5 * w), Unit(6 * h + 160)), 4)
    drums[5] = Drum((Unit(6 * w), Unit(10 * h + 160)), 5)
    drums[6] = Drum((Unit(9 * w), Unit(3 * h + 160)), 6)
    drums[7] = Drum((Unit(8 * w), Unit(7 * h + 160)), 7)
    drums[8] = Drum((Unit(7 * w), Unit(11 * h + 160)), 8)
    drums[9] = Drum((Unit(12 * w), Unit(4 * h + 160)), 9)
    drums[10] = Drum((Unit(11 * w), Unit(8 * h + 160)), 10)
    drums[11] = Drum((Unit(10 * w), Unit(12 * h + 160)), 11)
    MusicText((Unit(-20), Unit(100)), None, "noteheadBlack",
              MusicFont("Bravura", Unit(6)))
    neoscore.set_key_event_handler(key_handler)
    neoscore.set_mouse_event_handler(mouse_handler)

    neoscore.set_viewport_center_pos((Unit(screen_width / 2), Unit(screen_height / 2)))
    neoscore.show(refresh_func, display_page_geometry=False, auto_viewport_interaction_enabled=False,
                  min_window_size=(screen_width, screen_height), max_window_size=(screen_width, screen_height))
