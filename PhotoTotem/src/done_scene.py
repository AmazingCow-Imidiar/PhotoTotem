# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    done_scene.py                               ##
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
#Python
import os;
import json;
#Project
import config_validation;
import scene_manager;
from   logger      import Logger;
from   camera      import Camera;
from   base_scene  import BaseScene;
from   widgets     import Sprite;
from   widgets     import Button;
from   clock       import BasicClock;
from   dict_helper import DictHelper;

class DoneScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    _KEY_STATIC_SPRITES = "static_sprites";

    _REQUIRED_KEYS = [
        _KEY_STATIC_SPRITES,
    ];

    #Layers.
    _LAYER_INDEX_STATIC_SPRITE = 1;

    #How much time the scene will stay active (in ms).
    _SCENE_TIMER_TIME = 1000;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        ## iVars ##
        #Filenames and Content.
        self._config_filename = None;
        self._config_contents = None;

        #Scene timer.
        self._scene_timer = BasicClock(DoneScene._SCENE_TIMER_TIME,
                                       self._on_scene_timer_tick);


    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("DoneScene.start");
        #Start the timer just as the scene became active.
        self._scene_timer.start();

    def end(self):
        Logger.instance().log_debug("DoneScene.end");


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("DoneScene.init");

        self._config_filename = scene_manager.SceneManager.instance().get_done_scene_filename();

        #Validate the configuration.
        config_info = config_validation.validate("DoneScene",
                                                  self._config_filename,
                                                  DoneScene._REQUIRED_KEYS);
        self._config_contents = DictHelper(config_info);

        #Init the UI.
        self._init_static_sprites();


    def _init_static_sprites(self):
        sprite_list = self._config_contents.value_or_die(DoneScene._KEY_STATIC_SPRITES);
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image  (info["image"   ]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = DoneScene._LAYER_INDEX_STATIC_SPRITE);


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def update(self, dt):
        self._scene_timer.update(dt);


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def _on_scene_timer_tick(self):
        #Go to another scene.
        scene_manager.SceneManager.instance().scene_done_complete();

