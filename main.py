import math
from typing import Optional

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import Point, PointDef
from neoscore.core.units import Unit


def refresh_func(time: float) -> Optional[neoscore.RefreshFuncResult]:
    global reticle
    reticle.remove()
    reticle = Path.ellipse_from_center(Center, None,
                                       width=Unit((math.sin(time)+1) * 200),
                                       height=Unit((math.sin(time)+1) * 200),
                                       brush=Brush.no_brush(),
                                       pen=pen)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    neoscore.setup()

    pen = Pen("000000", thickness=Unit(2))
    UL = Path.ellipse((Unit(0), Unit(0)), None, Unit(0), Unit(0), pen=pen)
    UR = Path.ellipse((Unit(500), Unit(0)), None, Unit(0), Unit(0), pen=pen)
    BL = Path.ellipse((Unit(0), Unit(500)), None, Unit(0), Unit(0), pen=pen)
    BR = Path.ellipse((Unit(500), Unit(500)), None, Unit(0), Unit(0), pen=pen)
    Zero = (Unit(0), Unit(0))
    Center = (Unit(250), Unit(250))
    Path.straight_line(Zero, UL, Zero, UR, pen=pen)
    Path.straight_line(Zero, UR, Zero, BR, pen=pen)
    Path.straight_line(Zero, BR, Zero, BL, pen=pen)
    Path.straight_line(Zero, BL, Zero, UL, pen=pen)
    reticle = Path.ellipse_from_center(Center, None, width=Unit(10), height=Unit(10), pen=pen)

    neoscore.show(refresh_func)
