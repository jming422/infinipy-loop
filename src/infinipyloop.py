# Infinipy Loop -- Hackathon project for learning Python desktop GUIs
# Copyright ©2022 Jonathan Ming
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dearpygui.dearpygui as dpg
import math

dpg.create_context()
dpg.create_viewport(title="∞", width=240, height=340, resizable=False)
dpg.setup_dearpygui()


cw = 50
ch = 50

radius = 25

line_color = (137, 58, 63)
bg_color = (255, 201, 219)
# inverted_line_color = (255, 201, 219)
inverted_bg_color = (47, 8, 13)

debuglines = False

gamegrid = [
    ["turn", "turn", "turn", "turn"],
    ["straight", "t", "t", "dot"],
    ["turn", "t", "turn", "turn"],
    ["turn", "x", "t", "t"],
    ["turn", "t", "straight", "dot"],
    ["dot", "turn", "dot", None],
]

solution = [
    [1, 2, 1, 2],
    [0, 1, 3, 0],
    [0, 3, 0, 2],
    [1, 0, 2, 3],
    [0, 3, 0, 0],
    [1, 3, 0, None],
]

items = []


def is_winning():
    # Yes I know this could be more optimized but it's a hackathon so I don't care
    for (r, row) in enumerate(solution):
        for (c, expt) in enumerate(row):
            if expt is not None and expt != dpg.get_item_user_data(items[r][c]):
                return False
    return True


won = False


def check_win():
    global won
    won = is_winning()
    if won:
        # flip colors
        dpg.bind_theme(inverted_theme)


def base_push(sender, app_data, user_data, inner_tag, max_angles):
    if won:
        return

    new_angle = (user_data + 1) % max_angles
    dpg.set_item_user_data(sender, new_angle)
    dpg.apply_transform(
        inner_tag,
        dpg.create_rotation_matrix(math.pi * new_angle / 2.0, [0, 0, 1])
        * dpg.create_translation_matrix([radius, 0]),
    )
    check_win()


# dot has angles: 0 (up), 1 (right), 2 (down), and 3 (left)
def make_dot(tag, init_data=None, color=None):
    if init_data is None:
        init_data = 0
    if color is None:
        color = line_color

    inner_tag = f"_{tag}_inner"
    with dpg.drawlist(width=cw, height=ch, tag=tag, user_data=init_data):
        if debuglines:
            dpg.draw_rectangle((0, 0), (cw, ch), thickness=2, color=[255, 0, 0])

        with dpg.draw_node():
            dpg.apply_transform(
                dpg.last_item(), dpg.create_translation_matrix([cw / 2, ch / 2])
            )
            with dpg.draw_node(tag=inner_tag):
                dpg.apply_transform(
                    dpg.last_item(),
                    dpg.create_rotation_matrix(math.pi * init_data / 2.0, [0, 0, 1])
                    * dpg.create_translation_matrix([radius, 0]),
                )
                dot_radius = cw / 5.0
                dpg.draw_circle((-radius, 0), dot_radius, thickness=3, color=color)
                dpg.draw_line(
                    (-radius, -dot_radius), (-radius, -radius), thickness=5, color=color
                )

    dpg.set_item_callback(tag, lambda s, a, u: base_push(s, a, u, inner_tag, 4))


# turn has angles: 0 (upright), 1 (downright), 2 (downleft), and 3 (upleft)
def make_turn(tag, init_data=None, color=None):
    if init_data is None:
        init_data = 0
    if color is None:
        color = line_color

    inner_tag = f"_{tag}_inner"
    with dpg.drawlist(width=cw, height=ch, tag=tag, user_data=init_data):
        if debuglines:
            dpg.draw_rectangle((0, 0), (cw, ch), thickness=2, color=[255, 0, 0])

        with dpg.draw_node():
            dpg.apply_transform(
                dpg.last_item(), dpg.create_translation_matrix([cw / 2, ch / 2])
            )
            with dpg.draw_node(tag=inner_tag):
                dpg.apply_transform(
                    dpg.last_item(),
                    dpg.create_rotation_matrix(math.pi * init_data / 2.0, [0, 0, 1])
                    * dpg.create_translation_matrix([radius, 0]),
                )
                dpg.draw_line(
                    (-radius, 0), (-radius, -radius), thickness=5, color=color
                )
                dpg.draw_line((-radius, 0), (0, 0), thickness=5, color=color)

    dpg.set_item_callback(tag, lambda s, a, u: base_push(s, a, u, inner_tag, 4))


# straight has angles: 0 (updown), 1 (leftright)
def make_straight(tag, init_data=None, color=None):
    if init_data is None:
        init_data = 0
    if color is None:
        color = line_color

    inner_tag = f"_{tag}_inner"
    with dpg.drawlist(width=cw, height=ch, tag=tag, user_data=init_data):
        if debuglines:
            dpg.draw_rectangle((0, 0), (cw, ch), thickness=2, color=[255, 0, 0])

        with dpg.draw_node():
            dpg.apply_transform(
                dpg.last_item(), dpg.create_translation_matrix([cw / 2, ch / 2])
            )
            with dpg.draw_node(tag=inner_tag):
                dpg.apply_transform(
                    dpg.last_item(),
                    dpg.create_rotation_matrix(math.pi * init_data / 2.0, [0, 0, 1])
                    * dpg.create_translation_matrix([radius, 0]),
                )
                dpg.draw_line(
                    (-radius, radius), (-radius, -radius), thickness=5, color=color
                )

    dpg.set_item_callback(tag, lambda s, a, u: base_push(s, a, u, inner_tag, 2))


# t has angles: 0 (up), 1 (right), 2 (down), and 3 (left)
def make_t(tag, init_data=None, color=None):
    if init_data is None:
        init_data = 0
    if color is None:
        color = line_color

    inner_tag = f"_{tag}_inner"
    with dpg.drawlist(width=cw, height=ch, tag=tag, user_data=init_data):
        if debuglines:
            dpg.draw_rectangle((0, 0), (cw, ch), thickness=2, color=[255, 0, 0])

        with dpg.draw_node():
            dpg.apply_transform(
                dpg.last_item(), dpg.create_translation_matrix([cw / 2, ch / 2])
            )
            with dpg.draw_node(tag=inner_tag):
                dpg.apply_transform(
                    dpg.last_item(),
                    dpg.create_rotation_matrix(math.pi * init_data / 2.0, [0, 0, 1])
                    * dpg.create_translation_matrix([radius, 0]),
                )
                dpg.draw_line(
                    (-radius, 0), (-radius, -radius), thickness=5, color=color
                )
                dpg.draw_line((-2 * radius, 0), (0, 0), thickness=5, color=color)

    dpg.set_item_callback(tag, lambda s, a, u: base_push(s, a, u, inner_tag, 4))


# x has only one angle, 0
def make_x(tag, init_data=None, color=None):
    if init_data is None:
        init_data = 0
    if color is None:
        color = line_color

    inner_tag = f"_{tag}_inner"
    with dpg.drawlist(width=cw, height=ch, tag=tag, user_data=init_data):
        if debuglines:
            dpg.draw_rectangle((0, 0), (cw, ch), thickness=2, color=[255, 0, 0])

        with dpg.draw_node():
            dpg.apply_transform(
                dpg.last_item(), dpg.create_translation_matrix([cw / 2, ch / 2])
            )
            with dpg.draw_node(tag=inner_tag):
                dpg.apply_transform(
                    dpg.last_item(),
                    dpg.create_rotation_matrix(math.pi * init_data / 2.0, [0, 0, 1])
                    * dpg.create_translation_matrix([radius, 0]),
                )
                dpg.draw_line(
                    (-radius, -radius), (-radius, radius), thickness=5, color=color
                )
                dpg.draw_line((-2 * radius, 0), (0, 0), thickness=5, color=color)

    dpg.set_item_callback(tag, lambda s, a, u: base_push(s, a, u, inner_tag, 1))


def make_appropriate_item(item_type, tag, data=None, color=None):
    if item_type == "dot":
        make_dot(tag, data, color)
    elif item_type == "turn":
        make_turn(tag, data, color)
    elif item_type == "straight":
        make_straight(tag, data, color)
    elif item_type == "t":
        make_t(tag, data, color)
    elif item_type == "x":
        make_x(tag, data, color)


with dpg.window(tag="Primary Window"):
    for (r, row) in enumerate(gamegrid):
        row_items = []
        with dpg.group(horizontal=True, horizontal_spacing=0, pos=(20, 20 + (ch * r))):
            for (c, cell) in enumerate(row):
                tag = f"{r}_{c}_{cell}"
                make_appropriate_item(cell, tag)
                row_items.append(tag)

            items.append(row_items)


with dpg.theme() as main_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, bg_color, category=dpg.mvThemeCat_Core
        )


with dpg.theme() as inverted_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg, inverted_bg_color, category=dpg.mvThemeCat_Core
        )

dpg.bind_theme(main_theme)


# dpg.show_item_registry()

dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
