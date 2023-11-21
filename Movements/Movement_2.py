import io
import math
import time
from typing import Optional

import imageio
import numpy as np
import PIL.Image as Image
from neoscore.core import neoscore
from neoscore.core.rect import Rect
from neoscore.core.units import Unit
from neoscore.core.image import Image as im

from main import Drum, line, set_velo, cleanup, redraw_top_layer, sequence_reticles, circle, set_color, set_pattern, \
    radar
from config import *


def make_drums():
    w = screen_width / 13
    h = (screen_height - hud_height) / 13
    dict = {}
    dict[0] = Drum((Unit(1 * w), Unit(1 * h + 160)), 0)
    dict[1] = Drum((Unit(2 * w), Unit(5 * h + 160)), 1)
    dict[2] = Drum((Unit(3 * w), Unit(9 * h + 160)), 2)
    dict[3] = Drum((Unit(4 * w), Unit(2 * h + 160)), 3)
    dict[4] = Drum((Unit(5 * w), Unit(6 * h + 160)), 4)
    dict[5] = Drum((Unit(6 * w), Unit(10 * h + 160)), 5)
    dict[6] = Drum((Unit(9 * w), Unit(3 * h + 160)), 6)
    dict[7] = Drum((Unit(8 * w), Unit(7 * h + 160)), 7)
    dict[8] = Drum((Unit(7 * w), Unit(11 * h + 160)), 8)
    dict[9] = Drum((Unit(12 * w), Unit(4 * h + 160)), 9)
    dict[10] = Drum((Unit(11 * w), Unit(8 * h + 160)), 10)
    dict[11] = Drum((Unit(10 * w), Unit(12 * h + 160)), 11)
    return dict


def make_sequence():
    collection = []
    for i in range(20):
        collection.append((5 * i - 0.1, set_color, "ff3878", drums))
        collection.append((5 * i, line, "left", drums))
    # for i in range(20):
    #     collection.append((5 * i + 1 - 0.1, set_color, "f271c0", drums))
    #     collection.append((5 * i + 1, line, "up", drums))
    # for i in range(20):
    #     collection.append((5 * i + 2 - 0.1, set_color, "cf9fe9", drums))
    #     collection.append((5 * i + 2, line, "right", drums))
    # for i in range(20):
    #     collection.append((5 * i + 3 - 0.1, set_color, "bbc1f2", drums))
    #     collection.append((5 * i + 3, line, "down", drums))
    # for i in range(20):
    #     collection.append((4 * i + 0.1, set_velo, 80 + 5 * i, drums))

    # for i in range(25):
    #     collection.append((3 * i, line, "left", drums))
    # for i in range(10):
    #     collection.append((2.75 * i + 30, line, "down", drums))
    # for i in range(5):
    #     collection.append((2.5 * i + 57.5, line, "left", drums))
    # for i in range(20):
    #     collection.append((4 * i - 0.1, set_velo, 80 + 10 * i, drums))
    # collection.append((81.2, set_velo, 70, drums))
    # for i in range(10):
    #     collection.append((2 * i + 75, line, "left", drums))
    # collection.append((1, circle, (Unit(200), Unit(300)), drums))
    # collection.append((2, line, "left", drums))
    # collection.append((-0.75, set_color, "f41218", drums))
    # collection.append((-0.75, set_color, "ff3878", drums))
    # collection.append((-0.75, set_color, "f271c0", drums))
    # collection.append((-0.75, set_color, "cf9fe9", drums))
    # collection.append((-0.75, set_color, "bbc1f2", drums))
    # collection.append((1.750001, set_pattern, "DOT", drums))
    # collection.append((1.5, radar, "ccw", drums))
    collection.sort()
    return collection


def animate_all(global_time):
    global reticles, top_layer, piece_time, top_layer
    my_image.opacity = abs(math.sin(global_time)) - 0.5
    if render_to_file:
        piece_time = global_time
    else:
        piece_time = global_time - start_time
    print(piece_time)
    sequence_reticles(piece_time, my_sequence)
    trash = []
    for i in reticles:
        trash.append(reticles[i].animate(piece_time))
    cleanup("reticles", trash)
    for i in drums:
        drums[i].animate(piece_time)
    top_layer = redraw_top_layer(top_layer, ULP, URP, BRP, BLP, screen_width)
    trash = []
    for i in scrollers:
        trash.append(scrollers[i].animate(piece_time))
    cleanup("scrollers", trash)


def render_func():
    b_array = bytearray()
    writer = imageio.get_writer(video_name, mode="I", fps=fps)
    for i in range(fps * piece_duration):
        print(round(i/fps, 2), "/", piece_duration, "seconds rendered")
        animate_all(i/fps)
        neoscore.render_image(Rect(Unit(0), Unit(0), Unit(screen_width), Unit(screen_height)), b_array, quality=50)
        image = np.array(Image.open(io.BytesIO(b_array)))  # pip install imageio[ffmpeg]
        writer.append_data(image)
    writer.close()


def refresh_func(global_time: float) -> Optional[neoscore.RefreshFuncResult]:
    animate_all(global_time)


if __name__ == '__main__':
    render_to_file = False
    drums = make_drums()
    my_sequence = make_sequence()
    open(data_file, 'w').close()  # This wipes the file
    my_image = im((Unit(0), Unit(0)), None, "../Assets/test_pic.png")
    if render_to_file:
        render_func()
    else:
        neoscore.set_viewport_center_pos((Unit(screen_width / 2), Unit(screen_height / 2)))
        neoscore.show(refresh_func, display_page_geometry=False, auto_viewport_interaction_enabled=False,
                      min_window_size=(screen_width, screen_height), max_window_size=(screen_width, screen_height))
