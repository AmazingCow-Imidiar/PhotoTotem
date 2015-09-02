# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    button.py                                   ##
##              █ █        █ █    Amazing Photo Totem                         ##
##               ████████████                                                 ##
##             █              █   Copyright (c) 2015 AmazingCow               ##
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
import pygame.locals;
#Project
from base_widget import BaseWidget;
from sprite      import Sprite;


class Button(BaseWidget):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseWidget.__init__(self);
        #COWTODO: Remove.
        print "Button.__init__";

        ## iVars ##
        self.__normal_sprite  = Sprite();
        self.__pressed_sprite = Sprite();
        self.__current_sprite = None;


    ############################################################################
    ## Set Image Methods                                                      ##
    ############################################################################
    def set_sprite_filenames(self, normal_filename, pressed_filename):
        self.set_normal_sprite_filename(normal_filename);
        self.set_pressed_sprite_filename(pressed_filename);

    def set_normal_sprite_filename(self, normal_filename):
        self.__normal_sprite.set_image_filename(normal_filename);
        self.reset();

    def set_pressed_sprite_filename(self, pressed_filename):
        self.__pressed_sprite.set_image_filename(pressed_filename);
        self.reset();

    ############################################################################
    ## Position Methods                                                       ##
    ############################################################################
    def set_position(self, x, y):
        self.x = x;
        self.y = y;

        self.__normal_sprite.set_position(x, y);
        self.__normal_sprite.set_position(x, y);

        self.reset();

    ############################################################################
    ## State Methods                                                          ##
    ############################################################################
    def reset(self):
        self.__set_normal_state();


    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        self.__current_sprite.draw(surface);

    def handle_events(self, event):
        if(event.type == pygame.locals.MOUSEBUTTONDOWN):
            self.__onMouseButtonDown();
        elif(event.type == pygame.locals.MOUSEBUTTONUP):
            self.__onMouseButtonUp();
        elif(event.type == pygame.locals.MOUSEMOTION):
            self.__onMouseMotion();

    def __onMouseButtonDown(self):
        pos = pygame.mouse.get_pos();
        print "on mouse down", pos, self.__current_sprite.get_bounding_box();
        if(self.__current_sprite.get_bounding_box().collidepoint(pos)):
            self.__set_pressed_state();

    def __onMouseButtonUp(self):
        self.reset();
    def __onMouseMotion(self):
        pass;

    def __set_pressed_state(self):
        self.__current_sprite = self.__pressed_sprite;
    def __set_normal_state(self):
        self.__current_sprite = self.__normal_sprite;
