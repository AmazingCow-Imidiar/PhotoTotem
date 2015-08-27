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
import os.path;
import json;
#Project
from gui    import GUI;
from logger import Logger;

class Config(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __FLAG_CONFIG     = "config";
    __ALL_FLAGS_SHORT = "";
    __ALL_FLAGS_LONG  = [__FLAG_CONFIG+"="];

    __REQUIRED_KEY_CAMERA_FILENAME = "camera_config_filename";
    __REQUIRED_KEYS = [
        __REQUIRED_KEY_CAMERA_FILENAME,
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
        self.__validate_config_file();


    ############################################################################
    ## Getters                                                                ##
    ############################################################################
    def get_camera_config_filename(self):
        return self.__file_contents[Config.__REQUIRED_KEY_CAMERA_FILENAME];

    ############################################################################
    ## Validation Methods                                                     ##
    ############################################################################
    def __validate_config_file(self):
        Logger.instance().log_debug("Config.validate_config_file");

        #Just to ease the typing.
        filename = self.__config_filename;

        #Check if filename is valid.
        #Empty.
        if(len(filename) == 0):
            Logger.instance().log_fatal("Configuration Filename is empty.");
        #Not a valid file path.
        if(not os.path.isfile(filename)):
            msg = "Configuration Filename ({}) is invalid.".format(filename);
            Logger.instance().log_fatal(msg);

        #Check if is a valid json.
        try:
            self.__file_contents = json.load(open(filename));
        except:
            msg = "{} ({}) {}.".format("Configuration File",
                                       filename,
                                       "isn't a valid json file.");
            Logger.instance().log_fatal(msg);


        #Check if file has the required keys.
        for key in Config.__REQUIRED_KEYS:
            if(key not in self.__file_contents):
                msg = "{} ({}) {} ({})".format("Configuration File",
                                               filename,
                                               "doesn't have required key",
                                               "camera_config_filename");
                Logger.instance().log_fatal(msg);
