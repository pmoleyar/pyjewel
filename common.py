# coding=latin-1
# ----------------------------------------------------------------------------
# common.py
#
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
# Last update: 28 Sep, 2024
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

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 728
SCREEN_TITLE = 'pyjewel'

BLOCK_SIZE = 3
NUM_PIECES = 6      # 1: red, 2: green, 3: orange, 4: blue, 5: cyan, 6: yellow
WILD_PIECE = 0      # 0: jewel (white)
PIECES_PER_STAGE = 50
AVG_BLOCKS_BETWEEN_JEWELS = 27
NUM_BACKGND = 4
NUM_FLASH = 4

JEWEL_SCORE = 300
DROP_POINTS = 10
INITIAL_LIVES = 3
MAX_STAGE = 25

NCOLS = 6
NROWS = 14

MARGIN_X = 10
MARGIN_Y = 10

BOARD_X = MARGIN_X
BOARD_Y = MARGIN_Y
PIECE_SIZE = 40
BOARD_W = NCOLS+2
BOARD_H = NROWS+1

PREVIEW_W = 3
PREVIEW_H = BLOCK_SIZE+2
PREVIEW_X = BOARD_X + PIECE_SIZE * (BOARD_W + 1)
PREVIEW_Y = BOARD_Y

LOGO_W = 360
LOGO_H = 54
#LOGO_X = BOARD_X + PIECE_SIZE/2
LOGO_Y = BOARD_Y + PIECE_SIZE*BOARD_H + PIECE_SIZE/2
LOGO_CX = BOARD_X + PIECE_SIZE//2 + LOGO_W//2
LOGO_CY = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*BOARD_H+PIECE_SIZE//2 \
        + LOGO_H//2)

SCORE_X = PREVIEW_X
SCORE_Y = SCREEN_HEIGHT - (PREVIEW_Y + PIECE_SIZE * (PREVIEW_H + 1))
SCORE_W = 14
SCORE_RX = SCORE_X + 182
SCORE_CH = 43

START_STR = 'Press \140Space\047 to begin, or \140H\047 for Help'
START_X = SCREEN_WIDTH/2
START_Y = SCREEN_HEIGHT-600

VERSION_STR = 'Version 1.6 (1/29/93) By David Cooper and José Guterman'
VERSION_X = BOARD_X + PIECE_SIZE/2
VERSION_Y = SCREEN_HEIGHT - (LOGO_Y + LOGO_H)

FLASH_TIMER = 35
FLASH_JFRAMES = 3
FLASH_TFRAMES = 3
FLASH_DELAY = 4*FLASH_TIMER*(FLASH_JFRAMES + NUM_FLASH + FLASH_TFRAMES)/1000

class Timer:
    def __init__(self, duration, callback):
        self._duration = duration   # Duration is in seconds
        self.elapsed_time = 0
        self._debug = False
        self.active = False
        self.callback = callback

    def debug(self):
        self._debug = True

    def update(self, delta_time):
        if not self.active: return

        self.elapsed_time += delta_time
        if self.elapsed_time >= self._duration:
            self.elapsed_time -= self._duration
            self.callback(delta_time)

    def reset(self):
        self.elapsed_time = 0

    def stop(self):
        if self._debug: print('Timer stopped')
        self.active = False

    def start(self):
        if self._debug: print('Timer started')
        self.active = True

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, new_duration):
        """Update timer duration"""
        self._duration = new_duration
        self.elapsed_time = 0


def key_handler(cview, key, modifiers):
    """Handle user keyboard input
    Q, X: Quit the game
    Space, S: Start the game
    H: Show help
    P: Show high scores

    Arguments:
            key {int} == which key was pressed
            modifiers {int} -- which modifers were pressed
    """
    if key == arcade.key.SPACE or key == arcade.key.S:
        cview.window.show_view(cview.window.game_view)
    elif key == arcade.key.H:
        # Show Help
        # Note: No need to switch if already on help screen 
        #if cview.window.current_view != cview.window.help_view:
        cview.window.show_view(cview.window.help_view)
    elif key == arcade.key.P:
        # Show High scores
        cview.window.show_view(cview.window.hscore_view)
    elif key == arcade.key.Q or key == arcade.key.X:
        # Quit
        arcade.close_window()

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
