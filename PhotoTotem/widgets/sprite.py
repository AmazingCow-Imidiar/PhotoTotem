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
        self.__surface = None;

    ############################################################################
    ## Set Image Methods                                                      ##
    ############################################################################
    def set_image_filename(self, filename):
        self.__surface = pygame.image.load(filename);

    ############################################################################
    ## Position Methods                                                       ##
    ############################################################################
    def set_position(self, x, y):
        self.x = x;
        self.y = y;

    def get_bounding_box(self):
        return self.__surface.get_bounding_rect();

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        surface.blit(self.__surface, (self.x, self.y));

    def handle_events(self, event):
        pass;
