# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    sprite.py                                   ##
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

import pygame;
from base_widget import BaseWidget;

class Sprite(BaseWidget):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseWidget.__init__(self);
        #COWTODO: Remove.
        print "Sprite.__init__";

        ## iVars ##
        self.__surface     = None;
        self.__bouding_box = None;

    ############################################################################
    ## Set Image Methods                                                      ##
    ############################################################################
    def set_image_filename(self, filename):
        self.__surface = pygame.image.load(filename);
        self.__bouding_box = pygame.Rect(0,0,
                              self.__surface.get_width(),
                              self.__surface.get_height());

    ############################################################################
    ## Position Methods                                                       ##
    ############################################################################
    def set_position(self, x, y):
        self.x = x;
        self.y = y;
        self.__bouding_box[0] = x;
        self.__bouding_box[1] = y;

    def get_bounding_box(self):
        return self.__bouding_box;

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        surface.blit(self.__surface, (self.x, self.y));

    def handle_events(self, event):
        pass;
