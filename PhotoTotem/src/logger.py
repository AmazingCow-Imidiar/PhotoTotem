# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    logger.py                                   ##
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
#Project
import filesystem;
from   gui import GUI;

class Logger(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################
    __LOG_FILE_PATH     = filesystem.canonical_path("~/Documents/AmazingPhotoTotem_LOG");
    __LOG_FILE_FILENAME = filesystem.canonical_path(
                __LOG_FILE_PATH,
                "RuntimeLog-{}.txt".format(time.ctime()).replace(" ", "_")
    );

   ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    __instance = None;
    @staticmethod
    def instance():
        if(Logger.__instance is None):
            Logger.__instance = Logger();

        return Logger.__instance;

    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Remove
        print "Logger.__init__";

        #Check if the log dir/file is ok.
        self.__check_dirs_and_files();


    ############################################################################
    ## Log Methods                                                            ##
    ############################################################################
    def log_debug(self, msg):
        self.__log("[DEBUG]", msg);

    def log_fatal(self, msg):
        msg = str(msg);

        GUI().show_msg_box(msg);
        self.__log("[FATAL]", msg);

        exit(1);

    def __log(self, *msg):
        msg = time.ctime() + " -- " + " ".join(map(str, msg));
        echo_cmd = "echo {} >> {}".format(self.__escape_msg(msg),
                                          Logger.__LOG_FILE_FILENAME);
        self.__system_cmd(echo_cmd);


    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def __check_dirs_and_files(self):
        #Check if log folder exists and create one if not.
        if(not os.path.isdir(Logger.__LOG_FILE_PATH)):
            mkdir_cmd = "mkdir -p {}".format(Logger.__LOG_FILE_PATH);
            self.__system_cmd(mkdir_cmd);

        #Check if log file exists and create one if not.
        if(not os.path.isfile(Logger.__LOG_FILE_FILENAME)):
            touch_cmd = "touch {}".format(Logger.__LOG_FILE_FILENAME);
            self.__system_cmd(touch_cmd);

    def __system_cmd(self, cmd):
        if(os.system(cmd) != 0):
            print cmd, "failed";

    def __escape_msg(self, msg):
        msg = msg.replace('"', '\"');
        return "\"{}\"".format(msg);
