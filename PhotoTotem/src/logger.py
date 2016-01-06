# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    logger.py                                   ##
##              █ █        █ █    Amazing Photo Totem                         ##
##               ████████████                                                 ##
##             █              █   Copyright (c) 2015, 2016 - AmazingCow       ##
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
    _LOG_FILE_PATH     = filesystem.canonical_path("~/Documents/AmazingPhotoTotem_LOG");
    _LOG_FILE_FILENAME = filesystem.canonical_path(
                _LOG_FILE_PATH,
                "RuntimeLog-{}.txt".format(time.ctime()).replace(" ", "_")
    );


    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    _instance = None;
    @staticmethod
    def instance():
        if(Logger._instance is None):
            Logger._instance = Logger();

        return Logger._instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #Check if the log dir/file is ok.
        self._check_dirs_and_files();


    ############################################################################
    ## Log Methods                                                            ##
    ############################################################################
    def log_debug(self, msg):
        self._log("[DEBUG]", msg);

    def log_fatal(self, msg):
        msg = str(msg);

        GUI().show_msg_box(msg);
        self._log("[FATAL]", msg);

        exit(1);

    def _log(self, *msg):
        #Build the message.
        msg = time.ctime() + " -- " + " ".join(map(str, msg));

        #Save to the log file.
        echo_cmd = "echo {} >> {}".format(self._escape_msg(msg),
                                          Logger._LOG_FILE_FILENAME);
        self._system_cmd(echo_cmd);

        #Print to screen.
        print msg;


    ############################################################################
    ## Other Methods                                                          ##
    ############################################################################
    def _check_dirs_and_files(self):
        #Check if log folder exists and create one if not.
        if(not os.path.isdir(Logger._LOG_FILE_PATH)):
            mkdir_cmd = "mkdir -p {}".format(Logger._LOG_FILE_PATH);
            self._system_cmd(mkdir_cmd);

        #Check if log file exists and create one if not.
        if(not os.path.isfile(Logger._LOG_FILE_FILENAME)):
            touch_cmd = "touch {}".format(Logger._LOG_FILE_FILENAME);
            self._system_cmd(touch_cmd);

    def _system_cmd(self, cmd):
        if(os.system(cmd) != 0):
            print cmd, "failed";

    def _escape_msg(self, msg):
        msg = msg.replace('"', '\"');
        return "\"{}\"".format(msg);
