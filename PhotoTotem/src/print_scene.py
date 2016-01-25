# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    print_scene.py                              ##
##              █ █        █ █    Amazing Photo Totem                         ##
##               ████████████                                                 ##
##             █              █   Copyright (c) 2016 - AmazingCow             ##
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
import printer_manager;

from   logger      import Logger;
from   base_scene  import BaseScene;
from   widgets     import Sprite;
from   widgets     import Button;
from   clock       import BasicClock;
from   dict_helper import DictHelper;


class PrintScene(BaseScene):
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

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        ## iVars ##
        #Filenames and Content.
        self._config_filename = None;
        self._config_contents = None;

        self.a = None;

    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("PrintScene.start");

    def end(self):
        Logger.instance().log_debug("PrintScene.end");


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("PrintScene.init");

        self._config_filename = scene_manager.SceneManager.instance().get_print_scene_filename();

        #Validate the configuration.
        config_info = config_validation.validate("PrintScene",
                                                  self._config_filename,
                                                  PrintScene._REQUIRED_KEYS);
        self._config_contents = DictHelper(config_info);

        #Init the UI.
        self._init_static_sprites();


        #Init the print manager.
        printer_manager.PrinterManager.instance().print_photo("ola_Ateste_mate", self._on_print_completed);


    def _init_static_sprites(self):
        sprite_list = self._config_contents.value_or_die(PrintScene._KEY_STATIC_SPRITES);
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image  (info["image"   ]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = PrintScene._LAYER_INDEX_STATIC_SPRITE);

            self.a = sprite;

    def update(self, dt):
        pos = self.a.get_position();
        pos = pos[0] + (100 * dt), pos[1];
        self.a.set_position(pos);

    def _on_print_completed(self):
        print "CCOMDASFSDAFSDAFSDAFDASFDAS";
