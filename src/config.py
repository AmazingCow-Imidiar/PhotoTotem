# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        config.py                                 ##
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
import getopt;
import sys;
#Project
import config_validation;
from   gui         import GUI;
from   logger      import Logger;
from   dict_helper import DictHelper;


class Config(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    #Flags.
    _FLAG_CONFIG       = "config";
    _FLAG_DUMMY_CAMERA = "dummy-camera"

    _ALL_FLAGS_SHORT = "";
    _ALL_FLAGS_LONG  = [
        _FLAG_CONFIG + "=",
        _FLAG_DUMMY_CAMERA
    ];

    #Required keys.
    _KEY_CAMERA_FILENAME       = "camera_config_filename";
    _KEY_SCENEMANAGER_FILENAME = "scene_manager_config_filename";
    _KEY_PHOTO_OUTPUT_FOLDER   = "image_output_folder";
    _KEY_RUNTIME_PHOTO_MERGE   = "runtime_photo_merge";

    _REQUIRED_KEYS = [
        _KEY_CAMERA_FILENAME,
        _KEY_SCENEMANAGER_FILENAME,
        _KEY_PHOTO_OUTPUT_FOLDER,
        _KEY_RUNTIME_PHOTO_MERGE,
    ];


    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    _instance = None;
    @staticmethod
    def instance():
        if(Config._instance is None):
            Config._instance = Config();

        return Config._instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        ## iVars ##
        self._config_filename = None;
        self._config_contents  = None;
        self._dummy_camera    = False;


    ############################################################################
    ## Init Method                                                            ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("Config.init");

        #Try to get the command line options.
        try:
            options = getopt.gnu_getopt(sys.argv[1:],
                                        Config._ALL_FLAGS_SHORT,
                                        Config._ALL_FLAGS_LONG);
        except Exception, e:
            Logger.instance().log_fatal(e);

        #Parse the options.
        for option in options[0]:
            key, value = option;
            key = key.lstrip("-");

            #Configuration filename.
            if(key in Config._FLAG_CONFIG):
                self._config_filename = value;
            #Use dummy camera.
            elif(key in Config._FLAG_DUMMY_CAMERA):
                self._dummy_camera = True;

        #Check if file is valid.
        config_info = config_validation.validate("Config",
                                                 self._config_filename,
                                                 Config._REQUIRED_KEYS);

        self._config_contents = DictHelper(config_info);


    ############################################################################
    ## Getters                                                                ##
    ############################################################################
    def get_camera_config_filename(self):
        return self._config_contents.value_or_die(Config._KEY_CAMERA_FILENAME);

    def get_dummy_camera(self):
        return self._dummy_camera;

    def get_scene_manager_config_filename(self):
        return self._config_contents.value_or_die(Config._KEY_SCENEMANAGER_FILENAME);

    def get_image_output_path(self):
        return self._config_contents.value_or_die(Config._KEY_PHOTO_OUTPUT_FOLDER);

    def get_runtime_merge(self):
        return self._config_contents.value_or_die(Config._KEY_RUNTIME_PHOTO_MERGE);

