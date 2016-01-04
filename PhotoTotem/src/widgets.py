# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    base_scene.py                               ##
##              █ █        █ █    Amazing Photo Totem                         ##
##               ████████████                                                 ##
##             █              █   Copyright (c) 2015, 2016 - AmazingCow       ##
##            █     █    █     █  www.AmazingCow.com                          ##
##            █     █    █     █                                              ##
##             █              █   N2OMatt - n2omatt@amazingcow.com            ##
##               ████████████     www.amazingcow.com/n2omatt                  ##
##                                                                            ##
##                                                                            ##
##                          This file is proprietary                          ##
##                   CHECK THE COPYING FILE TO MORE DETAILS                   ##
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
