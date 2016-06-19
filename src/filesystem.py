# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        filesystem.py                             ##
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
