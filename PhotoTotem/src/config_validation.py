# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    config_validation.py                        ##
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
