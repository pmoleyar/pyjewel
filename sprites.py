# ----------------------------------------------------------------------------
# pyjewel - dropping jewels game
# Version 1.0
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
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
from random import randrange

from common import SCREEN_HEIGHT
from common import BOARD_X, BOARD_Y
from common import PREVIEW_X, PREVIEW_Y
from common import NCOLS, PIECE_SIZE
from common import BLOCK_SIZE, NUM_PIECES, WILD_PIECE
from common import AVG_BLOCKS_BETWEEN_JEWELS
from common import NUM_BACKGND, NUM_FLASH
from common import FLASH_JFRAMES, FLASH_TFRAMES

class BackgroundSprite(arcade.Sprite):
    """Sprite for a background tile with multiple textures
    
    base_filename   Name of a series of files containing the textures
            This is a string with a single '%d' in it. The %d is replaced
            by a series of numbers, one for each texture, from 'start' to 'end'
    start   number of the first texture file
    end     number of the last texture file
    """
    def __init__(self, base_filename, start, end, *args, **kwargs):
        self.bg_index = 1
        super().__init__(filename=None, *args, **kwargs)
        
        # Replace '%d' in filename with number
        index = base_filename.find('%d')
        filename = base_filename

        for n in range(start, end + 1):
            if index != -1:
                filename = base_filename[:index] + str(n) + \
                        base_filename[index+2:]
            self.textures.append(arcade.load_texture(filename))
        self.set_texture(self.bg_index)

    def update(self):
        self.bg_index = (self.bg_index + 1) % NUM_BACKGND
        self.set_texture(self.bg_index)

class Jewel(arcade.Sprite):
    """Sprite for a single jewel"""
    def __init__(self, jtexture, ftextures, piece, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piece = piece
        self.row, self.col = row, col

        # Jewel texture
        self.textures.append(jtexture)
        # Textures for flash animation
        for ftexture in ftextures:
            self.textures.append(ftexture)
        self.set_texture(0)
        self.aindex = 0
        self.animation = 'flash'

        # Flash Animation Frames:
        #   0: jewel
        #   1..NUM_FLASH: flash1,2,3,4,
        #   NUM_FLASH+1: transparent
        self.aframes = [0]*FLASH_JFRAMES                # jewel image
        self.aframes += list(range(1, NUM_FLASH+1))     # flash images
        self.aframes += [NUM_FLASH+1]*FLASH_TFRAMES     # transparent image
        self.alen = len(self.aframes)

        # Shrink animation params
        self.angle = 0.0
        self.scale = 1.0
        self.alpha = 255

        # Coords
        if col == NCOLS:
            self.left = PREVIEW_X + PIECE_SIZE
            self.top = SCREEN_HEIGHT - (PREVIEW_Y + PIECE_SIZE*(row+1))
        else:
            self.left = BOARD_X + PIECE_SIZE*(col+1)
            self.top = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*row)

    def update_animation(self, delta_time: float):
        """Animate"""
        if self.animation == 'flash':
            # 'Flash' Animation - cycle through animation frames
            self.aindex = (self.aindex + 1) % self.alen
            self.set_texture(self.aframes[self.aindex])
        elif self.animation == 'shrink':
            # Shrink Animation
            self.angle += 2.0
            self.scale *= 0.95
            self.alpha *= 0.95

class JewelBlock(arcade.SpriteList):
    """SpriteList for a jewel block"""
    def __init__(self, jtextures=None, ftextures=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a random set of jewels for this block
        if not randrange(AVG_BLOCKS_BETWEEN_JEWELS):
            self.iswild = True
            self.pieces = [WILD_PIECE] * BLOCK_SIZE
        else:
            self.iswild = False
            self.pieces = [randrange(NUM_PIECES)+1 for i in range(BLOCK_SIZE)]
        
        # Starting board coords of piece (of top jewel, specifically)
        self.row, self.col = 0, NCOLS // 2
        self.ismoving = False

        for i, j in enumerate(self.pieces):
            self.append(Jewel(jtextures[j], ftextures, j, i, NCOLS))

    def move_to_board(self):
        """Move block from preview to playing board"""
        for s in self.sprite_list:
            s.col = NCOLS // 2
        self.move(BOARD_X-PREVIEW_X + self.col*PIECE_SIZE,
                PREVIEW_Y-BOARD_Y + PIECE_SIZE)
        self.ismoving = True

    def rotate(self):
        """Rotate down the jewels in the block"""
        # Move sprites in geometry
        self.sprite_list[-1].center_y += 3*PIECE_SIZE
        self.move(0, -PIECE_SIZE)

        # Update sprite col,row
        self.sprite_list[-1].row -= 3
        for s in self.sprite_list:
            s.row += 1

        # Reorder sprites in the list
        self.insert(0, self.pop())

        # Reorder data
        self.pieces.insert(0, self.pieces.pop())

    def move_left(self):
        """Move block left one unit"""
        self.move(-PIECE_SIZE, 0)
        self.col -= 1
        for s in self.sprite_list:
            s.col -= 1

    def move_right(self):
        """Move block right one unit"""
        self.move(PIECE_SIZE, 0)
        self.col += 1
        for s in self.sprite_list:
            s.col += 1

    def move_down(self):
        """Move block down one unit"""
        self.move(0, -PIECE_SIZE)
        self.row += 1
        for s in self.sprite_list:
            s.row += 1

class JewelList(arcade.SpriteList):
    def print(self):
        print('JewelList.print:', end=' ')
        for s in self.sprite_list:
            print('({},{})'.format(s.row, s.col), end=' ')
        print('')

    def find(self, row, col):
        for s in self.sprite_list:
            if s.row == row and s.col == col:
                return s
        print ('ERROR: Couldn\'t find ({},{})'.format(row,col))
        self.print()
        return None


# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
