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
#Project
from logger     import Logger;
from camera     import Camera;
from base_scene import BaseScene;
from button     import Button;
from sprite     import Sprite;
import scene_manager; #Not from ... import to avoid circular imports.

class CameraScene(BaseScene):
     ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE = "camera_placeholder";
    __REQUIRED_KEY_TAKEPHOTO_BUTTON          = "take_photo";
    __REQUIRED_KEY_STATIC_SPRITES            = "static_sprites";
    __REQUIRED_KEY_COUNTDOWN_SPRITES         = "countdown";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE,
        __REQUIRED_KEY_TAKEPHOTO_BUTTON,
        __REQUIRED_KEY_STATIC_SPRITES,
        __REQUIRED_KEY_COUNTDOWN_SPRITES,
    ];

    __ONE_SECOND_IN_MS = 1000;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);
        #COWTODO: Remove it.
        print "CameraScene.__init__";

        ## iVars ##
        #Filenames and Content.
        self.__config_filename = None;
        self.__file_contents   = None;
        self.__countdown_sprite_filenames = None;

        #UI Elements.
        self.__static_sprites           = None;
        self.__take_photo_button        = None;
        self.__camera_placehoder_sprite = None;
        self.__countdown_sprite         = None;

        #Countdown
        self.__time_since_last_countdown_tick = None;
        self.__is_running_countdown           = None;
        self.__current_countdown_index        = None;
        self.__countdown_index_count          = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("CameraScene.init");
        self.__config_filename = scene_manager.SceneManager.instance().get_camera_scene_filename();

        #Validate the configuration.
        self.__validate_config_file();

        #Init the UI.
        self.__init_static_sprites();
        self.__init_camera_sprite();
        self.__init_buttons();
        self.__init_countdown_sprite();

        #Init the clock.
        self.__time_since_last_countdown_tick = 0;
        self.__is_running_countdown           = False;

    def __init_static_sprites(self):
        #Initialize the list.
        self.__static_sprites = [];

        l = self.__file_contents[CameraScene.__REQUIRED_KEY_STATIC_SPRITES];
        for sprite_info in l:
            #Get the info.
            pos = sprite_info["position"];
            fn  = sprite_info["image"];
            #Create the sprite.
            sprite = Sprite();
            sprite.set_image_filename(fn);
            sprite.set_position(pos[0], pos[1]);
            #Add them to list.
            self.__static_sprites.append(sprite);

    def __init_camera_sprite(self):
        #Initialize the sprite.
        self.__camera_placehoder_sprite = Sprite();
        #Get the info.
        sprite_info = self.__file_contents[CameraScene.__REQUIRED_KEY_CAMERA_PLACEHOLDER_SPRITE];
        pos         = sprite_info["position"];
        filename    = sprite_info["image"];
        #Set the sprite properties.
        self.__camera_placehoder_sprite.set_image_filename(filename);
        self.__camera_placehoder_sprite.set_position(pos[0],pos[1]);

    def __init_buttons(self):
        #Initialize the button.
        self.__take_photo_button = Button();
        #Get the info.
        button_info   = self.__file_contents[CameraScene.__REQUIRED_KEY_TAKEPHOTO_BUTTON];
        pos           = button_info["position"];
        normal_image  = button_info["normal_image"];
        pressed_image = button_info["pressed_image"];
        #Set the button properties.
        self.__take_photo_button.set_sprite_filenames(normal_image, pressed_image);
        self.__take_photo_button.set_position(pos[0], pos[1]);
        #Set the button callback.
        self.__take_photo_button.set_click_callback(self.__on_take_photo_button_pressed);

    def __init_countdown_sprite(self):
        #Init the list of filenames.
        self.__countdown_sprite_filenames = [];
        #Initialize the Sprite.
        self.__countdown_sprite = Sprite();
        #Get the info.
        countdown_info = self.__file_contents[CameraScene.__REQUIRED_KEY_COUNTDOWN_SPRITES];
        pos            = countdown_info["position"];
        for filename in countdown_info["sprites"]:
            self.__countdown_sprite_filenames.append(filename);
        #Set the button properties.
        self.__countdown_sprite.set_image_filename(self.__countdown_sprite_filenames[0]);
        self.__countdown_sprite.set_position(pos[0], pos[1]);
        #Set the other countdown properties.
        self.__current_countdown_index = 0;
        self.__countdown_index_count   = len(self.__countdown_sprite_filenames);

    ############################################################################
    ## Update / Draw / Handle Events Methods                                  ##
    ############################################################################
    def update(self, dt):
        if(not self.__is_running_countdown):
            return;

        self.__time_since_last_countdown_tick += dt;

        if(self.__time_since_last_countdown_tick >= CameraScene.__ONE_SECOND_IN_MS):
            self.__time_since_last_countdown_tick -= CameraScene.__ONE_SECOND_IN_MS;

            self.__current_countdown_index += 1;
            if(self.__current_countdown_index < self.__countdown_index_count):
                filename = self.__countdown_sprite_filenames[self.__current_countdown_index];
                self.__countdown_sprite.set_image_filename(filename);
            else:
                self.__countdown_time_finished();


    def draw(self, surface):
        #Static Sprites.
        for static_sprite in self.__static_sprites:
            static_sprite.draw(surface);
        #Take Photo Button.
        self.__take_photo_button.draw(surface);
        #Camera Image.
        placeholder_pos  = self.__camera_placehoder_sprite.get_position();
        placeholder_size = self.__camera_placehoder_sprite.get_size();
        frame            = Camera.instance().get_frame(placeholder_size);
        surface.blit(frame, placeholder_pos);
        #Countdown Sprite.
        self.__countdown_sprite.draw(surface);

    def handle_events(self, event):
        self.__take_photo_button.handle_events(event);

    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def __on_take_photo_button_pressed(self):
        #Set the UI Elements visibility.
        self.__countdown_sprite.set_visible(True);
        self.__take_photo_button.set_visible(False);
        #Set the now countdown is running.
        self.__is_running_countdown = True;

    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def __countdown_time_finished(self):
        #Set the UI Elements visibility.
        self.__countdown_sprite.set_visible(False);
        self.__take_photo_button.set_visible(True);
        #Set the now countdown not is running.
        self.__is_running_countdown = True;

        #Call the Camera to grab a photo.
        Camera.instance().take_photo();


    ############################################################################
    ## Validation Methods                                                     ##
    ############################################################################
    def __validate_config_file(self):
        Logger.instance().log_debug("CameraScene.validate_config_file");

        #Just to ease the typing.
        filename = self.__config_filename;

        #Check if filename is valid.
        #Empty.
        if(len(filename) == 0):
            Logger.instance().log_fatal("CameraScene Configuration Filename is empty.");
        #Not a valid file path.
        if(not os.path.isfile(filename)):
            msg = "CameraScene Configuration Filename ({}) is invalid.".format(filename);
            Logger.instance().log_fatal(msg);

        #Check if is a valid json.
        try:
            self.__file_contents = json.load(open(filename));
        except Exception, e:
            msg = "{} ({}) {}.".format("CameraScene Configuration File",
                                       filename,
                                       "isn't a valid json file.");
            Logger.instance().log_fatal(msg);


        #Check if file has the required keys.
        for key in CameraScene.__REQUIRED_KEYS:
            if(key not in self.__file_contents):
                msg = "{} ({}) {} ({})".format("CameraScene Configuration File",
                                               filename,
                                               "doesn't have required key",
                                               key);
                Logger.instance().log_fatal(msg);

