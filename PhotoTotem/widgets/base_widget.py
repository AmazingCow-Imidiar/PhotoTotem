# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    base_widget.py                              ##
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

class BaseWidget(object):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Remove
        print "BaseWidget.__init__";

        ## iVars ##
        self.x = 0;
        self.y = 0;

    ############################################################################
    ## Abstract Methods                                                       ##
    ############################################################################
    def get_bounding_box(self):
        assert "Override me";

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;
    def draw(self, surface):
        pass;
    def handle_events(self, event):
        pass;

