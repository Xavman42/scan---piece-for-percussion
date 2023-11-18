import time

from neoscore.core import neoscore
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.units import Unit

screen_width = int(1920/2)
screen_height = int(1080/2)
hud_height = 100
ret_pen = Pen("ffffff", thickness=Unit(4), pattern=PenPattern.SOLID)
count = 0
velo = 80
scrollers = {}
reticles = {}
drums = {}
top_layer = []
scroll_time = 8
num_reflections = 1
piece_time = 0
data_file = "Movement_1.data"
fps = 60
piece_duration = 10
video_name = "Movement_1.avi"

neoscore.setup()
neoscore.set_background_brush("#000000")
ULP = (Unit(0), Unit(hud_height))
URP = (Unit(screen_width), Unit(hud_height))
BLP = (Unit(0), Unit(screen_height))
BRP = (Unit(screen_width), Unit(screen_height))
UL = Path.ellipse(ULP, None, Unit(0), Unit(0), pen=Pen.no_pen())
UR = Path.ellipse(URP, None, Unit(0), Unit(0), pen=Pen.no_pen())
BL = Path.ellipse(BLP, None, Unit(0), Unit(0), pen=Pen.no_pen())
BR = Path.ellipse(BRP, None, Unit(0), Unit(0), pen=Pen.no_pen())
zero = (Unit(0), Unit(0))
Path.straight_line(zero, UL, zero, UR, pen=Pen.no_pen())
Path.straight_line(zero, UR, zero, BL, pen=Pen.no_pen())
Path.straight_line(zero, BR, zero, BL, pen=Pen.no_pen())
Path.straight_line(zero, BL, zero, UL, pen=Pen.no_pen())

start_time = time.time()

print("config complete")
