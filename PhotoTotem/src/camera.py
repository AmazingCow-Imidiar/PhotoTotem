# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    camera.py                                   ##
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
import os.path;
import json;
import time;
#Pygame
import pygame;
import pygame.camera;
#Project
import config_validation;
import filesystem;
from   config      import Config;
from   logger      import Logger;
from   dict_helper import DictHelper;


class Camera(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    _KEY_RESOLUTION = "camera_resolution";
    _KEY_DEVICE     = "camera_device";

    _REQUIRED_KEYS = [
        _KEY_RESOLUTION,
        _KEY_DEVICE,
    ];


    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    _instance = None;
    @staticmethod
    def instance():
        if(Camera._instance is None):
            Camera._instance = Camera();
        return Camera._instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        ## iVars ##
        #Configuration stuff.
        self._config_filename = None;
        self._config_contents = None;
        #Camera stuff.
        self._resolution        = None;
        self._device            = None;
        self._camera            = None;
        self._camera_surface    = None;
        self._should_flip_image = None;
        #Photos.
        self._last_photo = None;
        #Dummy Camera.
        self._dummy_camera_font  = None;
        self._dummy_camera_image = None;


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("Camera.init");

        #Get the configuration filename for camera.
        self._config_filename = Config.instance().get_camera_config_filename();

        #Validate the configuration.
        config_info = config_validation.validate("Camera",
                                                          self._config_filename,
                                                          Camera._REQUIRED_KEYS);

        self._config_contents = DictHelper(config_info);

        #Set the values.
        self._resolution = self._config_contents.value_or_die(Camera._KEY_RESOLUTION);
        self._device     = self._config_contents.value_or_die(Camera._KEY_DEVICE);

        self._should_flip_image = True;

        self._init_camera_device();


    def _init_camera_device(self):
        Logger.instance().log_debug("Camera.init_camera_device");

        #Initialize pygame.
        try:
            #Pygame is initialized always.
            pygame.init();

            #If we are using the dummy camera, init the it's font and image.
            if(Config.instance().get_dummy_camera()):
                self._init_dummy_camera();

            #Otherwise initialize the real camera.
            else:
                self._init_real_camera();

        #All errors here are fatal.
        except Exception, e:
            Logger.instance().log_fatal("Camera - {}".format(e));

    def _init_dummy_camera(self):
        #Font.
        font_path = filesystem.canonical_path("./private_resources/dummy_camera_font.ttf");
        self._dummy_camera_font = pygame.font.Font(font_path, 50);
        #Image.
        image_path = filesystem.canonical_path("./private_resources/dummy_camera_image.png");
        self._dummy_camera_image = pygame.image.load(image_path);

    def _init_real_camera(self):
        pygame.camera.init();
        # #Initialize the camera.
        self._camera = pygame.camera.Camera(self._device,
                                            self._resolution);
        self._camera.start();
        self._camera_surface = self._camera.get_image();


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
            self._camera.start();

    def stop(self):
        Logger.instance().log_debug("Camera.stop");
        if(not Config.instance().get_dummy_camera()):
            self._camera.stop();

    def get_frame(self, scale_to = None):
        img = self._camera_surface;

        #When using a dummy camera, get the current time and blit it
        #onto the dummy_image - The result is a generation of the "new"
        #image with the current time.
        if(Config.instance().get_dummy_camera()):
            time_label = str(time.time());
            font_surface = self._dummy_camera_font.render(time_label,
                                                           True,
                                                           (0,   0,   0),  #Black
                                                           (255, 0, 255)); #Magenta
            img = self._dummy_camera_image.copy();
            img.blit(font_surface, (10, 10));

        #When not using the dummy camera, just grab the current camera frame.
        else:
            #Decouple the camera from the fps.
            #So if camera is ready we return the new frame,
            #otherwise we just return the old Frame.
            if(self._camera.query_image()):
                img = self._camera.get_image(self._camera_surface);

        if(self._should_flip_image):
            img = pygame.transform.flip(img, True, False);

        return self._scale_img(img, scale_to);


    def take_photo(self):
        Logger.instance().log_debug("Camera.take_photo");
        self._last_photo = self.get_frame();

    def get_last_photo(self, scale_to = None):
        return self._scale_img(self._last_photo, scale_to);

    def _scale_img(self, original, scale_to):
        if(scale_to is None):
            return original;

        scaled_img = pygame.transform.scale(original, scale_to);
        return scaled_img;
