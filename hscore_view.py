# ----------------------------------------------------------------------------
# hscore_view.py
#
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
# Last Change: 28 Sep, 2024
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
import os
import getpass
from enum import IntEnum

from common import Timer

from common import SCREEN_WIDTH, SCREEN_HEIGHT
from common import key_handler

MAX_HIGH_SCORES = 10

HSCORE_X_START = 75
HSCORE_X_END = SCREEN_WIDTH - HSCORE_X_START
HSCORE_X_SIZE = HSCORE_X_END - HSCORE_X_START
HSCORE_Y_START = SCREEN_HEIGHT-100
HSCORE_Y_SIZE = 24
HSCORE_Y_SEP = 2*HSCORE_Y_SIZE
HSCORE_AVG_WIDTH = 14
HSCORE_COL1 = HSCORE_X_START + 4*HSCORE_AVG_WIDTH
HSCORE_COL3 = HSCORE_X_END
HSCORE_COL2 = HSCORE_COL3 - 12*HSCORE_AVG_WIDTH

SKULL_W = 30
SKULL_H = 30
SKULL_CX = HSCORE_X_START + SKULL_W // 2
SKULL_CY = HSCORE_Y_START-11*HSCORE_Y_SEP
STEP = 2
NSTEPS = HSCORE_X_SIZE // STEP

class State(IntEnum):
    ERASE = 0
    MOVE_DOWN = 1
    WRITE_NEW = 2
    FINISH = 3

class HscoreView(arcade.View):
    """View to show High scores"""

    def __init__(self):
        super().__init__()

        self.statetc = [NSTEPS, HSCORE_Y_SEP + 10, NSTEPS, 1]
        self.timers = [2, 100, 2, 10000]    # in milliseconds
        self.state = State.FINISH

        self.hscores = []       # list of high scores
        self.hscore_file = 'resources/text/pyjewel.scores'
        self.read_high_scores()

        # Load skull image
        self.skull = arcade.load_texture('resources/images/skule.png', can_cache=True)

        self.init_vars()


    def init_vars(self):
        self.need_insert = False
        self.need_append = False
        self.need_delete = False
        self.insert_pos = MAX_HIGH_SCORES
        self.delete_entry = None

        self.count = 0                          # Number of ticks of timer
        self.timer = Timer(self.timers[self.state.value]/1000, self.timer_tick)

    def set_state(self, state):
        self.state = state
        self.timer.duration = self.timers[self.state]/1000
        self.count = 0

    def change_state(self):
        """Trigger state change"""
        if self.state == State.FINISH:
            # Switch to help view
            self.window.show_view(self.window.help_view)
        elif self.state == State.ERASE and \
                self.insert_pos == MAX_HIGH_SCORES - 1:
            # Nothing to move down in this case
            self.set_state(State.WRITE_NEW)
        else:
            self.set_state(State(self.state + 1))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.init_vars()
        self.timer.reset()

    def timer_tick(self, delta_time):
        """Manage the hscore state machine"""
        self.count += 1

        if self.count > self.statetc[int(self.state)]:
            self.change_state()

    def on_update(self, delta_time: float):
        self.timer.update(delta_time)

    #
    # FILE OPERATIONS
    #
    def read_high_scores(self):
        """Read high scores from file"""
        if not os.path.isfile(self.hscore_file):
            # Create a high score file if needed
            self.write_high_scores()

        try:
            with open(self.hscore_file, 'r') as f:
                for line in f:
                    self.hscores.append(line.strip().split(' '))
                self.hscores = self.hscores[:MAX_HIGH_SCORES]
        except IOError:
            # Couldn't open high score file
            pass

    def write_high_scores(self):
        """Write high scores to file"""
        with open(self.hscore_file, 'w') as f:
            for entry in self.hscores:
                f.write(f'{" ".join(entry)}\n')

    def print_high_scores(self):
        print('High score table:')
        for i, entry in enumerate(self.hscores):
            print(f'{str(i+1)}: {" ".join(entry)}')

    #
    # HIGH SCORE UPDATION
    #
    def update_high_scores(self, stage, score):
        # Read high score file
        self.read_high_scores()

        # Do we need to insert a new high score? If so, Where?
        self.insert_entry = [getpass.getuser(), str(stage), str(score)]

        self.need_insert = False
        self.need_append = False
        self.need_delete = False
        self.insert_pos = len(self.hscores)

        for i, entry in enumerate(self.hscores):
            if score >= int(entry[2]):
                self.need_insert = True
                self.insert_pos = i
                break
        
        self.need_append = not self.need_insert and \
                len(self.hscores) < MAX_HIGH_SCORES

        # Insert or append new high-score entry
        if self.need_insert:
            self.hscores.insert(self.insert_pos, self.insert_entry)
        elif self.need_append:
            self.hscores.append(self.insert_entry)

        # Do we need to delete the 10th high score?
        if len(self.hscores) > MAX_HIGH_SCORES:
            self.need_delete = True
            self.delete_entry = self.hscores.pop()

        # Write to file
        self.write_high_scores()

        # Start animation sequence
        if self.need_delete:
            self.set_state(State.ERASE)
        elif self.need_insert:
            self.set_state(State.MOVE_DOWN)
        elif self.need_append:
            self.set_state(State.WRITE_NEW)
        else:
            self.set_state(State.FINISH)

    #
    # DRAW ROUTINES
    #
    def draw_score(self, i, sl, entry, y_offset=0):
        arcade.draw_text(str(sl)+'- ',
                HSCORE_COL1, HSCORE_Y_START-(i+2)*HSCORE_Y_SEP + y_offset,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='right', anchor_y='center')
        arcade.draw_text(entry[0],
                HSCORE_COL1, HSCORE_Y_START-(i+2)*HSCORE_Y_SEP + y_offset,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='left', anchor_y='center')
        arcade.draw_text(entry[1],
                HSCORE_COL2, HSCORE_Y_START-(i+2)*HSCORE_Y_SEP + y_offset,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='center', anchor_y='center')
        arcade.draw_text(entry[2],
                HSCORE_COL3, HSCORE_Y_START-(i+2)*HSCORE_Y_SEP + y_offset,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='right', anchor_y='center')

    def on_draw(self):
        """Draw high scores"""
        arcade.start_render()

        # Draw title
        arcade.draw_text('HIGH SCORES',
                SCREEN_WIDTH/2, HSCORE_Y_START, arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='center', anchor_y='center')
        arcade.draw_text('Name',
                HSCORE_COL1, HSCORE_Y_START - HSCORE_Y_SEP,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='left', anchor_y='center')
        arcade.draw_text('Stage',
                HSCORE_COL2, HSCORE_Y_START - HSCORE_Y_SEP,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='center', anchor_y='center')
        arcade.draw_text('Score',
                HSCORE_COL3, HSCORE_Y_START - HSCORE_Y_SEP,
                arcade.color.WHITE,
                font_name='fixed', font_size=18,
                anchor_x='right', anchor_y='center')

        # Draw high scores
        # State transition: ERASE -> MOVE_DOWN -> WRITE_NEW -> FINISH
        # One special case handled in change_state() above
        # State transition: ERASE -> WRITE_NEW -> FINISH

        # ..Upto insert_pos
        for i, entry in enumerate(self.hscores[:self.insert_pos]):
            self.draw_score(i, i+1, entry)

        # ..Move down old score entries after insert_pos
        if self.state == State.ERASE:
            offset = 0
            sl_inc = 1
        elif self.state == State.MOVE_DOWN:
            offset = -min(self.count, HSCORE_Y_SEP)
            sl_inc = 1
        else:
            offset = -HSCORE_Y_SEP
            sl_inc = 2

        if self.state != State.FINISH: # ERASE, MOVE_DOWN, WRITE_NEW
            for i, entry in enumerate(self.hscores[self.insert_pos+1:]):
                self.draw_score(i+self.insert_pos, i+self.insert_pos+sl_inc, entry, offset)

        if self.state == State.ERASE:
            self.draw_score(9, 10, self.delete_entry, offset)

            # Animate skull erasing old entry at position 10
            mwidth = self.count*STEP
            arcade.draw_rectangle_filled(SKULL_CX + mwidth // 2, SKULL_CY,
                    mwidth, SKULL_H, arcade.color.BLACK)
            arcade.draw_texture_rectangle(SKULL_CX + mwidth, SKULL_CY,
                    SKULL_W, SKULL_H, self.skull)

        if self.state == State.WRITE_NEW:
            mwidth = HSCORE_X_SIZE - self.count*STEP
            self.draw_score(self.insert_pos, self.insert_pos+1, self.insert_entry)
            arcade.draw_rectangle_filled(
                    HSCORE_X_END - mwidth // 2,
                    HSCORE_Y_START - (self.insert_pos+2)*HSCORE_Y_SEP,
                    mwidth, 1.5*HSCORE_Y_SIZE, arcade.color.BLACK)

        if self.state == State.FINISH:
            # Animation sequence completed, just show all the scores
            for i, entry in enumerate(self.hscores):
                self.draw_score(i, i+1, entry)

    #
    # HANDLE USER INPUT
    #
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """If the user presses the mouse button, start the game. """
        self.window.show_view(self.window.game_view)

    def on_key_press(self, key, modifiers):
        """Handle user keyboard input"""
        key_handler(self, key, modifiers)

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
