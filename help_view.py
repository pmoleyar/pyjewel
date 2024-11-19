"""
File:           help_view.py
Description:    Help view

Author:         Prabhanjan M. <prabhanjan@gmail.com>
Created:        27 Feb, 2021
Last Modified:  

Copyright:      (C) 2024, Prabhanjan M.
License:        GPL (See LICENSE file for details)

"""

import arcade

from common import Timer

from common import SCREEN_WIDTH, SCREEN_HEIGHT
from common import START_STR, START_X, START_Y
from common import VERSION_STR, VERSION_X, VERSION_Y
from common import key_handler

SYMBOL_FONT = '-adobe-symbol-*-*-*-*-18-*-*-*-*-*-adobe-*'
HEADER_FONT = '-*-*-bold-r-*-*-24-*-*-*-p-*-iso8859-1'
HEADER_CX = SCREEN_WIDTH/2
HEADER_CY = SCREEN_HEIGHT - 100
HELP_LEFT_X = 100
HELP_RIGHT_X = SCREEN_WIDTH - HELP_LEFT_X
HEADER_STR = '\253\253\253 Keys \273\273\273'

HELP_STRS = [
        ['\u2190', ', j, 4', 'Move Block Left'],
        ['\u2191', ', k, 5', 'Rotate Block'],
        ['\u2192', ', l, 6', 'Move Block Right'],
        ['\u2193', ', Space, 0', 'Drop Block'],
        [None, 'P, p', 'Pause/unPause'],
        [None, 'U, u', 'Iconify and Pause']
        ]
NUM_HELP = len(HELP_STRS)

class HelpView(arcade.View):
    """View to show Help"""

    def __init__(self):
        super().__init__()
        self.init_vars()

    def init_vars(self):
        self.timeout = 10.0     # seconds
        self.interval = 0.0     # Time interval in seconds
        self.timer = Timer(self.timeout, self.timer_tick)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.init_vars()
        self.timer.reset()
        self.timer.start()

    def timer_tick(self, delta_time):
        self.timer.stop()
        self.window.show_view(self.window.intro_view)

    def on_update(self, delta_time: float):
        self.timer.update(delta_time)

    def on_draw(self):
        """Draw help view"""
        arcade.start_render()

        arcade.draw_text(HEADER_STR,
                HEADER_CX, HEADER_CY, arcade.color.WHITE, font_size=24,
                anchor_x='center', anchor_y='center')

        y = HEADER_CY
        separation = 60

        for help_item in HELP_STRS:
            arrow, key, ops = help_item
            y -= separation

            # Show help text for operations
            if arrow:
                arcade.draw_text(arrow,
                        HELP_LEFT_X, y, arcade.color.WHITE,
                        font_size=18,# font_name='symbol',
                        anchor_x='left', anchor_y='top')
            arcade.draw_text(key,
                    HELP_LEFT_X+20, y, arcade.color.WHITE, font_size=18,
                    anchor_x='left', anchor_y='top')
            arcade.draw_text(ops,
                    HELP_RIGHT_X, y, arcade.color.WHITE, font_size=18,
                    anchor_x='right', anchor_y='top')

            arcade.draw_text(START_STR,
                    START_X, START_Y, arcade.color.WHITE, font_size=18,
                    anchor_x='center', anchor_y='center')
            arcade.draw_text(VERSION_STR, VERSION_X, VERSION_Y,
                    arcade.color.WHITE,
                    font_size=16, font_name='calibri', bold=True, italic=True,
                    anchor_x='left', anchor_y='top')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """If the user presses the mouse button, start the game. """
        self.window.show_view(self.window.game_view)

    def on_key_press(self, key, modifiers):
        """Handle user keyboard input"""
        key_handler(self, key, modifiers)

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
