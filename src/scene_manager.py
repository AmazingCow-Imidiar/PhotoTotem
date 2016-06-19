# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        scene_manager.py                          ##
##            █ █        █ █        AmazingCow/Imidiar - Photo Totem          ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must not be misrepresented as being the original software.      ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
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
from   dict_helper     import DictHelper;

from   camera_scene    import CameraScene;
from   postphoto_scene import PostPhotoScene;
from   done_scene      import DoneScene;

class SceneManager(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    ## Public CONSTATNS ##
    SCENE_NAME_CAMERA    = "SCENE_NAME_CAMERA";
    SCENE_NAME_POSTPHOTO = "SCENE_NAME_POSTPHOTO";
    SCENE_NAME_FILTER    = "SCENE_NAME_FILTER";
    SCENE_NAME_DONE      = "SCENE_NAME_DONE";

    #Window Properties.
    _KEY_WINDOW_SIZE = "window_size";

    #Scenes Filenames.
    _KEY_SCENE_CAMERA_FILENAME    = "scene_camera_filename";
    _KEY_SCENE_POSTPHOTO_FILENAME = "scene_postphoto_filename";
    _KEY_SCENE_FILTER_FILENAME    = "scene_filter_filename";
    _KEY_SCENE_DONE_FILENAME      = "scene_done_filename";

    _REQUIRED_KEYS = [
        _KEY_WINDOW_SIZE,

        _KEY_SCENE_CAMERA_FILENAME,
        _KEY_SCENE_POSTPHOTO_FILENAME,
        _KEY_SCENE_FILTER_FILENAME,
        _KEY_SCENE_DONE_FILENAME,
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
        self._config_contents = None;

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
        config_info = config_validation.validate("SceneManager",
                                                  self._config_filename,
                                                  SceneManager._REQUIRED_KEYS);
        self._config_contents = DictHelper(config_info);

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
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE;
        self._screen_surface = pygame.display.set_mode(self.get_window_size(), flags);
        self._screen_surface.fill((0,0,0));


    ############################################################################
    ## Run                                                                    ##
    ############################################################################
    def run(self):
        Logger.instance().log_debug("SceneManager.run");

        #Set the app to running and start the clock.
        self._app_running = True;
        dt = self._app_clock.tick_busy_loop();

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
        dirty_rects = self._scene_current.draw(self._screen_surface);
        pygame.display.update(dirty_rects);


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
    def scene_is_complete(self, target_scene_name):
        #Camera.
        if(target_scene_name == SceneManager.SCENE_NAME_CAMERA):
            self._change_scene(self._get_scene_camera_instance());

        #PostPhoto.
        elif(target_scene_name == SceneManager.SCENE_NAME_POSTPHOTO):
            self._change_scene(self._get_scene_postphoto_instance());

        #Done.
        elif(target_scene_name == SceneManager.SCENE_NAME_DONE):
            self._change_scene(self._get_scene_done_instance());


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
        return self._config_contents.value_or_die(SceneManager._KEY_WINDOW_SIZE);

    #Scenes Filenames.
    def get_camera_scene_filename(self):
        return self._config_contents.value_or_die(SceneManager._KEY_SCENE_CAMERA_FILENAME);
    def get_postphoto_scene_filename(self):
        return self._config_contents.value_or_die(SceneManager._KEY_SCENE_POSTPHOTO_FILENAME);
    def get_filter_scene_filename(self):
        return self._config_contents.value_or_die(SceneManager._KEY_SCENE_FILTER_FILENAME);
    def get_done_scene_filename(self):
        return self._config_contents.value_or_die(SceneManager._KEY_SCENE_DONE_FILENAME);


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



