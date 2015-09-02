# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    scene_manager.py                            ##
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
import pygame.locals;
#Project
from config              import Config;
from logger              import Logger;
from scenes.camera_scene import CameraScene;

class SceneManager(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Window Properties.
    __REQUIRED_KEY_WINDOW_SIZE = "window_size";

    #Scenes Filenames.
    __REQUIRED_KEY_SCENE_CAMERA_FILENAME    = "scene_camera_filename";
    __REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME = "scene_postphoto_filename";
    __REQUIRED_KEY_SCENE_FILTER_FILENAME    = "scene_filter_filename";
    __REQUIRED_KEY_SCENE_DONE_FILENAME      = "scene_done_filename";

    #Scenes Enabled.
    __REQUIRED_KEY_SCENE_POSTPHOTO_ENABLED = "scene_postphoto_enabled";
    __REQUIRED_KEY_SCENE_FILTER_ENABLED    = "scene_filter_enabled";
    __REQUIRED_KEY_SCENE_DONE_ENABLED      = "scene_done_enabled";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_WINDOW_SIZE,

        __REQUIRED_KEY_SCENE_CAMERA_FILENAME,
        __REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME,
        __REQUIRED_KEY_SCENE_FILTER_FILENAME,
        __REQUIRED_KEY_SCENE_DONE_FILENAME,

        __REQUIRED_KEY_SCENE_POSTPHOTO_ENABLED,
        __REQUIRED_KEY_SCENE_FILTER_ENABLED,
        __REQUIRED_KEY_SCENE_DONE_ENABLED,
    ];

    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    __instance = None;
    @staticmethod
    def instance():
        if(SceneManager.__instance is None):
            SceneManager.__instance = SceneManager();
        return SceneManager.__instance;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Remove.
        print "SceneManager.__init__";

        ## iVars ##
        self.__config_filename = None;
        self.__file_contents   = None;

        #Pygame related.
        self.__screen_surface = None;
        self.__app_clock      = None;
        self.__app_fps        = None;
        self.__app_running    = None;

        #Scenes.
        self.__scene_camera    = None;
        self.__scene_postphoto = None;
        self.__scene_filter    = None;
        self.__scene_done      = None;

        self.__scene_current   = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("SceneManager.init");

        #Get the configuration filename for SceneManager.
        self.__config_filename = Config.instance().get_scene_manager_config_filename();

        #Validate the configuration.
        self.__validate_config_file();

        #Initialize the Pygame.
        self.__init_pygame();

        #Initialize the Scenes.
        self.__init_scenes();

    def __init_pygame(self):
        pygame.init();

        self.__app_running = False;

        self.__app_clock = pygame.time.Clock();
        self.__app_fps   = float(60.0);

        self.__screen_surface = pygame.display.set_mode(self.get_window_size());
        self.__screen_surface.fill((0,0,0));

    def __init_scenes(self):
        self.__scene_camera = CameraScene();


    ############################################################################
    ## Run                                                                    ##
    ############################################################################
    def run(self):
        Logger.instance().log_debug("SceneManager.run");

        self.__app_running = True;
        while(self.__app_running):
            self.__handle_events();
            self.__update();
            self.__draw();

            self.__app_clock.tick(self.__app_fps);

    def __handle_events(self):
        for event in pygame.event.get():
            if(event.type == pygame.locals.QUIT):
                self.__app_running = False;
            else:
                self.__scene_camera.handle_events(event);

    def __update(self):
        pass;

    def __draw(self):
        self.__scene_camera.draw(self.__screen_surface);
        pygame.display.update();

    ############################################################################
    ## Quit                                                                   ##
    ############################################################################
    def quit(self):
        Logger.instance().log_debug("SceneManager.quit");
        pygame.quit();


    ############################################################################
    ## Getters Methods                                                        ##
    ############################################################################
    #Window Properties.
    def get_window_size(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_WINDOW_SIZE];

    #Scenes Filenames.
    def get_camera_scene_filename(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_CAMERA_FILENAME];
    def get_postphoto_scene_filename(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME];
    def get_filter_scene_filename(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_FILTER_FILENAME];
    def get_done_scene_filename(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_DONE_FILENAME];

    #Scenes Enabled.
    def get_postphoto_scene_enabled(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_POSTPHOTO_ENABLED];
    def get_filter_scene_enabled(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_FILTER_ENABLED];
    def get_done_scene_enabled(self):
        return self.__file_contents[SceneManager.__REQUIRED_KEY_SCENE_DONE_ENABLED];

    ############################################################################
    ## Validation Methods                                                     ##
    ############################################################################
    def __validate_config_file(self):
        Logger.instance().log_debug("SceneManager.validate_config_file");

        #Just to ease the typing.
        filename = self.__config_filename;

        #Check if filename is valid.
        #Empty.
        if(len(filename) == 0):
            Logger.instance().log_fatal("SceneManager Configuration Filename is empty.");
        #Not a valid file path.
        if(not os.path.isfile(filename)):
            msg = "SceneManager Configuration Filename ({}) is invalid.".format(filename);
            Logger.instance().log_fatal(msg);

        #Check if is a valid json.
        try:
            self.__file_contents = json.load(open(filename));
        except:
            msg = "{} ({}) {}.".format("SceneManager Configuration File",
                                       filename,
                                       "isn't a valid json file.");
            Logger.instance().log_fatal(msg);


        #Check if file has the required keys.
        for key in SceneManager.__REQUIRED_KEYS:
            if(key not in self.__file_contents):
                msg = "{} ({}) {} ({})".format("Configuration File",
                                               filename,
                                               "doesn't have required key",
                                               key);
                Logger.instance().log_fatal(msg);

