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
    _REQUIRED_KEY_WINDOW_SIZE = "window_size";

    #Scenes Filenames.
    _REQUIRED_KEY_SCENE_CAMERA_FILENAME    = "scene_camera_filename";
    _REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME = "scene_postphoto_filename";
    _REQUIRED_KEY_SCENE_FILTER_FILENAME    = "scene_filter_filename";
    _REQUIRED_KEY_SCENE_DONE_FILENAME      = "scene_done_filename";

    _REQUIRED_KEYS = [
        _REQUIRED_KEY_WINDOW_SIZE,

        _REQUIRED_KEY_SCENE_CAMERA_FILENAME,
        _REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME,
        _REQUIRED_KEY_SCENE_FILTER_FILENAME,
        _REQUIRED_KEY_SCENE_DONE_FILENAME
    ];

    #The frame rate of application.
    _APP_FPS = float(60.0)


    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    _instance = None;
    @staticmethod
    def instance():
        if(SceneManager._instance is None):
            SceneManager._instance = SceneManager();
        return SceneManager._instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        ## iVars ##
        self._config_filename = None;
        self._file_contents   = None;

        #Pygame related.
        self._screen_surface = None;
        self._app_clock      = None;
        self._app_fps        = None;
        self._app_running    = None;

        #Scenes.
        self._scene_camera    = None;
        self._scene_postphoto = None;
        self._scene_filter    = None;
        self._scene_done      = None;

        self._scene_current   = None;

        #FPS
        self._fps_timer = None;
        self._fps_count = None;


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("SceneManager.init");

        #Get the configuration filename for SceneManager.
        self._config_filename = Config.instance().get_scene_manager_config_filename();

        #Validate the configuration.
        self._file_contents = config_validation.validate("SceneManager",
                                                          self._config_filename,
                                                          SceneManager._REQUIRED_KEYS);
        #Initialize the Pygame.
        self._init_pygame();

        #Initialize the Scenes.
        self._change_scene(self._get_scene_camera_instance());

    def _init_pygame(self):
        #Init pygame.
        pygame.init();

        #Set the app is not running yet (GAME LOOP).
        self._app_running = False;

        #Init the App clock.
        self._app_clock = pygame.time.Clock();
        self._app_fps   = SceneManager._APP_FPS;

        #Init the Window.
        self._screen_surface = pygame.display.set_mode(self.get_window_size());
        self._screen_surface.fill((0,0,0));


    ############################################################################
    ## Run                                                                    ##
    ############################################################################
    def run(self):
        Logger.instance().log_debug("SceneManager.run");

        #Set the app to running and start the clock.
        self._app_running = True;
        dt = self._app_clock.tick(self._app_fps);

        #Start the FPS Counter.
        self._fps_timer = BasicClock(1000, self._on_fps_timer_tick);
        self._fps_timer.start();
        self._fps_count = 0;

        #Game loop.
        while(self._app_running):
            #Events/Update/Draw.
            self._handle_events();
            self._update(dt);
            self._draw();

            #Update the timer and check fps.
            dt = self._app_clock.tick(self._app_fps);

            self._fps_timer.update(dt);
            self._fps_count += 1;


    def _handle_events(self):
        for event in pygame.event.get():
            #Quit event or Escape key.
            if((event.type == pygame.locals.QUIT or
                event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE)):
                self._app_running = False;
            #Everything else.
            else:
                self._scene_current.handle_events(event);


    def _update(self, dt):
        self._scene_current.update(dt);


    def _draw(self):
        self._scene_current.draw(self._screen_surface);
        pygame.display.update();


    ############################################################################
    ## FPS Timer Callback                                                     ##
    ############################################################################
    def _on_fps_timer_tick(self):
        print "FPS:", self._fps_count;
        self._fps_count = 0;


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
        self._change_scene(self._get_scene_postphoto_instance());

    def scene_postphoto_complete(self, go_back):
        #If go_back is true, means that user
        #didn't accepted the taken photo.
        if(go_back):
            self._change_scene(self._get_scene_camera_instance());
        else:
            self._change_scene(self._get_scene_done_instance());

    def scene_done_complete(self):
        self._change_scene(self._get_scene_camera_instance());

    def _change_scene(self, scene):
        #At first time _scene_current is None.
        if(self._scene_current is not None):
            self._scene_current.end();

        self._scene_current = scene;
        self._scene_current.start();


    ############################################################################
    ## Getters Methods                                                        ##
    ############################################################################
    #Window Properties.
    def get_window_size(self):
        return self._file_contents[SceneManager._REQUIRED_KEY_WINDOW_SIZE];

    #Scenes Filenames.
    def get_camera_scene_filename(self):
        return self._file_contents[SceneManager._REQUIRED_KEY_SCENE_CAMERA_FILENAME];
    def get_postphoto_scene_filename(self):
        return self._file_contents[SceneManager._REQUIRED_KEY_SCENE_POSTPHOTO_FILENAME];
    def get_filter_scene_filename(self):
        return self._file_contents[SceneManager._REQUIRED_KEY_SCENE_FILTER_FILENAME];
    def get_done_scene_filename(self):
        return self._file_contents[SceneManager._REQUIRED_KEY_SCENE_DONE_FILENAME];


    ############################################################################
    ## Scenes instances getters                                               ##
    ############################################################################
    def _get_scene_camera_instance(self):
        if(self._scene_camera is None):
            self._scene_camera = CameraScene();
            self._scene_camera.init();
        return self._scene_camera;

    def _get_scene_postphoto_instance(self):
        if(self._scene_postphoto is None):
            self._scene_postphoto = PostPhotoScene();
            self._scene_postphoto.init();
        return self._scene_postphoto;

    def _get_scene_done_instance(self):
        if(self._scene_done is None):
            self._scene_done = DoneScene();
            self._scene_done.init();
        return self._scene_done;

    def _get_scene_filter_instance(self):
        if(self._scene_postphoto is None):
            self._scene_postphoto = PostPhotoScene();
            self._scene_postphoto.init();
        return self._scene_camera;



