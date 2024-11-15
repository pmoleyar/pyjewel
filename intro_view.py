# coding=latin-1
# ----------------------------------------------------------------------------
# pyjewel - dropping jewels game
# Version 1.0
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
# Last update: 26 Sep, 2024
#
# Ported from xjewel Version 1.6 (1/29/93) by David Cooper and José Guterman
# Bitmaps taken from xjewel
# Originally written by Yoshihiro Satoh of HP.
#
# ORIGINAL NOTATIONS
# ==================
# > >Authors
# > >-------
# > >
# > >   Programming       Yoshihiro Satoh
# > >   Font Design       Yoshiharu Minami
# > >   Document Writing  Nancy Paisner
# > >
# > >Copyright
# > >---------
# > >
# > >  This software is in the Yoshihiro's Arcade Collections.
# > >  Domain/JewelBox is a trade mark of Yoshihiro Satoh.
# > >
# > >  Copyright @ 1990 by Yoshihiro Satoh
# > >  All rights are reserved by Yoshihiro Satoh.
# 
# > xjewel - Jewel for X11 Copyright 1992 by David Cooper
# 
# ----------------------------------------------------------------------------
# Ported from xjewel Version 1.6 (1/29/93) by David Cooper and José Guterman
# Bitmaps taken from xjewel
# Originally written by Yoshihiro Satoh of HP.
#
#   Copyright (C) 2021  Prabhanjan M.
#   Copyright is only on the code in this file.
#   No claim is made to the bitmaps.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# ----------------------------------------------------------------------------

import arcade
from enum import IntEnum

from common import Timer

from common import SCREEN_WIDTH, SCREEN_HEIGHT
from common import MARGIN_X, MARGIN_Y, BOARD_X, BOARD_Y
from common import PIECE_SIZE, LOGO_Y, LOGO_H
from common import START_STR, START_X, START_Y
from common import VERSION_STR, VERSION_X, VERSION_Y
from common import key_handler

PRESENT_STR = 'Presenting...'
PRESENT_X = 100
PRESENT_Y = SCREEN_HEIGHT-100

BIGLOGO_W = 577
BIGLOGO_H = 86
PHASE_CX = SCREEN_WIDTH/2
PHASE_CY = SCREEN_HEIGHT-300-BIGLOGO_H/2
STEP = 2
YELSTEP = 20
SHINESTEP = 10
GWIDTH = BIGLOGO_W/STEP+1

THANK_STR = 'Originally by Yoshihiro Satoh of hp'
THANK_X = SCREEN_WIDTH/2
THANK_Y = SCREEN_HEIGHT-500

NSHINE = 4

class State(IntEnum):
    PRESENT = 0
    LOGO = 1
    BY = 2
    SHINE = 3
    FINISH = 4

class IntroView(arcade.View):
    """View to show instructions"""

    def __init__(self):
        super().__init__()
        self.statetc = [len(PRESENT_STR), GWIDTH/2, 1, 2*NSHINE*GWIDTH, 10]
        self.timertc = [200, 2, 200, 2, 1000]  # in millisecs

        # Load logo image
        self.logo = arcade.load_texture('resources/images/biglogo.png',
                can_cache=True)
        self.init_vars()

    def init_vars(self):
        self.state = State.PRESENT
        self.count = 0                  # number of ticks of timer
        self.interval = 0.0             # time since last timer tick
        self.timer = Timer(self.timertc[self.state.value]/1000, self.timer_tick)

    def set_state(self, state):
        self.state = state
        self.timer.duration = self.timertc[self.state]/1000
        self.count = 0

    def change_state(self):
        """Trigger state change"""
        if self.state == State.FINISH:
            self.window.show_view(self.window.hscore_view)
        else:
            self.set_state(State(self.state + 1))

    def on_show_view(self):
        """This is run once when we switch to this view"""
        arcade.set_background_color(arcade.color.BLACK)
        self.init_vars()
        self.timer.reset()
        self.timer.start()

    def timer_tick(self, delta_time: float):
        """Manage the intro state machine"""
        self.count += 1
        if self.count > self.statetc[int(self.state)]:
            self.change_state()

        if self.state == State.LOGO:
            self.shinex = (SCREEN_WIDTH - BIGLOGO_W) / 2
            self.shinedir = 'forward'

    def on_update(self, delta_time: float):
        self.timer.update(delta_time)

    def on_draw(self):
        """Draw this view"""
        arcade.start_render()

        if self.state == State.PRESENT:
            tlen = self.count
        else: 
            tlen = len(PRESENT_STR)

        if self.state == State.LOGO:
            gwidth = 2 * self.count * STEP
        else:
            gwidth = BIGLOGO_W


        if self.state >= State.PRESENT:
            # Draw progressively more of presentation text
            arcade.draw_text(PRESENT_STR[:tlen],
                    PRESENT_X, PRESENT_Y, arcade.color.YELLOW, font_size=24,
                    anchor_x='left', anchor_y='top')

        if self.state >= State.LOGO:
            # Unhide progressively more of logo

            if self.state == State.LOGO:
                # Render two yellow strips on left and right
                # which move with count
                x1 = SCREEN_WIDTH / 2 - (self.count + 1) * STEP - YELSTEP
                if x1 < (SCREEN_WIDTH - BIGLOGO_W) / 2:
                    x1 = (SCREEN_WIDTH - BIGLOGO_W) / 2
                x2 = SCREEN_WIDTH / 2 + (self.count + 1) * STEP
                if x2 > (SCREEN_WIDTH + BIGLOGO_W) / 2 - YELSTEP:
                    x2 = (SCREEN_WIDTH + BIGLOGO_W) / 2 - YELSTEP

                y = PHASE_CY - BIGLOGO_H / 2
                arcade.draw_xywh_rectangle_filled(x1, y,
                        YELSTEP, BIGLOGO_H, arcade.color.YELLOW)
                arcade.draw_xywh_rectangle_filled(x2, y,
                        YELSTEP, BIGLOGO_H, arcade.color.YELLOW)

            # Render centred green rectangle that grows larger
            # with count
            arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, PHASE_CY,
                    gwidth, BIGLOGO_H, arcade.color.GREEN)

            if self.state == State.SHINE:
                # For the shine effect, render a yellow strip which moves
                # forward and back across the logo
                y = PHASE_CY - BIGLOGO_H / 2
                arcade.draw_xywh_rectangle_filled(self.shinex, y,
                        SHINESTEP, BIGLOGO_H, arcade.color.YELLOW)

                if self.shinedir == 'forward':
                    self.shinex += STEP
                else:
                    self.shinex -= STEP

                if self.shinex > (SCREEN_WIDTH + BIGLOGO_W) / 2 - SHINESTEP:
                    self.shinex = (SCREEN_WIDTH + BIGLOGO_W) / 2 - SHINESTEP
                    self.shinedir = 'backward'
                elif self.shinex < (SCREEN_WIDTH - BIGLOGO_W) / 2:
                    self.shinex = (SCREEN_WIDTH - BIGLOGO_W) / 2
                    self.shinedir = 'forward'

            # Render the logo last - it is transparent
            arcade.draw_texture_rectangle(PHASE_CX, PHASE_CY,
                    BIGLOGO_W, BIGLOGO_H, self.logo)

        if self.state >= State.BY:
            # Show other text
            arcade.draw_text(THANK_STR,
                    THANK_X, THANK_Y, arcade.color.WHITE,
                    font_size=16, font_name='calibri', bold=True, italic=True,
                    anchor_x='center', anchor_y='center')
            arcade.draw_text(START_STR,
                    START_X, START_Y, arcade.color.WHITE,
                    font_size=16, font_name='calibri', bold=True, italic=True,
                    anchor_x='center', anchor_y='center')
            arcade.draw_text(VERSION_STR,
                    VERSION_X, VERSION_Y, arcade.color.WHITE,
                    font_size=16, font_name='calibri', bold=True, italic=True,
                    anchor_x='left', anchor_y='top')

    #
    # HANDLE USER INPUT
    #
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        self.window.show_view(self.window.game_view)

    def on_key_press(self, key, modifiers):
        """Handle user keyboard input"""
        key_handler(self, key, modifiers)

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
