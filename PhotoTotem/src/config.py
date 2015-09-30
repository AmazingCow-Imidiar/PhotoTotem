# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    config.py                                   ##
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
import getopt;
import sys;
#Project
from gui    import GUI;
from logger import Logger;
import config_validation;

class Config(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Flags.
    __FLAG_CONFIG     = "config";
    __ALL_FLAGS_SHORT = "";
    __ALL_FLAGS_LONG  = [__FLAG_CONFIG+"="];

    #Required keys.
    __REQUIRED_KEY_CAMERA_FILENAME       = "camera_config_filename";
    __REQUIRED_KEY_SCENEMANAGER_FILENAME = "scene_manager_config_filename";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_CAMERA_FILENAME,
        __REQUIRED_KEY_SCENEMANAGER_FILENAME,
    ];


    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    __instance = None;
    @staticmethod
    def instance():
        if(Config.__instance is None):
            Config.__instance = Config();

        return Config.__instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Remove
        print "Config.__init__";

        ## iVars ##
        self.__config_filename = None;
        self.__file_contents   = None;


    ############################################################################
    ## Init Method                                                            ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("Config.init");

        #Try to get the command line options.
        try:
            options = getopt.gnu_getopt(sys.argv[1:],
                                        Config.__ALL_FLAGS_SHORT,
                                        Config.__ALL_FLAGS_LONG);
        except Exception, e:
            Logger.instance().log_fatal(e);

        #Parse the options.
        for option in options[0]:
            key, value = option;
            key = key.lstrip("-");

            #Configuration filename.
            if(key in Config.__FLAG_CONFIG):
                self.__config_filename = value;

        #Check if file is valid.
        self.__file_contents = config_validation.validate("Config",
                                                          self.__config_filename,
                                                          Config.__REQUIRED_KEYS);


    ############################################################################
    ## Getters                                                                ##
    ############################################################################
    def get_camera_config_filename(self):
        return self.__file_contents[Config.__REQUIRED_KEY_CAMERA_FILENAME];

    def get_scene_manager_config_filename(self):
        return self.__file_contents[Config.__REQUIRED_KEY_SCENEMANAGER_FILENAME];



