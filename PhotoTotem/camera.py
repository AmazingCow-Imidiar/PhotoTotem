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
import config_validation;

#COWTODO: REMOVe
import time;

class Camera(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
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

        self._font = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("Camera.init");

        #Get the configuration filename for camera.
        self.__config_filename = Config.instance().get_camera_config_filename();

        #Validate the configuration.
        self.__file_contents = config_validation.validate("Camera",
                                                          self.__config_filename,
                                                          Camera.__REQUIRED_KEYS);

        #Set the values.
        self.__resolution = self.__file_contents[Camera.__REQUIRED_KEY_RESOLUTION];
        self.__device     = self.__file_contents[Camera.__REQUIRED_KEY_DEVICE];

        self.__init_camera_device();

    def __init_camera_device(self):
        Logger.instance().log_debug("Camera.init_camera_device");

        #COWTODO: Uncomment.
        #Initialize pygame.
        try:
            pygame.init();
            self._font = pygame.font.Font("./imgs/SourceCodePro-Regular.ttf", 50);
        #     pygame.camera.init();
        except Exception, e:
            Logger.instance().log_fatal("Camera - {}".format(e));

        # #Initialize the camera.
        # self.__camera = pygame.camera.Camera(self.__device, self.__resolution);
        # self.__camera.start();


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

    def get_frame(self, scale_to = None):
        #COWTODO: Uncomment.
        # img = self.__camera.get_image();

        #COWTODO: Only for dev on OSX.
        surface = self._font.render(str(time.clock()), True, (0, 0,  0), (255, 0,255));
        img = pygame.image.load("./imgs/ingrid.jpg");
        img.blit(surface, (10, 10));

        return self.__scale_img(img, scale_to);


    def take_photo(self):
        self.__last_photo = self.get_frame();

    def get_last_photo(self, scale_to = None):
        return self.__scale_img(self.__last_photo, scale_to);

    def __scale_img(self, original, scale_to):
        if(scale_to is None):
            return original;

        scaled_img = pygame.transform.scale(original, scale_to);
        return scaled_img;
