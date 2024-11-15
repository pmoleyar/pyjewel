# ----------------------------------------------------------------------------
# pyjewel - dropping jewels game
# Version 1.0
# Prabhanjan M. <prabhanjan@gmail.com>
#
# Date: 27 Feb, 2021
# Last Change: 26 Sep, 2024
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
from random import randrange, choice
from itertools import groupby
from functools import partial

from common import Timer

from common import SCREEN_WIDTH, SCREEN_HEIGHT
from common import BOARD_W, BOARD_H, BOARD_X, BOARD_Y
from common import PREVIEW_W, PREVIEW_H, PREVIEW_X, PREVIEW_Y
from common import SCORE_X, SCORE_Y, SCORE_W, SCORE_RX, SCORE_CH
from common import LOGO_W, LOGO_H, LOGO_CX, LOGO_CY
from common import NCOLS, NROWS, PIECE_SIZE
from common import VERSION_STR, VERSION_X, VERSION_Y
from common import BLOCK_SIZE, NUM_PIECES, WILD_PIECE
from common import PIECES_PER_STAGE, AVG_BLOCKS_BETWEEN_JEWELS
from common import NUM_BACKGND, NUM_FLASH
from common import FLASH_TIMER, FLASH_DELAY
from common import JEWEL_SCORE, DROP_POINTS, INITIAL_LIVES, MAX_STAGE

from sprites import BackgroundSprite, Jewel, JewelBlock, JewelList


class GameView(arcade.View):
    """View for the actual game"""

    def __init__(self):
        super().__init__()
        self.speeds = [ 1.500, 1.250, 1.000, 0.750, 0.500, 0.250, 0.2375,
                0.2250, 0.2125, 0.2000, 0.1875, 0.1750, 0.1625, 0.1500,
                0.1375, 0.1250, 0.1125, 0.1000, 0.0875, 0.0750, 0.0625,
                0.0500, 0.0375, 0.0250, 0.0125, 0.0000, 0.0000]
        #self.speed is the game tick (seconds)

        # Create timers - one for special effects, one for the game progress
        self.fx_timer = Timer(FLASH_TIMER/1000, self.advance_fx)
        self.game_timer = Timer(self.speeds[0], self.advance_game)

        self.new_game()

    #
    # GAME SETUP
    #
    def setup(self):
        # Load textures
        self.logo = arcade.load_texture('resources/images/jewellogo.png',
                can_cache=True)
        self.logo2 = arcade.load_texture('resources/images/jewellogo2.png',
                can_cache=True)
        self.jtextures = [arcade.load_texture('resources/images/jewel.png',
                can_cache=True)]
        for i in range(1, NUM_PIECES + 1):
            self.jtextures.append(arcade.load_texture(
                    'resources/images/piece' + str(i) + '.png', can_cache=True))
        self.ftextures = []
        for i in range(1, NUM_FLASH + 1):
            self.ftextures.append(arcade.load_texture(
                    'resources/images/flash' + str(i) + '.png', can_cache=True))
        self.ftextures.append(arcade.load_texture('resources/images/trans.png',
                can_cache=True))

        # Load sounds
        self.move_down_sound = arcade.load_sound(':resources:/sounds/jump4.wav')
        self.drop_sound = arcade.load_sound(':resources:/sounds/jump2.wav')
        self.hit_sound = arcade.load_sound(':resources:/sounds/hit4.wav')
        self.flash_sound = arcade.load_sound(':resources:/sounds/rockHit2.ogg')
        self.lose_sound = arcade.load_sound(':resources:/sounds/lose1.wav')

        # Board border
        self.border = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        for i in range(BOARD_H):
            b = arcade.Sprite('resources/images/border.png')
            b.left = BOARD_X
            b.top = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*i)
            self.border.append(b)

            b = arcade.Sprite('resources/images/border.png')
            b.left = BOARD_X + PIECE_SIZE*(BOARD_W-1)
            b.top = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*i)
            self.border.append(b)

        for i in range(BOARD_W):
            b = arcade.Sprite('resources/images/border.png')
            b.left = BOARD_X + PIECE_SIZE*i
            b.top = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*(BOARD_H-1))
            self.border.append(b)

        # Preview border
        for i in range(PREVIEW_W):
            for j in range(PREVIEW_H):
                if i == 1 and j != 0 and j != PREVIEW_H - 1: continue
                #and (j != 0 or j != PREVIEW_H -1): continue
                b = arcade.Sprite('resources/images/border.png')
                b.left = PREVIEW_X + PIECE_SIZE*i
                b.top = SCREEN_HEIGHT - (PREVIEW_Y + PIECE_SIZE*j)
                self.border.append(b)

        # Board background
        self.background = arcade.SpriteList(is_static=False)
        for i in range(NCOLS):
            for j in range(NROWS):
                b = BackgroundSprite('resources/images/back%d.png',
                        1, NUM_BACKGND)
                b.left = BOARD_X + PIECE_SIZE*(i+1)
                b.top = SCREEN_HEIGHT - (BOARD_Y + PIECE_SIZE*j)
                self.background.append(b)

        # Preview block of jewels
        self.preview_block = JewelBlock(self.jtextures, self.ftextures)

        # Falling block of jewels
        self.falling_block = self.preview_block

        # Fallen jewels
        self.fallen_jewels = JewelList(use_spatial_hash=True)

        # Jewels that need to flash
        self.flashing_jewels = JewelList(use_spatial_hash=True)

    #
    # GAME LOGIC
    #
    def new_board(self):
        # Create the main board of 0's
        board = [[0 for i in range(NCOLS)] for j in range(NROWS)]
        return board

    def new_game(self):
        self.setup()
        self.points = 0
        self.showpoints = False
        self.mult = 1
        self.showmult = False
        self.score = 0
        self.score_incr = 0
        self.iteration = 0
        self.lives = INITIAL_LIVES
        self.stage = 1
        self.speed = self.speeds[self.stage]
        self.rest = PIECES_PER_STAGE
        self.paused = False
        self.sound = False
        self.game_over = False
        self.fx_fill = False
        self.board = self.new_board()

        # Reset and stop fx timer
        self.fx_timer.reset()
        self.fx_timer.stop()

        # Reset and start game timer
        self.game_timer.duration = self.speed
        self.game_timer.start()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.fx_timer.stop()
            self.game_timer.stop()
        else:
            self.fx_timer.start()
            self.game_timer.start()

    def incr_stage(self):
        self.stage = 1 + (self.stage % MAX_STAGE)
        self.background.update()
        self.speed = self.speeds[self.stage]

        # Update timer with new speed
        self.game_timer.duration = self.speed

    def decr_rest(self, val):
        self.rest -= val
        if self.rest <= 0:
            self.rest += PIECES_PER_STAGE
            self.incr_stage()

    def decr_lives(self):
        #if self.sound:
        #    arcade.play_sound(self.lose_sound)
        self.lives -= 1
        if not self.lives: 
            self.game_over = True
            self.game_timer.stop()
            # This call isn't needed. process_blocks() will call end_game()
            #arcade.schedule(self.end_game, 2*FLASH_DELAY)

    def end_game(self, delta_time: float):
        """End game"""
        arcade.unschedule(self.end_game)

        #  Switch to highscore view, and update high scores
        self.window.show_view(self.window.hscore_view)
        self.window.hscore_view.update_high_scores(self.stage, self.score)

    def exit_game(self):
        self.game_over = True
        self.game_timer.stop()

        self.fx_fill = True
        self.fx_timer.start()

        self.falling_block = self.preview_block
        arcade.schedule(self.end_game, 3*FLASH_DELAY) # enough delay for fx

    def on_show(self):
        """This is run once when we switch to this view"""
        self.new_game()

    def rotate(self):
        if not self.falling_block.ismoving: return
        self.falling_block.rotate()

    def move_left(self):
        if not self.falling_block.ismoving: return
        fc, fr = self.falling_block[-1].col, self.falling_block[-1].row
        if fc > 0 and self.board[fr][fc-1] == 0:
            self.falling_block.move_left()

    def move_right(self):
        if not self.falling_block.ismoving: return
        fc, fr = self.falling_block[-1].col, self.falling_block[-1].row
        if fc < NCOLS-1 and self.board[fr][fc+1] == 0:
            self.falling_block.move_right()

    def drop(self):
        if not self.falling_block.ismoving: return
        #if self.sound:
        #    arcade.play_sound(self.drop_sound)

        cycles = -1
        while self.falling_block.ismoving:
            cycles += 1
            self.move_down(quiet=True)

        if cycles > 0:
            self.score += DROP_POINTS*cycles

    def move_down(self, quiet=False):
        # Have we hit bottom, or one of the fallen jewels
        fc, fr = self.falling_block[-1].col, self.falling_block[-1].row
        if (self.falling_block.row + BLOCK_SIZE == NROWS) or \
                self.board[fr+1][fc] != 0:
            #if self.sound and not quiet:
            #    arcade.play_sound(self.hit_sound)
            self.falling_block.ismoving = False # Disable response to keys

            # Enable effects, pause game
            self.game_timer.stop()
            self.fx_timer.start()

            # Add to fallen blocks
            self.fallen_jewels.extend(self.falling_block)
            if self.falling_block.iswild:
                # Process the block hit by the wildpiece
                self.process_wildpiece_drop(self.falling_block)
            else:
                # Update board
                self.add_to_board(self.falling_block)
                # Process the fallen block
                self.process_blocks()
        else:
            self.falling_block.move_down()

    # Call chart:
    # move_down ->
    # | -> if iswild: process_wildpiece_drop
    # |               |-> [schedule] delete_jewels
    # |                              |-> process_blocks
    # |                                  |-> [schedule] delete_jewels (...)
    # | -> else: process_blocks
    # |          |-> [schedule] delete_jewels
    # |                         |-> process_blocks
    # |                             |-> [schedule] delete_jewels (...)

    def add_to_board(self, block):
        c, r = block.col, block.row
        for i in range(BLOCK_SIZE):
            self.board[r+i][c] = block.pieces[i]

    def print_board(self):
        self.fallen_jewels.print()
        for i in range(NROWS):
            print(' '.join([str(self.board[i][j]) for j in range(NCOLS)]))
        print('-'.join(['-' for j in range(NCOLS)]))

    def fill_effect(self):
        empty_cells = [(r, c) for r in range(NROWS) for c in range(NCOLS) \
                if not self.board[r][c]]

        # Fill an empty cell with a random jewel
        if len(empty_cells):
            r, c = choice(empty_cells)
            j = randrange(NUM_PIECES)+1
            self.fallen_jewels.append(
                    Jewel(self.jtextures[j], self.ftextures, j, r, c))
            self.board[r][c] = j
        else:
            # If done adding random jewels, 
            # disable fill effect, (enable animation - shrink)
            self.fx_fill = False
            for s in self.fallen_jewels.sprite_list:
                s.animation = 'shrink'
            self.board = self.new_board()
            self.flashing_jewels.extend(self.fallen_jewels)
            self.decr_lives()
            self.scheduled_function = partial(self.delete_jewels, False)
            arcade.schedule(self.scheduled_function, FLASH_DELAY)

    def process_wildpiece_drop(self, block):
        self.flashing_jewels.extend(block)

        c, r = block.col, block.row
        if r + 3 < NROWS:
            # Didn't hit bottom, so must have hit a fallen jewel. What color?
            match_piece = self.board[r+3][c]
            indices = [(i, j) for i in range(NROWS) \
                    for j in range(NCOLS) if self.board[i][j] == match_piece]
            match_jewels = [self.fallen_jewels.find(i[0], i[1]) \
                    for i in indices]
            self.flashing_jewels.extend(match_jewels)

        self.calc_points(JEWEL_SCORE, 1)

        # Give jewels time to flash, and schedule deletion/further processing
        self.scheduled_function = partial(self.delete_jewels, True)
        arcade.schedule(self.scheduled_function, FLASH_DELAY)

    def drop_down_blocks(self):
        """Move fallen jewels down after flashing jewels are removed"""
        for r in range(NROWS-2, -1, -1):
            for c in range(NCOLS):
                if self.board[r][c]:
                    s = self.fallen_jewels.find(r, c)
                    assert s is not None
                    for nr in range(r+1, NROWS):
                        if not self.board[nr][c]:
                            s.center_y += -PIECE_SIZE
                            s.row += 1
                            self.board[nr][c] = self.board[nr-1][c]
                            self.board[nr-1][c] = 0

    def verify_match_pieces(self, indices):
        if not len(indices): return
        print('verify_match_pieces {}'.format(indices))
        i0 = indices[0]
        first_piece = self.board[i0[0]][i0[1]]
        error = 0
        for i in indices[1:]:
            if self.board[i[0]][i[1]] != first_piece:
                error = 1
                break

        if error:
            self.print_board()
            print('ERROR: Found match pieces to be', end=' ')
            for i in indices:
                print(self.board[i[0]][i[1]], end=' ')
            raise ValueError('verify error')

    def calc_points(self, points, mult):
        self.points = points * (1 << (mult-1))
        self.mult = mult
        self.showpoints = True
        self.showmult = True

    def add_score(self):
        self.score += self.points
        self.showpoints = False
        self.showmult = False
        self.points = 0

    def process_blocks(self):
        """Check the board for adjacent matching jewels."""
        # https://stackoverflow.com/questions/44790869/
        # find-indexes-of-repeated-elements-in-an-array-python-numpy
        # /44792205#44792205
        def find_consecutive_ranges(lst, n=3):
            # Elements of the input list are of the form (v, k)
            # Return a list of list of k's of >=n runs of the same 'v'

            # Identify consecutive groups of same value (value != 0)
            groups = [list(g) for k, g in groupby(lst, lambda x: x[0]) if k]
            # Pick only groups of length >= 3
            len3reps = [g for g in groups if len(g) >= n]
            # Extract list of list of k's
            return [[x[1] for x in len3rep] for len3rep in len3reps]

        def points(n):
            return 300 + (n-3)*150

        add_score = 0
        self.iteration += 1
        indices = set()     # Needs to be set to avoid duplicates

        # Check consecutive matching blocks horizontally
        for r in range(NROWS):
            # For this row, create ordered list of (value, cell)
            L = [(self.board[r][c], (r, c)) for c in range(NCOLS)]
            for cell_range in find_consecutive_ranges(L):
                add_score += points(len(cell_range))
                indices.update(cell_range)

        # Check consecutive matching blocks vertically
        for c in range(NCOLS):
            # For this row, create ordered list of (value, cell)
            L = [(self.board[r][c], (r, c)) for r in range(NROWS)]
            for cell_range in find_consecutive_ranges(L):
                add_score += points(len(cell_range))
                indices.update(cell_range)

        # Check consecutive matching blocks diagonally right
        # https://www.geeksforgeeks.org/zigzag-or-diagonal-traversal-of-matrix/
        for line in range(3, NROWS+NCOLS-2):
            # Get column index of first element in this line
            # index is 0 for line 0, and (line - ROW) for a given line
            start_col = max(0, line - NROWS)
            count = min(line, (NCOLS - start_col), NROWS)
            L = [(self.board[min(NROWS, line) - j - 1][start_col+j], 
                    (min(NROWS, line) - j - 1, start_col+j)) \
                    for j in range(count)]
            for cell_range in find_consecutive_ranges(L):
                add_score += points(len(cell_range))
                indices.update(cell_range)

        # Check consecutive matching blocks diagonally left
        for line in range(3, NROWS+NCOLS-2):
            # Get column index of first element in this line
            # index is 0 for line 0, and (line - ROW) for a given line
            start_col = max(0, line - NROWS)
            count = min(line, (NCOLS - start_col), NROWS)
            L = [(self.board[min(NROWS, line) - j - 1][NCOLS-start_col-j-1], 
                    (min(NROWS, line) - j - 1, NCOLS-start_col-j-1)) \
                    for j in range(count)]
            for cell_range in find_consecutive_ranges(L):
                add_score += points(len(cell_range))
                indices.update(cell_range)

        match_jewels = [self.fallen_jewels.find(i[0], i[1]) \
                for i in indices]
        assert not self.flashing_jewels  # Must be empty at this point
        self.flashing_jewels.extend(match_jewels)

        # Schedule deletion
        # (with a further mutual recursive call into this function)
        # only if there's something to delete
        if len(self.flashing_jewels):
            #if self.sound:
            #    arcade.play_sound(self.lose_sound)
            # Post the score increase for when the jewels are removed
            self.calc_points(add_score, self.iteration)

            self.scheduled_function = partial(self.delete_jewels, True)
            arcade.schedule(self.scheduled_function, FLASH_DELAY)
        else:
            # Done processing dropped block, game logic can resume
            self.iteration = 0
            # Disable effects, resume game logic
            self.fx_timer.stop()
            if self.game_over:
                self.end_game(0)
            else:
                self.game_timer.start()

    def delete_jewels(self, scoring, delta_time: float):
        # Unschedule future recurrences of this scheduled call
        arcade.unschedule(self.scheduled_function)

        # Remove jewels (note: can't iterate over sprite_list directly)
        jewels_to_delete = [s for s in self.flashing_jewels.sprite_list]
        
        if scoring:
            # Update score and rest
            self.add_score()
            self.decr_rest(len(jewels_to_delete))

        for s in jewels_to_delete:
            self.board[s.row][s.col] = 0
            s.kill()

        self.drop_down_blocks()
        # Continue processing fallen blocks
        self.process_blocks()

    def advance_fx(self, delta_time):
        """
        Initiate special effects.
        There are two kinds of special-effects:
        - "fill effect": fill the game board with random blocks
        - "flash/shrink effect": animate the blocks by shrinking them

        :param float delta_time: Unused
        """
        if self.fx_fill:
            # Fill effect
            self.fill_effect()
        else:
            # Animation effect (flash/shrink)
            self.flashing_jewels.update_animation(delta_time)

    def advance_game(self, _delta_time):
        """
        Advance the game one step.

        :param float delta_time: Unused
        """
        if self.falling_block.ismoving:
            # If a block is already on the board,  move it down
            self.move_down()
        elif self.board[BLOCK_SIZE-1][NCOLS//2]:
            # Can a new block be introduced?
            # ..No: trigger fill effect
            self.fx_fill = True
            self.game_timer.stop()
            self.fx_timer.start()
        else:
            # ..Yes: move preview block to board as a falling block
            self.falling_block = self.preview_block
            self.falling_block.move_to_board()
            #if self.sound:
            #    arcade.play_sound(self.move_down_sound)

            # New preview block
            self.preview_block = JewelBlock(self.jtextures, self.ftextures)

    def on_update(self, delta_time: float):
        self.fx_timer.update(delta_time)
        self.game_timer.update(delta_time)

    #
    # DRAW ROUTINES
    #
    def draw_scoreboard(self):
        # Score and other status items
        flags = [self.showpoints, self.showmult, True, True, True, True,
                True, True, self.paused or self.game_over]
        labels = ['POINTS', 'X', 'SCORE', 'LIVES', 'SPEED', 'STAGE',
                'REST', 'SOUND', '']
        values = [self.points, self.mult, self.score, self.lives,
                '{:.4f}'.format(self.speed), self.stage,
                self.rest, 'ON' if self.sound else 'OFF',
                'PAUSED' if self.paused else 'GAME OVER']

        for i, item in enumerate(zip(flags, labels, values)):
            flag, label, value = item
            if flag:
                arcade.draw_text(label, SCORE_X, SCORE_Y - SCORE_CH*i,
                        color=arcade.color.WHITE,
                        font_name='fixed', font_size=18, bold=True,
                        anchor_x='left')
                arcade.draw_text(str(value), SCORE_RX, SCORE_Y - SCORE_CH*i,
                        color=arcade.color.WHITE,
                        font_name='fixed', font_size=18, bold=True,
                        anchor_x='right')

        # Logo
        arcade.draw_texture_rectangle(LOGO_CX, LOGO_CY,
                LOGO_W, LOGO_H, self.logo)
        arcade.draw_texture_rectangle(LOGO_CX, LOGO_CY,
                LOGO_W, LOGO_H, self.logo2)
        # Help string
        arcade.draw_text(VERSION_STR, VERSION_X, VERSION_Y, arcade.color.WHITE,
                font_size=16, font_name='calibri', bold=True, italic=True,
                anchor_x='left', anchor_y='top')

    def on_draw(self):
        """Draw this view"""
        arcade.start_render()
        self.border.draw()
        self.background.draw()
        self.draw_scoreboard()
        self.preview_block.draw()
        self.falling_block.draw()
        self.fallen_jewels.draw()
        self.flashing_jewels.draw()

    def on_key_press(self, key, modifiers):
        """Handle user keyboard input
        Q: Quit the game

        Arguments:
                key {int} == which key was pressed
                modifiers {int} -- which modifers were pressed
        """
        if key == arcade.key.UP and not self.paused:
            self.rotate()
        elif key == arcade.key.LEFT and not self.paused:
            self.move_left()
        elif key == arcade.key.RIGHT and not self.paused:
            self.move_right()
        elif key == arcade.key.DOWN or key == arcade.key.SPACE and \
                not self.paused:
            self.drop()
        elif key == arcade.key.E:
            # Exit game
            self.exit_game()
        elif key == arcade.key.P:
            # Toggle pause
            self.toggle_pause()
        elif key == arcade.key.S:
            # Toggle sound
            self.sound = not self.sound
        elif key == arcade.key.Q or key == arcade.key.X:
            # Quit
            arcade.close_window()

# vim:ft=python tabstop=4 expandtab autoindent foldmethod=indent:
