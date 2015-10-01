# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    postphoto_scene.py                          ##
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
from widgets    import Sprite;
from widgets    import Button;
from clock      import BasicClock;
import scene_manager; #Not from ... import to avoid circular imports.
import config_validation;
import filesystem;

class PostPhotoScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    __REQUIRED_KEY_PHOTO_PLACEHOLDER_SPRITE = "photo_placeholder";
    __REQUIRED_KEY_ACCEPT_BUTTON            = "accept_button";
    __REQUIRED_KEY_REJECT_BUTTON            = "reject_button";
    __REQUIRED_KEY_STATIC_SPRITES           = "static_sprites";

    __REQUIRED_KEYS = [
        __REQUIRED_KEY_PHOTO_PLACEHOLDER_SPRITE,
        __REQUIRED_KEY_ACCEPT_BUTTON,
        __REQUIRED_KEY_REJECT_BUTTON,
        __REQUIRED_KEY_STATIC_SPRITES,
    ];

    #COWTODO: COMMENT.
    __LAYER_INDEX_STATIC_SPRITE = 1;
    __LAYER_INDEX_CAMERA_SPRITE = 2;
    __LAYER_INDEX_BUTTONS       = 3;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        BaseScene.__init__(self);

        #COWTODO: Remove it.
        print "PostPhotoScene.__init__";

        ## iVars ##
        #Filenames and Content.
        self.__config_filename = None;
        self.__file_contents   = None;

        #UI Elements.
        self.__accept_button = None;
        self.__reject_button = None;
        self.__photo_sprite  = None;

    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("PostPhotoScene.start");

        #Update the placeholder image to the last photo taken by camera.
        placeholder_size = self.__photo_sprite.get_size();
        last_photo = Camera.instance().get_last_photo(scale_to = placeholder_size);
        self.__photo_sprite.update_image(last_photo);

    def end(self):
        Logger.instance().log_debug("PostPhotoScene.end");

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("PostPhotoScene.init");
        self.__config_filename = scene_manager.SceneManager.instance().get_postphoto_scene_filename();

        #Validate the configuration.
        self.__file_contents = config_validation.validate("PostPhotoScene",
                                                          self.__config_filename,
                                                          PostPhotoScene.__REQUIRED_KEYS);
        #Init the UI.
        self.__init_static_sprites();
        self.__init_photo_sprite();
        self.__init_buttons();


    def __init_static_sprites(self):
        sprite_list = self.__file_contents[PostPhotoScene.__REQUIRED_KEY_STATIC_SPRITES];
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image(info["image"]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = PostPhotoScene.__LAYER_INDEX_STATIC_SPRITE);


    def __init_photo_sprite(self):
        #Get the info.
        info = self.__file_contents[PostPhotoScene.__REQUIRED_KEY_PHOTO_PLACEHOLDER_SPRITE];

        #Create the sprite.
        self.__photo_sprite = Sprite();

        #Set the sprite properties.
        self.__photo_sprite.load_image(info["image"]);
        self.__photo_sprite.set_position(info["position"]);

        #Add to scene.
        self.add(self.__photo_sprite,
                 layer = PostPhotoScene.__LAYER_INDEX_CAMERA_SPRITE);


    def __init_buttons(self):
        #Initialize the buttons.
        self.__accept_button = Button();
        self.__reject_button = Button();

        #Get the info.
        accept_info = self.__file_contents[PostPhotoScene.__REQUIRED_KEY_ACCEPT_BUTTON];
        reject_info = self.__file_contents[PostPhotoScene.__REQUIRED_KEY_REJECT_BUTTON];

        #Set the Accept Button properties.
        self.__accept_button.load_images(accept_info["normal_image"],
                                         accept_info["pressed_image"]);

        self.__accept_button.set_position(accept_info["position"]);

        self.__accept_button.set_click_callback(self.__on_accept_button_pressed);


        #Set the Reject Button properties.
        self.__reject_button.load_images(reject_info["normal_image"],
                                         reject_info["pressed_image"]);

        self.__reject_button.set_position(reject_info["position"]);

        self.__reject_button.set_click_callback(self.__on_reject_button_pressed);

        #Add them to scene.
        self.add(self.__accept_button,
                 layer = PostPhotoScene.__LAYER_INDEX_BUTTONS);
        self.add(self.__reject_button,
                 layer = PostPhotoScene.__LAYER_INDEX_BUTTONS);


    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def handle_events(self, event):
        self.__accept_button.handle_events(event);
        self.__reject_button.handle_events(event);


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def __on_accept_button_pressed(self):
        scene_manager.SceneManager.instance().scene_postphoto_complete(go_back=False);
        filesystem.save_photo(Camera.instance().get_last_photo(), None);

    def __on_reject_button_pressed(self):
        scene_manager.SceneManager.instance().scene_postphoto_complete(go_back=True);
