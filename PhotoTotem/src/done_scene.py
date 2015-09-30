# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    done_scene.py                               ##
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
#Python
import os;
import json;
#Project
from logger     import Logger;
from camera     import Camera;
from base_scene import BaseScene;
from widgets    import Sprite;
from widgets    import Button;
from clock      import BasicClock;
import config_validation;
import scene_manager;

class DoneScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    __REQUIRED_KEY_STATIC_SPRITES = "static_sprites";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_STATIC_SPRITES,
    ];

    #COWTODO: COMMENT.
    __LAYER_INDEX_STATIC_SPRITE = 1;

    __SCENE_TIMER_TIME = 1000;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        #COWTODO: Remove it.
        print "DoneScene.__init__";

        ## iVars ##
        #Filenames and Content.
        self.__config_filename = None;
        self.__file_contents   = None;

        #Scene timer.
        self.__scene_timer = BasicClock(DoneScene.__SCENE_TIMER_TIME,
                                        self.__on_scene_timer_tick);

    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("DoneScene.start");
        self.__scene_timer.start();

    def end(self):
        Logger.instance().log_debug("DoneScene.end");

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("DoneScene.init");
        self.__config_filename = scene_manager.SceneManager.instance().get_done_scene_filename();

        #Validate the configuration.
        self.__file_contents = config_validation.validate("DoneScene",
                                                          self.__config_filename,
                                                          DoneScene.__REQUIRED_KEYS);
        #Init the UI.
        self.__init_static_sprites();

    def __init_static_sprites(self):
        sprite_list = self.__file_contents[DoneScene.__REQUIRED_KEY_STATIC_SPRITES];
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image(info["image"]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = DoneScene.__LAYER_INDEX_STATIC_SPRITE);


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def update(self, dt):
        self.__scene_timer.update(dt);

    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def __on_scene_timer_tick(self):
        #Go to another scene.
        scene_manager.SceneManager.instance().scene_done_complete();

