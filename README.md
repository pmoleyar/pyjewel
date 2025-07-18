# pyjewel
 A falling blocks game.
 Ported to python by Prabhanjan M. from "xjewel" version 1.6 (1/29/93) By David Cooper and José Guterman.
 
 Original README follows.

==============================================================================

			    #
			   #  ######  #    #  ######  #
			  #  #       #    #  #       #
			 #  #####   #    #  #####   #
		  #     #  #       # ## #  #       #
		 #     #  #       ##  ##  #       #
		 #####   ######  #    #  ######  ######

==============================================================================

This game was originally written by Yoshihiro Satoh of HP.  David Cooper
then replicated Domain/JewelBox under X.

I have taken the bitmaps from the original game carried over by David Cooper
I hold the copyright for the code, as I created it, but I hold no claim to the
bitmaps which were freely distributed with the Domain version.

REDISTRIBUTION in source or binary from is permited as long as adequate
notation of the originators is retained, including the developer of the 
original Domain/Jewlbox, Yoshihiro Satoh.
NOTE: I do not claim to hold any copyright on columns games, Jewelbox, or any
related name or icon.  I have written the source and thats all I hold claim to.

USE AT YOUR OWN RISK AND PERIL, I MAKE NO CLAIM OF USEABILITY OR WARANTY.

PLAYING
=======

Jewel is a game much like Domain/Jewelbox which is a puzzle game like
Tetris.

It is played by controling the motion of blocks which continue to fall from
the top of the screen.  One can move them left and right, as well as
rotate the jewel segements.  The object is to get the most points before
the grim reaper ends the fun.

Death happens when the screen is no longer capable of holding any more
blocks.  To make high scores more interesting, you are given but three
attempts to get points -- use them wisely.

As the game progresses, and more jewels are removed, the speed of the game
will increase.  This is measured in seconds of delay between steps of
block motion.

Keys
----
There are three sets of keys that can be used:
( or any combination )

Option 1:

         +---+ +---+ +---+
         | j | | k | | l |
         +---+ +---+ +---+
           ^     ^     ^
           |     |     |__ move block right
           |     |________ rotate block
           |______________ move block left

         +---------+
         |  SPACE  | <---- drop block
         +---------+

Option 2:

         +---+ +---+ +---+
         | 4 | | 5 | | 6 |
         +---+ +---+ +---+
           ^     ^     ^
           |     |     |__ move block right
           |     |________ rotate block
           |______________ move block left

         +---------+
         |    0    | <---- drop block
         +---------+

Option 3: (cursor keypad)
                
               +---+
               | ^ | <----  rotate block
               +---+
         +---+ +---+ +---+
         | < | | V | | > |
         +---+ +---+ +---+
           ^     ^     ^
           |     |     |__ move block right
           |     |________ drop block
           |______________ move block left


Rotations
---------
The folowing rotations are possible:
( there are no others )

              +---+       +---+       +---+
              | 1 |       | 3 |       | 2 |
              +---+       +---+       +---+
              | 2 |  ==>  | 1 | ==>   | 3 |
              +---+       +---+       +---+
              | 3 |       | 2 |       | 1 |
              +---+       +---+       +---+



SCORING
=======

The basic way to get points is to unite the jewels to form triplet (or
higher) matches.  This can be done in any direction, and can be
accomplished in more than one part of the board at one time.  As the
jewels are removed, the board falls to fill the spaces -- matches may
again occur.

These teritiary matches provide an interesting part to the game due to the
formula for calculating points:
    
    ( 300 (for base triplet) + 150 * (each additional jewel) ) * 2^order

    where order is the number of the repeition from which the match
    occured.

As a light at the end of the bleak tunnel, a WILD CARD is available.  The
wild block will be given at infrequent intervals, and will give the user
the points for one triplet by removing all the jewels of a particular
shape/color.

To add some interest to the game, points are awarded for dropping the
block from a height above its resting place.  This is accumlated at 10
points per level above the place it will rest.

Stages
------
There are no changes for the higher levels, although the speed increases,
proportionaly to the level.  Stage increases with the successful
completion of the 50 jewels required per level.  The current status is
shown in the REST field.


ORIGINAL NOTATIONS
==================
>>Authors
>>-------
>>
>>   Programming       Yoshihiro Satoh
>>   Font Design       Yoshiharu Minami
>>   Document Writing  Nancy Paisner
>>
>>Copyright
>>---------
>>
>>  This software is in the Yoshihiro's Arcade Collections.
>>  Domain/JewelBox is a trade mark of Yoshihiro Satoh.
>>
>>  Copyright @ 1990 by Yoshihiro Satoh
>>  All rights are reserved by Yoshihiro Satoh.
>
>xjewel - Jewel for X11 Copyright 1992 by David Cooper
>
