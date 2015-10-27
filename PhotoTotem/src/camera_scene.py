# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    camera_scene.py                             ##
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
import json;
#Pygame
import pygame;
#Project
import scene_manager;
import config_validation;
from   logger     import Logger;
from   camera     import Camera;
from   base_scene import BaseScene;
from   widgets    import Sprite;
from   widgets    import Button;
from   clock      import BasicClock;


class CameraScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE = "camera_placeholder";
    __REQUIRED_KEY_CAMERA_FRAME_SPRITE       = "camera_frame";
    __REQUIRED_KEY_TAKEPHOTO_BUTTON          = "take_photo";
    __REQUIRED_KEY_STATIC_SPRITES            = "static_sprites";
    __REQUIRED_KEY_COUNTDOWN_SPRITES         = "countdown";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE,
        __REQUIRED_KEY_CAMERA_FRAME_SPRITE,
        __REQUIRED_KEY_TAKEPHOTO_BUTTON,
        __REQUIRED_KEY_STATIC_SPRITES,
        __REQUIRED_KEY_COUNTDOWN_SPRITES,
    ];

    #How much time each countdown step will take (in ms).
    __COUNTDOWN_CLOCK_TIME = 10;

    #Layers.
    __LAYER_INDEX_STATIC_SPRITE    = 1;
    __LAYER_INDEX_CAMERA_SPRITE    = 2;
    __LAYER_INDEX_FRAME_SPRITE     = 3;
    __LAYER_INDEX_PHOTO_BUTTON     = 4;
    __LAYER_INDEX_COUNTDOWN_SPRITE = 5;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        ## iVars ##
        #Filenames and Content.
        self.__config_filename = None;
        self.__file_contents   = None;

        #UI Elements.
        self.__countdown_sprite  = None;
        self.__camera_sprite     = None;
        self.__frame_sprite      = None;
        self.__take_photo_button = None;

        #Countdown clock.
        self.__countdown_clock  = BasicClock(CameraScene.__COUNTDOWN_CLOCK_TIME,
                                             self.__on_countdown_timer_tick);

        self.__camera_sprite_size = None;


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
        self.__config_filename = scene_manager.SceneManager.instance().get_camera_scene_filename();

        #Validate the configuration.
        self.__file_contents = config_validation.validate("CameraScene",
                                                          self.__config_filename,
                                                          CameraScene.__REQUIRED_KEYS);
        #Init the UI.
        self.__init_static_sprites();
        self.__init_camera_sprite();
        self.__init_frame_sprite();
        self.__init_buttons();
        self.__init_countdown_sprite();


    def __init_static_sprites(self):
        sprite_list = self.__file_contents[CameraScene.__REQUIRED_KEY_STATIC_SPRITES];
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image(info["image"]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = CameraScene.__LAYER_INDEX_STATIC_SPRITE);


    def __init_camera_sprite(self):
        #Initialize the sprite.
        self.__camera_sprite = Sprite();

        #Get the info.
        info = self.__file_contents[CameraScene.__REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE];

        #Set the sprite properties.
        self.__camera_sprite.load_image(info["image"]);
        self.__camera_sprite.set_position(info["position"]);

        #Add to scene.
        self.add(self.__camera_sprite,
                 layer = CameraScene.__LAYER_INDEX_CAMERA_SPRITE);

        self.__camera_sprite_size = self.__camera_sprite.get_size();

    def __init_frame_sprite(self):
        #Get the info.
        info = self.__file_contents[CameraScene.__REQUIRED_KEY_CAMERA_FRAME_SPRITE];

        #Don't need the frame...
        if(info == False):
            return;

        #Init the sprite.
        self.__frame_sprite = Sprite();

        #Set the sprite properties.
        self.__frame_sprite.load_image(info["image"]);
        self.__frame_sprite.set_position(info["position"]);

        #Frame isn't same size of camera image, so scale it.
        if(self.__frame_sprite.get_size() != self.__camera_sprite_size):
            frame_image  = self.__frame_sprite.image;
            scaled_image = pygame.transform.scale(frame_image,
                                                  self.__camera_sprite_size);

            self.__frame_sprite.update_image(scaled_image);


        #Add to scene.
        self.add(self.__frame_sprite,
                 layer = CameraScene.__LAYER_INDEX_FRAME_SPRITE);


    def __init_buttons(self):
        #Initialize the button.
        self.__take_photo_button = Button();

        #Get the info.
        info = self.__file_contents[CameraScene.__REQUIRED_KEY_TAKEPHOTO_BUTTON];

        #Set the button properties.
        self.__take_photo_button.load_images(info["normal_image"],
                                             info["pressed_image"]);

        self.__take_photo_button.set_position(info["position"]);

        self.__take_photo_button.set_click_callback(self.__on_take_photo_button_pressed);

        #Add to scene.
        self.add(self.__take_photo_button,
                 layer = CameraScene.__LAYER_INDEX_PHOTO_BUTTON);


    def __init_countdown_sprite(self):
        #Initialize the Sprite.
        self.__countdown_sprite = Sprite();

        #Get the info.
        info = self.__file_contents[CameraScene.__REQUIRED_KEY_COUNTDOWN_SPRITES];

        #Set the sprite properties.
        self.__countdown_sprite.set_position(info["position"]);
        self.__countdown_sprite.load_image(info["sprites"][0]);    


    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        self.__countdown_clock.update(dt);
        img = Camera.instance().get_frame(scale_to = self.__camera_sprite_size);
        self.__camera_sprite.update_image(img);

    def handle_events(self, event):
        self.__take_photo_button.handle_events(event);


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def __on_take_photo_button_pressed(self):
        #Set the UI Elements visibility.
        self.remove(self.__take_photo_button);
        self.add(self.__countdown_sprite,
                 layer = CameraScene.__LAYER_INDEX_COUNTDOWN_SPRITE);

        #Start the countdown...
        self.__countdown_clock.start();


    ############################################################################
    ## Timer Callbacks                                                        ##
    ############################################################################
    def __on_countdown_timer_tick(self):
        #Get the info.
        info = self.__file_contents[CameraScene.__REQUIRED_KEY_COUNTDOWN_SPRITES];

        sprites_list = info["sprites"];
        index        = self.__countdown_clock.get_ticks_count();

        #Check if have more countdown images to show...
        if(index < len(sprites_list)):
            self.__countdown_sprite.load_image(sprites_list[index]);
        else:
            #Reset the image to the first frame and inform that
            #the countdown is done.
            self.__countdown_sprite.load_image(sprites_list[0]);
            self.__countdown_timer_finished();


    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def __countdown_timer_finished(self):
        #Set the UI Elements visibility.
        self.remove(self.__countdown_sprite);
        self.add(self.__take_photo_button,
                 layer = CameraScene.__LAYER_INDEX_PHOTO_BUTTON);

        #Stop the countdown...
        self.__countdown_clock.stop();

        #Call the Camera to grab a photo.
        Camera.instance().take_photo();

        #Go to another scene.
        scene_manager.SceneManager.instance().scene_camera_complete();
