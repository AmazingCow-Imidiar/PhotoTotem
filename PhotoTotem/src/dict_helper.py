# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    config_validation.py                        ##
##              █ █        █ █    Amazing Photo Totem                         ##
##               ████████████                                                 ##
##             █              █   Copyright (c) 2016 - AmazingCow             ##
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
#Project
import logger;


class DictHelper:
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, d):
        self._d = d;

    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def value_or_none(self, key):
        if(key in self._d.keys()):
            return self._d[key];
        return None;

    def value_or_die(self, key):
        if(key in self._d.keys()):
            return self._d[key];

        msg = "Key not found: {}\n dump:{}".format(key, self._d);
        logger.Logger.instance().log_fatal(msg);
        exit(0);
