# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    camera.py                                   ##
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
import os.path;
import json;
#Pygame
import pygame;
import pygame.camera;
#Project
from config import Config;
from logger import Logger;

class Camera(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __REQUIRED_KEY_RESOLUTION = "camera_resolution";
    __REQUIRED_KEY_DEVICE     = "camera_device";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_RESOLUTION,
        __REQUIRED_KEY_DEVICE,
    ];

    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    __instance = None;
    @staticmethod
    def instance():
        if(Camera.__instance is None):
            Camera.__instance = Camera();
        return Camera.__instance;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Remove.
        print "Camera.__init__";

        ## iVars ##
        self.__config_filename = None;
        self.__file_contents   = None;

        self.__resolution = None;
        self.__device     = None;

        self.__camera = None;

        self.__last_photo = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("Camera.init");

        #Get the configuration filename for camera.
        self.__config_filename = Config.instance().get_camera_config_filename();

        #Validate the configuration.
        self.__validate_config_file();

        #Set the values.
        self.__resolution = self.__file_contents[Camera.__REQUIRED_KEY_RESOLUTION];
        self.__device     = self.__file_contents[Camera.__REQUIRED_KEY_DEVICE];

        self.__init_camera_device();

    def __init_camera_device(self):
        Logger.instance().log_debug("Camera.init_camera_device");

        #Initialize pygame.
        pygame.init();
        pygame.camera.init();

        #Initialize the camera.
        self.__camera = pygame.camera.Camera(self.__device, self.__resolution);
        self.__camera.start();

    ############################################################################
    ## Quit                                                                   ##
    ############################################################################
    def quit(self):
        Logger.instance().log_debug("Camera.quit");
        pygame.quit();

    ############################################################################
    ## Camera Control                                                         ##
    ############################################################################
    def start(self):
        self.__camera.start();

    def stop(self):
        self.__camera.stop();

    def get_frame(self, scaleTo = None):
        img = self.__camera.get_image();
        if(scaleTo is None):
            return img;
        scaled_img = pygame.transform.scale(img, scaleTo);
        return scaled_img;

    def take_photo(self):
        self.__last_photo = self.get_image();

    def get_last_photo(self):
        return self.__last_photo;

    ############################################################################
    ## Validation Methods                                                     ##
    ############################################################################
    def __validate_config_file(self):
        Logger.instance().log_debug("Camera.validate_config_file");

        #Just to ease the typing.
        filename = self.__config_filename;

        #Check if filename is valid.
        #Empty.
        if(len(filename) == 0):
            Logger.instance().log_fatal("Camera Configuration Filename is empty.");
        #Not a valid file path.
        if(not os.path.isfile(filename)):
            msg = "Camera Configuration Filename ({}) is invalid.".format(filename);
            Logger.instance().log_fatal(msg);

        #Check if is a valid json.
        try:
            self.__file_contents = json.load(open(filename));
        except:
            msg = "{} ({}) {}.".format("Camera Configuration File",
                                       filename,
                                       "isn't a valid json file.");
            Logger.instance().log_fatal(msg);


        #Check if file has the required keys.
        for key in Camera.__REQUIRED_KEYS:
            if(key not in self.__file_contents):
                msg = "{} ({}) {} ({})".format("Configuration File",
                                               filename,
                                               "doesn't have required key",
                                               key);
                Logger.instance().log_fatal(msg);

