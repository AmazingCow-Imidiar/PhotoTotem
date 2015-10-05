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
import config_validation;
from   config          import Config;
from   logger          import Logger;
from   clock           import BasicClock;
from   camera_scene    import CameraScene;
from   postphoto_scene import PostPhotoScene;
from   done_scene      import DoneScene;



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

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_WINDOW_SIZE,

        __REQUIRED_KEY_SCENE_CAMERA_FILENAME,
        __REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME,
        __REQUIRED_KEY_SCENE_FILTER_FILENAME,
        __REQUIRED_KEY_SCENE_DONE_FILENAME
    ];

    #The frame rate of application.
    __APP_FPS = float(60.0)


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

        #FPS
        self.__fps_timer = None;
        self.__fps_count = None;


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("SceneManager.init");

        #Get the configuration filename for SceneManager.
        self.__config_filename = Config.instance().get_scene_manager_config_filename();

        #Validate the configuration.
        self.__file_contents = config_validation.validate("SceneManager",
                                                          self.__config_filename,
                                                          SceneManager.__REQUIRED_KEYS);
        #Initialize the Pygame.
        self.__init_pygame();

        #Initialize the Scenes.
        self.__change_scene(self.__get_scene_camera_instance());

    def __init_pygame(self):
        #Init pygame.
        pygame.init();

        #Set the app is not running yet (GAME LOOP).
        self.__app_running = False;

        #Init the App clock.
        self.__app_clock = pygame.time.Clock();
        self.__app_fps   = SceneManager.__APP_FPS;

        #Init the Window.
        self.__screen_surface = pygame.display.set_mode(self.get_window_size());
        self.__screen_surface.fill((0,0,0));


    ############################################################################
    ## Run                                                                    ##
    ############################################################################
    def run(self):
        Logger.instance().log_debug("SceneManager.run");

        #Set the app to running and start the clock.
        self.__app_running = True;
        dt = self.__app_clock.tick(self.__app_fps);

        #Start the FPS Counter.
        self.__fps_timer = BasicClock(1000, self.__on_fps_timer_tick);
        self.__fps_timer.start();
        self.__fps_count = 0;

        #Game loop.
        while(self.__app_running):
            #Events/Update/Draw.
            self.__handle_events();
            self.__update(dt);
            self.__draw();

            #Update the timer and check fps.
            dt = self.__app_clock.tick(self.__app_fps);

            self.__fps_timer.update(dt);
            self.__fps_count += 1;


    def __handle_events(self):
        for event in pygame.event.get():
            if(event.type == pygame.locals.QUIT):
                self.__app_running = False;
            else:
                self.__scene_current.handle_events(event);


    def __update(self, dt):
        self.__scene_current.update(dt);


    def __draw(self):
        self.__screen_surface.fill((0,0,0));
        self.__scene_current.draw(self.__screen_surface);
        pygame.display.update();


    ############################################################################
    ## FPS Timer Callback                                                     ##
    ############################################################################
    def __on_fps_timer_tick(self):
        print "FPS:", self.__fps_count;
        self.__fps_count = 0;


    ############################################################################
    ## Quit                                                                   ##
    ############################################################################
    def quit(self):
        Logger.instance().log_debug("SceneManager.quit");
        pygame.quit();


    ############################################################################
    ## Scenes Management                                                      ##
    ############################################################################
    def scene_camera_complete(self):
        self.__change_scene(self.__get_scene_postphoto_instance());

    def scene_postphoto_complete(self, go_back):
        #If go_back is true, means that user
        #didn't accepted the taken photo.
        if(go_back):
            self.__change_scene(self.__get_scene_camera_instance());
        else:
            self.__change_scene(self.__get_scene_done_instance());

    def scene_done_complete(self):
        self.__change_scene(self.__get_scene_camera_instance());

    def __change_scene(self, scene):
        #At first time __scene_current is None.
        if(self.__scene_current is not None):
            self.__scene_current.end();

        self.__scene_current = scene;
        self.__scene_current.start();


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


    ############################################################################
    ## Scenes instances getters                                               ##
    ############################################################################
    def __get_scene_camera_instance(self):
        if(self.__scene_camera is None):
            self.__scene_camera = CameraScene();
            self.__scene_camera.init();
        return self.__scene_camera;

    def __get_scene_postphoto_instance(self):
        if(self.__scene_postphoto is None):
            self.__scene_postphoto = PostPhotoScene();
            self.__scene_postphoto.init();
        return self.__scene_postphoto;

    def __get_scene_done_instance(self):
        if(self.__scene_done is None):
            self.__scene_done = DoneScene();
            self.__scene_done.init();
        return self.__scene_done;

    def __get_scene_filter_instance(self):
        if(self.__scene_postphoto is None):
            self.__scene_postphoto = PostPhotoScene();
            self.__scene_postphoto.init();
        return self.__scene_camera;



