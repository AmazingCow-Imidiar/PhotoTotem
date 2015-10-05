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
import time;
#Pygame
import pygame;
import pygame.camera;
#Project
import config_validation;
import filesystem;
from   config import Config;
from   logger import Logger;

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
        ## iVars ##
        #Configuration stuff.
        self.__config_filename = None;
        self.__file_contents   = None;
        #Camera stuff.
        self.__resolution = None;
        self.__device     = None;
        self.__camera     = None;
        #Photos.
        self.__last_photo = None;
        #Dummy Camera.
        self.__dummy_camera_font  = None;
        self.__dummy_camera_image = None;


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

        #Initialize pygame.
        try:
            #Pygame is initialized always.
            pygame.init();

            #If we are using the dummy camera, init the it's font and image.
            if(Config.instance().get_dummy_camera()):
                #Font.
                font_path = filesystem.canonical_path("./private_resources/dummy_camera_font.ttf");
                self.__dummy_camera_font = pygame.font.Font(font_path, 50);
                #Image.
                image_path = filesystem.canonical_path("./private_resources/dummy_camera_image.png");
                self.__dummy_camera_image = pygame.image.load(image_path);
            #Otherwise initialize the real camera.
            else:
                pygame.camera.init();
                # #Initialize the camera.
                self.__camera = pygame.camera.Camera(self.__device,
                                                     self.__resolution);
                self.__camera.start();

        #All errors here are fatal.
        except Exception, e:
            Logger.instance().log_fatal("Camera - {}".format(e));


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
        Logger.instance().log_debug("Camera.start");
        if(not Config.instance().get_dummy_camera()):
            self.__camera.start();

    def stop(self):
        Logger.instance().log_debug("Camera.stop");
        if(not Config.instance().get_dummy_camera()):
            self.__camera.stop();

    def get_frame(self, scale_to = None):
        img = None;

        #When using a dummy camera, get the current time and blit it
        #onto the dummy_image - The result is a generation of the "new"
        #image with the current time.
        if(Config.instance().get_dummy_camera()):
            time_label = str(time.time());
            font_surface = self.__dummy_camera_font.render(time_label,
                                                           True,
                                                           (0, 0,  0),    #Black
                                                           (255, 0,255)); #Magenta
            img = self.__dummy_camera_image.copy();
            img.blit(font_surface, (10, 10));

        #When not using the dummy camera, just grab the current camera frame.
        else:
            img = self.__camera.get_image();


        return self.__scale_img(img, scale_to);


    def take_photo(self):
        Logger.instance().log_debug("Camera.take_photo");
        self.__last_photo = self.get_frame();

    def get_last_photo(self, scale_to = None):
        return self.__scale_img(self.__last_photo, scale_to);

    def __scale_img(self, original, scale_to):
        if(scale_to is None):
            return original;

        scaled_img = pygame.transform.scale(original, scale_to);
        return scaled_img;
