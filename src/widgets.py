# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        widgets.py                                ##
##            █ █        █ █        AmazingCow/Imidiar - Photo Totem          ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##
## Imports ##
#Pygame
import pygame;
#Project.
from logger import Logger;

################################################################################
## Sprite                                                                     ##
################################################################################
class Sprite(pygame.sprite.Sprite):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, surface = None):
        pygame.sprite.Sprite.__init__(self);

        self.rect = pygame.rect.Rect(0,0,0,0);

        if(surface is not None):
            self.update_image(surface);


    ############################################################################
    ## Image Methods                                                          ##
    ############################################################################
    def load_image(self, filename):
        surface = pygame.image.load(filename).convert_alpha();
        self.update_image(surface);

    def update_image(self, surface):
        self.image   = surface;
        self.rect[2] = self.image.get_width();
        self.rect[3] = self.image.get_height();


    ############################################################################
    ## Positions Setter/Getters                                               ##
    ############################################################################
    def set_position(self, pos):
        self.rect[0] = pos[0];
        self.rect[1] = pos[1];

    def get_position(self):
        return self.rect[0], self.rect[1];


    ############################################################################
    ## Size Setter/Getters                                                    ##
    ############################################################################
    def get_size(self):
        return self.rect[2], self.rect[3];



class Button(Sprite):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Sprite.__init__(self);

        ## iVars #
        self._normal_surface  = None;
        self._pressed_surface = None;

        self._click_callback = None;


    ############################################################################
    ## Set Image Methods                                                      ##
    ############################################################################
    def load_images(self, normal_filename, pressed_filename):
        self._normal_surface  = pygame.image.load(normal_filename);
        self._pressed_surface = pygame.image.load(pressed_filename);

        self.reset();


    ############################################################################
    ## Callback Methods                                                       ##
    ############################################################################
    def set_click_callback(self, callback):
        self._click_callback = callback;


    ############################################################################
    ## State Methods                                                          ##
    ############################################################################
    def reset(self):
        self._set_normal_state();

    def _set_pressed_state(self):
        self.update_image(self._pressed_surface);

    def _set_normal_state(self):
        self.update_image(self._normal_surface);


    def handle_events(self, event):
        #Check which type of event and pass to handler.
        if(event.type == pygame.locals.MOUSEBUTTONDOWN):
            self._onMouseButtonDown();
        elif(event.type == pygame.locals.MOUSEBUTTONUP):
            self._onMouseButtonUp();


    ############################################################################
    ## Mouse Events                                                           ##
    ############################################################################
    def _onMouseButtonDown(self):
        #User touch the screen, check if the touch point
        #is inside of the Button bounding box and set
        #the state to pressed if is.
        pos = pygame.mouse.get_pos();
        if(self.rect.collidepoint(pos)):
            self._set_pressed_state();

    def _onMouseButtonUp(self):
        #Button untouch the screen, set the state to normal
        #and check if the touch point was inside the button
        #bouding box. If was set that button was pressed.
        self.reset();

        pos = pygame.mouse.get_pos();
        if(self.rect.collidepoint(pos) and self._click_callback is not None):
            self._click_callback();
