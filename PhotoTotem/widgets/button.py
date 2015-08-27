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
        self.__current_sprite = self.__normal_sprite;


    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        self.__current_sprite.draw(surface);

    def handle_events(self, event):
        #COWTODO: Handle the mouse.
        pass;
