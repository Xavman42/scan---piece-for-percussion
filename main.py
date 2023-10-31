import math
import time
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.units import Unit


class CircleReticle:
    def __init__(self, center, pen, ul, ur, bl, br, id_num=0):
        self.id_num = id_num
        self.center = center
        self.pen = pen
        self.ul = ul
        self.ur = ur
        self.bl = bl
        self.br = br
        self.box_width = (ur[0] - ul[0]).base_value
        self.box_height = (ul[1] - bl[1]).base_value
        # self.object = Path.ellipse_from_center(self.center, None,
        #                                        width=Unit((math.sin(0) + 1) * 200),
        #                                        height=Unit((math.sin(0) + 1) * 200),
        #                                        brush=Brush.no_brush(),
        #                                        pen=self.pen)
        self.object_1 = Path.arc(self.center, None, Unit(1), Unit(1), 0, math.pi / 2, Brush.no_brush(), self.pen)
        self.object_2 = Path.arc(self.center, None, Unit(1), Unit(1), math.pi / 2, math.pi, Brush.no_brush(), self.pen)
        self.object_3 = Path.arc(self.center, None, Unit(1), Unit(1), math.pi, 3 * math.pi / 2,
                                 Brush.no_brush(), self.pen)
        self.object_4 = Path.arc(self.center, None, Unit(1), Unit(1), 3 * math.pi / 2, 2 * math.pi,
                                 Brush.no_brush(), self.pen)
        self.object_5 = None
        self.object_6 = None
        self.object_7 = None
        self.object_8 = None

    def animate(self, real_time):
        radius = real_time * 200 + 1
        arc_center = (self.center[0] - Unit(radius/2), self.center[1] - Unit(radius/2))
        try:
            self.object_1.remove()
        except:
            pass
        try:
            self.object_2.remove()
        except:
            pass
        try:
            self.object_3.remove()
        except:
            pass
        try:
            self.object_4.remove()
        except:
            pass
        try:
            self.object_5.remove()
        except:
            pass
        try:
            self.object_6.remove()
        except:
            pass
        try:
            self.object_7.remove()
        except:
            pass
        try:
            self.object_8.remove()
        except:
            pass
        if radius < self.box_width:
            self.object_1 = Path.arc(arc_center, None, Unit(radius), Unit(radius), 0, math.pi / 2,
                                     Brush.no_brush(), self.pen)
            self.object_2 = Path.arc(arc_center, None, Unit(radius), Unit(radius), math.pi / 2, math.pi,
                                     Brush.no_brush(), self.pen)
            self.object_3 = Path.arc(arc_center, None, Unit(radius), Unit(radius), math.pi, 3 * math.pi / 2,
                                     Brush.no_brush(), self.pen)
            self.object_4 = Path.arc(arc_center, None, Unit(radius), Unit(radius), 3 * math.pi / 2, 2 * math.pi,
                                     Brush.no_brush(), self.pen)
        elif self.box_width < radius < (self.box_width * math.sqrt(2)):
            self.object_1 = Path.arc(arc_center, None, Unit(radius), Unit(radius), math.acos(self.box_width/radius),
                                     math.pi / 2 - math.acos(self.box_width/radius), Brush.no_brush(), self.pen)
            self.object_2 = Path.arc(arc_center, None, Unit(radius), Unit(radius),
                                     math.pi / 2 + math.acos(self.box_width/radius),
                                     math.pi - math.acos(self.box_width/radius),
                                     Brush.no_brush(), self.pen)
            self.object_3 = Path.arc(arc_center, None, Unit(radius), Unit(radius),
                                     math.pi + math.acos(self.box_width/radius),
                                     (3 * math.pi / 2) - math.acos(self.box_width/radius),
                                     Brush.no_brush(), self.pen)
            self.object_4 = Path.arc(arc_center, None, Unit(radius), Unit(radius),
                                     (3 * math.pi / 2) + math.acos(self.box_width/radius),
                                     2 * math.pi - math.acos(self.box_width/radius),
                                     Brush.no_brush(), self.pen)
            self.object_5 = Path.arc((arc_center[0] + 2 * self.center[0], arc_center[1]), None,
                                     Unit(radius), Unit(radius), math.pi - math.acos(self.box_width/radius),
                                     math.pi + math.acos(self.box_width/radius), Brush.no_brush(), self.pen)
            self.object_6 = Path.arc((arc_center[0], arc_center[1] + 2 * self.center[1]), None,
                                     Unit(radius), Unit(radius), (3 * math.pi / 2) - math.acos(self.box_width/radius),
                                     (3 * math.pi / 2) + math.acos(self.box_width/radius), Brush.no_brush(),
                                     self.pen)
            self.object_7 = Path.arc((arc_center[0] - 2 * self.center[0], arc_center[1]), None,
                                     Unit(radius), Unit(radius),  - math.acos(self.box_width/radius),
                                     math.acos(self.box_width / radius), Brush.no_brush(),
                                     self.pen)
            self.object_8 = Path.arc((arc_center[0], arc_center[1] - 2 * self.center[1]), None,
                                     Unit(radius), Unit(radius), (math.pi / 2) - math.acos(self.box_width/radius),
                                     (math.pi / 2) + math.acos(self.box_width/radius), Brush.no_brush(),
                                     self.pen)
        elif radius > (self.box_width * math.sqrt(2)):
            self.object_5 = Path.arc((arc_center[0] + 2 * self.center[0], arc_center[1]), None,
                                     Unit(radius), Unit(radius), math.pi - math.acos(self.box_width / radius),
                                     math.pi + math.acos(self.box_width / radius), Brush.no_brush(), self.pen)
            self.object_6 = Path.arc((arc_center[0], arc_center[1] + 2 * self.center[1]), None,
                                     Unit(radius), Unit(radius), (3 * math.pi / 2) - math.acos(self.box_width / radius),
                                     (3 * math.pi / 2) + math.acos(self.box_width / radius), Brush.no_brush(),
                                     self.pen)
            self.object_7 = Path.arc((arc_center[0] - 2 * self.center[0], arc_center[1]), None,
                                     Unit(radius), Unit(radius), - math.acos(self.box_width / radius),
                                     math.acos(self.box_width / radius), Brush.no_brush(),
                                     self.pen)
            self.object_8 = Path.arc((arc_center[0], arc_center[1] - 2 * self.center[1]), None,
                                     Unit(radius), Unit(radius), (math.pi / 2) - math.acos(self.box_width / radius),
                                     (math.pi / 2) + math.acos(self.box_width / radius), Brush.no_brush(),
                                     self.pen)
        else:
            pass


def refresh_func(current_time: float) -> Optional[neoscore.RefreshFuncResult]:
    global reticle
    real_time = current_time - start_time
    reticle.animate(real_time)


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
    reticle = CircleReticle(Center, pen, UL_point, UR_point, BL_point, BR_point)
    start_time = time.time()

    neoscore.show(refresh_func)
