# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        config_validation.py                      ##
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
import os.path;
import sys;
import json;
#Project
from logger import Logger;


################################################################################
## Validation Methods                                                         ##
################################################################################
def validate(name, filename, required_keys):
    Logger.instance().log_debug("config_validation.validate [{}]".format(name));

    #Check if filename is valid.
    #Empty.
    if(filename is None or len(filename) == 0):
        msg = _build_str(name, "Configuration Filename is empty.");
        Logger.instance().log_fatal(msg);

    #Not a valid file path.
    if(not os.path.isfile(filename)):
        msg = _build_str(name, "Configuration filename is invalid.",
                         "Filename: ({})".format(filename));
        Logger.instance().log_fatal(msg);

    #Check if is a valid json.
    try:
        file_contents = json.load(open(filename));
    except Exception, e:
        msg = _build_str(name, "Configuration file isn't a valid json.",
                         "Filename: ({})".format(filename),
                         "Exception: ({})".format(str(e)));
        Logger.instance().log_fatal(msg);


    #Check if file has the required keys.
    for key in required_keys:
        if(key not in file_contents):
            msg = _build_str(name, "Configuration file doesn't have required key.",
                             "Key: ({})".format(key),
                             "Filename: ({})".format(filename));
            Logger.instance().log_fatal(msg);

    return file_contents;


################################################################################
## Helper Methods                                                             ##
################################################################################
def _build_str(name, *args):
    msg = "[" + name + "]" + " - ";
    msg += " ".join(map(str, args));
    return msg;
