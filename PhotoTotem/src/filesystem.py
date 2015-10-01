# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    filesystem.py                               ##
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

import os;
import os.path;
import time;

import pygame;

from config import Config;
from camera import Camera;

def canonical_path(*args):
    return os.path.abspath(os.path.expanduser(os.path.join(*args)));

def save_photo(original_photo, frame_photo, use_another_thread = False):
    out_path = Config.instance().get_image_output_path();
    merge    = Config.instance().get_runtime_merge();

    dir_path   = canonical_path(out_path);
    image_name = time.asctime().replace(" ", "_").replace(":", "_") + ".png";
    fullpath   = canonical_path(dir_path, image_name);

    if(not os.path.isdir(dir_path)):
        os.system("mkdir -p {}".format(dir_path));

    pygame.image.save(original_photo, fullpath);
