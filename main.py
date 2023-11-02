import math
import time
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.key_event import KeyEventType
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.units import Unit


class CircleReticle:
    def __init__(self, origin, ul, ur, bl, br, order=1):
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

    def animate(self):
        radius = (time.time() - self.init_time) * 200 + 1
        for i in self.objects:
            i.remove()
        self.objects = []
        if radius < 3000:
            # 0th order circle
            if self.order >= 0:
                self.objects.append(Path.ellipse_from_center(self.origin, None, Unit(radius), Unit(radius),
                                                             Brush.no_brush(), self.pen))
            # 1st order reflections
            if self.order >= 1:
                self.objects.append(Path.ellipse_from_center((self.origin[0] + 2 * self.right_dist, self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0] - 2 * self.left_dist, self.origin[1]), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0], self.origin[1] - 2 * self.top_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
                self.objects.append(Path.ellipse_from_center((self.origin[0], self.origin[1] + 2 * self.bottom_dist), None,
                                                             Unit(radius), Unit(radius), Brush.no_brush(), self.pen))
            # 2nd order reflections
            if self.order >= 2:
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


def redraw_top_layer():
    global top_layer
    for i in top_layer:
        i.remove()
    top_layer = []
    top_layer.append(Path.rect(UL_point, None, Unit(2000), -Unit(2000), Brush("#ffffff"), Pen.no_pen()))
    top_layer.append(Path.rect(UR_point, None, Unit(2000), Unit(2000), Brush("#ffffff"), Pen.no_pen()))
    top_layer.append(Path.rect(BR_point, None, -Unit(2000), Unit(2000), Brush("#ffffff"), Pen.no_pen()))
    top_layer.append(Path.rect(BL_point, None, -Unit(2000), -Unit(2000), Brush("#ffffff"), Pen.no_pen()))


def refresh_func(current_time: float) -> Optional[neoscore.RefreshFuncResult]:
    global reticles
    for i in reticles:
        i.animate()
    redraw_top_layer()


def key_handler(event):
    if event.event_type == KeyEventType.PRESS:
        # reticles.append(CircleReticle(Center, UL_point, UR_point, BL_point, BR_point))
        print("hi!")


def mouse_handler(event):
    if event.event_type == MouseEventType.PRESS:
        x, y = event.document_pos
        if UL_point[0] < x < UR_point[0] and UL_point[1] < y < BL_point[1]:
            reticles.append(CircleReticle((x, y), UL_point, UR_point, BL_point, BR_point))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    neoscore.setup()

    pen = Pen("000000", thickness=Unit(2))
    UL_point = (Unit(0), Unit(0))
    UR_point = (Unit(500), Unit(0))
    BL_point = (Unit(0), Unit(500))
    BR_point = (Unit(500), Unit(500))
    UL = Path.ellipse(UL_point, None, Unit(0), Unit(0), pen=pen)
    UR = Path.ellipse(UR_point, None, Unit(0), Unit(0), pen=pen)
    BL = Path.ellipse(BL_point, None, Unit(0), Unit(0), pen=pen)
    BR = Path.ellipse(BR_point, None, Unit(0), Unit(0), pen=pen)
    Zero = (Unit(0), Unit(0))
    Center = (Unit(250), Unit(250))
    Path.straight_line(Zero, UL, Zero, UR, pen=pen)
    Path.straight_line(Zero, UR, Zero, BR, pen=pen)
    Path.straight_line(Zero, BR, Zero, BL, pen=pen)
    Path.straight_line(Zero, BL, Zero, UL, pen=pen)
    top_layer = []
    reticles = []
    # reticles.append(CircleReticle(Center, UL_point, UR_point, BL_point, BR_point))
    start_time = time.time()

    neoscore.set_key_event_handler(key_handler)
    neoscore.set_mouse_event_handler(mouse_handler)
    neoscore.show(refresh_func, display_page_geometry=False)
