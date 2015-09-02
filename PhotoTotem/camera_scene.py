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
        pass;
    def __init_camera(self):
        pass;
    def __init_buttons(self):
        pass;

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        pass;

    def draw(self, surface):
        pass;

    def handle_events(self, event):
        pass;

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
        except:
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

