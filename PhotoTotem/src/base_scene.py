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
#Project
from logger import Logger;

################################################################################
## Scene                                                                      ##
################################################################################
class BaseScene(pygame.sprite.LayeredUpdates):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self);

    ############################################################################
    ## Abstract Methods                                                       ##
    ############################################################################
    def start(self):
        assert "override me";

    def end(self):
        assert "override me";

    ############################################################################
    ## Handle Events                                                          ##
    ############################################################################
    def handle_events(self, event):
        pass;

