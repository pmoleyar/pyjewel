# coding=latin-1
# ----------------------------------------------------------------------------
# pyjewel - dropping jewels game
# Version 1.0
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
# Last update: 23 Sep, 2024
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

import sys
import random
import arcade

from common import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

from intro_view import IntroView
from help_view import HelpView
from game_view import GameView
from hscore_view import HscoreView

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def main():
    """ Main method """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Create all the views needed
    window.intro_view = IntroView()
    window.help_view = HelpView()
    window.hscore_view = HscoreView()
    window.game_view = GameView()

    # Switch to the intro view
    window.show_view(window.intro_view)
    arcade.run()


if __name__ == "__main__":
    main()

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
