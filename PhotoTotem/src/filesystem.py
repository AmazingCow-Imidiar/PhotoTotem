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

## Imports ##
#Python
import os;
import os.path;
import time;
from multiprocessing import Process;
#Pygame
import pygame;
#Project
import config;
import logger;

################################################################################
## ???                                                                        ##
################################################################################
def canonical_path(*args):
    return os.path.abspath(os.path.expanduser(os.path.join(*args)));


def save_photo(image_to_save, use_another_thread = True):
    #Get the path that photo will be saved.
    out_path = config.Config.instance().get_image_output_path();

    #Canonize the the path...
    dir_path   = canonical_path(out_path);
    image_name = time.asctime().replace(" ", "_").replace(":", "_") + ".png";
    fullpath   = canonical_path(dir_path, image_name);

    logger.Logger.instance().log_debug("Filesystem.save_photo - {}".format(fullpath));

    #Create the diretory if it doesn't exists already.
    if(not os.path.isdir(dir_path)):
        msg = "Filesystem.save_photo - Directory doesn't exists... creating one now.";
        logger.Logger.instance().log_debug(msg)

        os.system("mkdir -p {}".format(dir_path));

    #Two of save... Fist one is in the main thread, blocking the UI.
    #The another one is saving in background...
    if(use_another_thread):
        p = Process(target = _save,
                    args   = (image_to_save, fullpath));
        p.start();
    else:
        _save(image_to_save, fullpath);

################################################################################
## Helper Methods                                                             ##
################################################################################
def _save(img, fullpath):
    pygame.image.save(img, fullpath);
