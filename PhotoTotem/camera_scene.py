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
#Python
import os;
import json;
#Project
from logger     import Logger;
from base_scene import BaseScene;
from button     import Button;
from sprite     import Sprite;
import scene_manager; #Not from ... import to avoid circular imports.

class CameraScene(BaseScene):
     ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE = "camera_placeholder";
    __REQUIRED_KEY_TAKEPHOTO_BUTTON          = "take_photo";
    __REQUIRED_KEY_STATIC_SPRITES            = "static_sprites";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE,
        __REQUIRED_KEY_TAKEPHOTO_BUTTON,
        __REQUIRED_KEY_STATIC_SPRITES,
    ];

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);
        #COWTODO: Remove it.
        print "CameraScene.__init__";

        ## iVars ##
        self.__config_filename = None;
        self.__file_contents   = None;

        self.__static_sprites    = None;
        self.__take_photo_button = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("CameraScene.init");
        self.__config_filename = scene_manager.SceneManager.instance().get_camera_scene_filename();

        #Validate the configuration.
        self.__validate_config_file();

        #Init the UI.
        self.__init_static_sprites();
        self.__init_camera();
        self.__init_buttons();

    def __init_static_sprites(self):
        self.__static_sprites = [];

        l = self.__file_contents[CameraScene.__REQUIRED_KEY_STATIC_SPRITES];
        for sprite_info in l:
            pos = sprite_info["position"];
            fn  = sprite_info["image"];

            sprite = Sprite();
            sprite.set_image_filename(fn);
            sprite.set_position(pos[0], pos[1]);

            self.__static_sprites.append(sprite);

    def __init_camera(self):
        pass;

    def __init_buttons(self):
        self.__take_photo_button = Button();

        button_info = self.__file_contents[CameraScene.__REQUIRED_KEY_TAKEPHOTO_BUTTON];

        pos           = button_info["position"];
        normal_image  = button_info["normal_image"];
        pressed_image = button_info["pressed_image"];

        self.__take_photo_button.set_sprite_filenames(normal_image, pressed_image);
        self.__take_photo_button.set_position(pos[0], pos[1]);


    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        for static_sprite in self.__static_sprites:
            static_sprite.draw(surface);
        self.__take_photo_button.draw(surface);

    def handle_events(self, event):
        self.__take_photo_button.handle_events(event);

    ############################################################################
    ## Validation Methods                                                     ##
    ############################################################################
    def __validate_config_file(self):
        Logger.instance().log_debug("CameraScene.validate_config_file");

        #Just to ease the typing.
        filename = self.__config_filename;

        #Check if filename is valid.
        #Empty.
        if(len(filename) == 0):
            Logger.instance().log_fatal("CameraScene Configuration Filename is empty.");
        #Not a valid file path.
        if(not os.path.isfile(filename)):
            msg = "CameraScene Configuration Filename ({}) is invalid.".format(filename);
            Logger.instance().log_fatal(msg);

        #Check if is a valid json.
        try:
            self.__file_contents = json.load(open(filename));
        except Exception, e:
            msg = "{} ({}) {}.".format("CameraScene Configuration File",
                                       filename,
                                       "isn't a valid json file.");
            Logger.instance().log_fatal(msg);


        #Check if file has the required keys.
        for key in CameraScene.__REQUIRED_KEYS:
            if(key not in self.__file_contents):
                msg = "{} ({}) {} ({})".format("CameraScene Configuration File",
                                               filename,
                                               "doesn't have required key",
                                               key);
                Logger.instance().log_fatal(msg);

