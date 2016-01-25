# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    camera_scene.py                             ##
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
import json;
import pdb;
#Pygame
import pygame;
#Project
import scene_manager;
import config_validation;
from   logger      import Logger;
from   camera      import Camera;
from   base_scene  import BaseScene;
from   widgets     import Sprite;
from   widgets     import Button;
from   clock       import BasicClock;
from   dict_helper import DictHelper;


class CameraScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    _KEY_CAMERA_PLACEHOLDER_SPRITE = "camera_placeholder";
    _KEY_CAMERA_FRAME_SPRITE       = "camera_frame";
    _KEY_TAKEPHOTO_BUTTON          = "take_photo";
    _KEY_STATIC_SPRITES            = "static_sprites";
    _KEY_COUNTDOWN_SPRITES         = "countdown";

    _REQUIRED_KEYS = [
        _KEY_CAMERA_PLACEHOLDER_SPRITE,
        _KEY_CAMERA_FRAME_SPRITE,
        _KEY_TAKEPHOTO_BUTTON,
        _KEY_STATIC_SPRITES,
        _KEY_COUNTDOWN_SPRITES,
    ];

    #How much time each countdown step will take (in ms).
    _COUNTDOWN_CLOCK_TIME = 10;

    #Layers.
    _LAYER_INDEX_STATIC_SPRITE    = 1;
    _LAYER_INDEX_CAMERA_SPRITE    = 2;
    _LAYER_INDEX_FRAME_SPRITE     = 3;
    _LAYER_INDEX_PHOTO_BUTTON     = 4;
    _LAYER_INDEX_COUNTDOWN_SPRITE = 5;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        ## iVars ##
        #Filenames and Content.
        self._config_filename = None;
        self._config_contents = None;

        #UI Elements.
        self._countdown_sprite  = None;
        self._camera_sprite     = None;
        self._frame_sprite      = None;
        self._take_photo_button = None;

        #Countdown clock.
        self._countdown_clock = BasicClock(CameraScene._COUNTDOWN_CLOCK_TIME,
                                           self._on_countdown_timer_tick);

        self._camera_sprite_size = None;


    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("CameraScene.start");

    def end(self):
        Logger.instance().log_debug("CameraScene.end");


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("CameraScene.init");
        self._config_filename = scene_manager.SceneManager.instance().get_camera_scene_filename();

        #Validate the configuration.
        config_dict = config_validation.validate("CameraScene",
                                                 self._config_filename,
                                                 CameraScene._REQUIRED_KEYS);
        self._config_contents = DictHelper(config_dict);


        #Init the UI.
        self._init_static_sprites();
        self._init_camera_sprite();
        self._init_frame_sprite();
        self._init_buttons();
        self._init_countdown_sprite();


    def _init_static_sprites(self):
        sprite_list = self._config_contents.value_or_die(CameraScene._KEY_STATIC_SPRITES);
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image  (info["image"   ]);
            sprite.set_position(info["position"]);

            self._background_sprite = sprite;
            #Add to scene.
            self.add(sprite, layer = CameraScene._LAYER_INDEX_STATIC_SPRITE);

    def _init_camera_sprite(self):
        #Initialize the sprite.
        self._camera_sprite = Sprite();

        #Get the info.
        info = self._config_contents.value_or_die(CameraScene._KEY_CAMERA_PLACEHOLDER_SPRITE);

        #Set the sprite properties.
        self._camera_sprite.load_image  (info["image"   ]);
        self._camera_sprite.set_position(info["position"]);

        #Add to scene.
        self.add(self._camera_sprite,
                 layer = CameraScene._LAYER_INDEX_CAMERA_SPRITE);

        self._camera_sprite_size = self._camera_sprite.get_size();

    def _init_frame_sprite(self):
        #Get the info.
        info = self._config_contents.value_or_die(CameraScene._KEY_CAMERA_FRAME_SPRITE);

        #Don't need the frame...
        if(info == False):
            return;

        #Init the sprite.
        self._frame_sprite = Sprite();

        #Set the sprite properties.
        self._frame_sprite.load_image(info["image"]);
        self._frame_sprite.set_position(info["position"]);

        #Frame isn't same size of camera image, so scale it.
        if(self._frame_sprite.get_size() != self._camera_sprite_size):
            frame_image  = self._frame_sprite.image;
            scaled_image = pygame.transform.scale(frame_image,
                                                  self._camera_sprite_size);

            self._frame_sprite.update_image(scaled_image);


        #Add to scene.
        self.add(self._frame_sprite,
                 layer = CameraScene._LAYER_INDEX_FRAME_SPRITE);

    def _init_buttons(self):
        #Initialize the button.
        self._take_photo_button = Button();

        #Get the info.
        info = self._config_contents.value_or_die(CameraScene._KEY_TAKEPHOTO_BUTTON);

        #Set the button properties.
        self._take_photo_button.load_images(info["normal_image"],
                                            info["pressed_image"]);

        self._take_photo_button.set_position(info["position"]);

        self._take_photo_button.set_click_callback(self._on_take_photo_button_pressed);

        #Add to scene.
        self.add(self._take_photo_button,
                 layer = CameraScene._LAYER_INDEX_PHOTO_BUTTON);

    def _init_countdown_sprite(self):
        #Initialize the Sprite.
        self._countdown_sprite = Sprite();

        #Get the info.
        info = self._config_contents.value_or_die(CameraScene._KEY_COUNTDOWN_SPRITES);

        #Set the sprite properties.
        self._countdown_sprite.set_position(info["position"]);
        self._countdown_sprite.load_image(info["sprites"][0]);

        #Countdown is hidden by default.


    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        self._countdown_clock.update(dt);
        img = Camera.instance().get_frame(scale_to = self._camera_sprite_size);
        self._camera_sprite.update_image(img);

    def handle_events(self, event):
        self._take_photo_button.handle_events(event);


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def _on_take_photo_button_pressed(self):
        #Set the UI Elements visibility.
        self.remove(self._take_photo_button);
        self.add(self._countdown_sprite,
                 layer = CameraScene._LAYER_INDEX_COUNTDOWN_SPRITE);

        #Start the countdown...
        self._countdown_clock.start();


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def _on_countdown_timer_tick(self):
        #Get the info.
        info = self._config_contents.value_or_die(CameraScene._KEY_COUNTDOWN_SPRITES);

        sprites_list = info["sprites"];
        index        = self._countdown_clock.get_ticks_count();

        #Check if have more countdown images to show...
        if(index < len(sprites_list)):
            self._countdown_sprite.load_image(sprites_list[index]);
        else:
            #Reset the image to the first frame and inform that
            #the countdown is done.
            self._countdown_sprite.load_image(sprites_list[0]);
            self._countdown_timer_finished();


    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def _countdown_timer_finished(self):
        #Set the UI Elements visibility.
        self.remove(self._countdown_sprite);
        self.add(self._take_photo_button,
                 layer = CameraScene._LAYER_INDEX_PHOTO_BUTTON);

        #Stop the countdown...
        self._countdown_clock.stop();

        #Call the Camera to grab a photo.
        Camera.instance().take_photo();

        #Go to another scene.
        scene_mgr = scene_manager.SceneManager;
        scene_mgr.instance().scene_is_complete(scene_mgr.SCENE_NAME_POSTPHOTO);
