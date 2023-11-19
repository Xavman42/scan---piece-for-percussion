import io
import time
from typing import Optional

import imageio
import numpy as np
import PIL.Image as Image
from neoscore.core import neoscore
from neoscore.core.rect import Rect
from neoscore.core.units import Unit

from main import Drum, line, set_velo, cleanup, redraw_top_layer, sequence_reticles, circle, set_color, set_pattern, \
    radar

from config import ret_pen, count, screen_width, screen_height, hud_height, ULP, URP, BLP, BRP, UL, UR, BL, BR, velo, \
    scrollers, reticles, drums, data_file, video_name, fps, start_time, top_layer, piece_duration


def make_drums():
    w = screen_width / 13
    h = (screen_height - hud_height) / 13
    dict = {}
    # dict[0] = Drum((Unit(1 * w), Unit(1 * h + hud_height)), 0)
    dict[1] = Drum((Unit(2 * w), Unit(5 * h + hud_height)), 1)
    dict[2] = Drum((Unit(3 * w), Unit(9 * h + hud_height)), 2)
    # dict[3] = Drum((Unit(4 * w), Unit(2 * h + hud_height)), 3)
    dict[4] = Drum((Unit(5 * w), Unit(6 * h + hud_height)), 4)
    # dict[5] = Drum((Unit(6 * w), Unit(10 * h + hud_height)), 5)
    # dict[6] = Drum((Unit(9 * w), Unit(3 * h + hud_height)), 6)
    # dict[7] = Drum((Unit(8 * w), Unit(7 * h + hud_height)), 7)
    dict[8] = Drum((Unit(7 * w), Unit(11 * h + hud_height)), 8)
    # dict[9] = Drum((Unit(12 * w), Unit(4 * h + hud_height)), 9)
    dict[10] = Drum((Unit(11 * w), Unit(8 * h + hud_height)), 10)
    dict[11] = Drum((Unit(10 * w), Unit(12 * h + hud_height)), 11)
    return dict


def make_sequence():
    collection = []
    collection.append((-0.8, set_velo, 66, drums))
    collection.append((-0.9, set_color, "f41218", drums))
    collection.append((0, circle, (Unit(screen_width/2), Unit(screen_height/2)), drums))
    collection.append((40.1, set_color, "ff3878", drums))
    collection.append((46, radar, "ccw", drums))
    collection.append((49, radar, "cw", drums))
    collection.append((52, radar, "ccw", drums))
    collection.append((55, radar, "cw", drums))
    collection.append((-0.8, set_velo, 30, drums))
    collection.append((55.1, set_color, "f271c0", drums))
    collection.append((55.01, set_pattern, "DOT", drums))
    collection.append((60, circle, (Unit(screen_width / 5), Unit(4 * screen_height / 6)), drums))
    collection.append((60.1, set_color, "bbc1f2", drums))
    collection.append((60.01, set_pattern, "DASH", drums))
    collection.append((64, circle, (Unit(4 * screen_width / 5), Unit(5 * screen_height / 6)), drums))

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
        drums[i].animate()
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

    if render_to_file:
        render_func()
    else:
        neoscore.set_viewport_center_pos((Unit(screen_width / 2), Unit(screen_height / 2)))
        neoscore.show(refresh_func, display_page_geometry=False, auto_viewport_interaction_enabled=False,
                      min_window_size=(screen_width, screen_height), max_window_size=(screen_width, screen_height))
