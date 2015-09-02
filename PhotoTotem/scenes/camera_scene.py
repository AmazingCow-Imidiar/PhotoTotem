# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    camera_scene.py                             ##
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
#Project
from logger         import Logger;
from scene_manager  import *;
from base_scene     import BaseScene;
from widgets.button import Button;
from widgets.sprite import Sprite;

class CameraScene(BaseScene):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        #COWTODO: Remove it.
        print "CameraScene.__init__";
        self.button = Button();
        self.button.set_sprite_filenames("./imgs/Button_Delete_Normal.png",
                                         "./imgs/Button_Delete_Pressed.png");
        self.button.set_position(100, 100);

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("CameraScene.init");
        SceneManager.instance().get_camera_scene_filename();

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;
    def draw(self, surface):
        self.button.draw(surface);

    def handle_events(self, event):
        pass;
