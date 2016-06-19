# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        postphoto_scene.py                        ##
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
import json;
import time;
#Pygame
import pygame;
#Project
import scene_manager;
import config_validation;
import filesystem;
from   logger      import Logger;
from   camera      import Camera;
from   base_scene  import BaseScene;
from   widgets     import Sprite;
from   widgets     import Button;
from   clock       import BasicClock;
from   dict_helper import DictHelper;

class PostPhotoScene(BaseScene):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Required Keys.
    _KEY_PHOTO_PLACEHOLDER_SPRITE = "photo_placeholder";
    _KEY_PHOTO_FRAME_SPRITE       = "photo_frame";
    _KEY_STATIC_SPRITES           = "static_sprites";

    _KEY_ACCEPT_BUTTON = "accept_button";
    _KEY_REJECT_BUTTON = "reject_button";

    _REQUIRED_KEYS = [
        _KEY_PHOTO_PLACEHOLDER_SPRITE,
        _KEY_PHOTO_FRAME_SPRITE,
        _KEY_STATIC_SPRITES,

        _KEY_ACCEPT_BUTTON,
        _KEY_REJECT_BUTTON,
    ];

    #Layers.
    _LAYER_INDEX_STATIC_SPRITE = 1;
    _LAYER_INDEX_CAMERA_SPRITE = 2;
    _LAYER_INDEX_FRAME_SPRITE  = 3;
    _LAYER_INDEX_BUTTONS       = 4;


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
        self._accept_button = None;
        self._reject_button = None;

        self._photo_sprite  = None;
        self._frame_sprite  = None;


    ############################################################################
    ## Overriden Methods                                                      ##
    ############################################################################
    def start(self):
        Logger.instance().log_debug("PostPhotoScene.start");

        #Update the placeholder image to the last photo taken by camera.
        placeholder_size = self._photo_sprite.get_size();
        last_photo = Camera.instance().get_last_photo(scale_to = placeholder_size);
        self._photo_sprite.update_image(last_photo);

    def end(self):
        Logger.instance().log_debug("PostPhotoScene.end");


    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("PostPhotoScene.init");
        self._config_filename = scene_manager.SceneManager.instance().get_postphoto_scene_filename();

        #Validate the configuration.
        config_info = config_validation.validate("PostPhotoScene",
                                                 self._config_filename,
                                                 PostPhotoScene._REQUIRED_KEYS);
        self._config_contents = DictHelper(config_info);

        #Init the UI.
        self._init_static_sprites();
        self._init_photo_sprite();
        self._init_frame_sprite();
        self._init_buttons();


    def _init_static_sprites(self):
        sprite_list = self._config_contents.value_or_die(PostPhotoScene._KEY_STATIC_SPRITES);
        for info in sprite_list:
            #Create the sprite.
            sprite = Sprite();

            #Set the sprite properties.
            sprite.load_image  (info["image"   ]);
            sprite.set_position(info["position"]);

            #Add to scene.
            self.add(sprite, layer = PostPhotoScene._LAYER_INDEX_STATIC_SPRITE);

    def _init_photo_sprite(self):
        #Get the info.
        info = self._config_contents.value_or_die(PostPhotoScene._KEY_PHOTO_PLACEHOLDER_SPRITE);

        #Create the sprite.
        self._photo_sprite = Sprite();

        #Set the sprite properties.
        self._photo_sprite.load_image  (info["image"  ]);
        self._photo_sprite.set_position(info["position"]);

        #Add to scene.
        self.add(self._photo_sprite,
                 layer = PostPhotoScene._LAYER_INDEX_CAMERA_SPRITE);

    def _init_frame_sprite(self):
        #Get the info.
        info = self._config_contents.value_or_die(PostPhotoScene._KEY_PHOTO_FRAME_SPRITE);

        #Don't need the frame...
        if(info == False):
            return;

        #Init the sprite.
        self._frame_sprite = Sprite();

        #Set the sprite properties.
        self._frame_sprite.load_image  (info["image"   ]);
        self._frame_sprite.set_position(info["position"]);

        #Frame isn't same size of camera image, so scale it.
        photo_sprite_size = self._photo_sprite.get_size();
        if(self._frame_sprite.get_size() != photo_sprite_size):
            frame_image  = self._frame_sprite.image;
            scaled_image = pygame.transform.scale(frame_image,
                                                  photo_sprite_size);

            self._frame_sprite.update_image(scaled_image);

        #Add to scene.
        self.add(self._frame_sprite,
                 layer = PostPhotoScene._LAYER_INDEX_FRAME_SPRITE);

    def _init_buttons(self):
        ## Initialize the Accept and Reject Buttons. ##
        #Get the infos.
        accept_info = self._config_contents.value_or_die(PostPhotoScene._KEY_ACCEPT_BUTTON);
        reject_info = self._config_contents.value_or_die(PostPhotoScene._KEY_REJECT_BUTTON);

        #Initialize the buttons.
        self._accept_button = self._create_button_helper(accept_info,
                                                         self._on_accept_button_pressed);

        self._reject_button = self._create_button_helper(reject_info,
                                                         self._on_reject_button_pressed);


    def _create_button_helper(self, info, callback):
        button = Button();

        #Images.
        button.load_images(info["normal_image"],
                           info["pressed_image"]);
        #Position.
        button.set_position(info["position"]);
        #Callback.
        button.set_click_callback(callback);

        #Add to scene.
        self.add(button, layer = PostPhotoScene._LAYER_INDEX_BUTTONS);

        return button;

    ############################################################################
    ## Update / Draw / Handle Events                                          ##
    ############################################################################
    def handle_events(self, event):
        #Those buttons are *always* present.
        self._accept_button.handle_events(event);
        self._reject_button.handle_events(event);


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def _on_accept_button_pressed(self):
        self._save_photo_on_disk();

        #Change to other scene.
        self._change_scene(scene_manager.SceneManager.SCENE_NAME_DONE);

    def _on_reject_button_pressed(self):
        self._change_scene(scene_manager.SceneManager.SCENE_NAME_CAMERA);


    ############################################################################
    ## Helper Methods                                                         ##
    ############################################################################
    def _change_scene(self, scene_name):
        scene_manager.SceneManager.instance().scene_is_complete(target_scene_name=scene_name);

    def _save_photo_on_disk(self):
        #Save the photo on disk...
        filesystem.save_photo(Camera.instance().get_last_photo(),
                              use_another_thread = True);

