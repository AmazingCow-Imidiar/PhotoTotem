# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    printer_manager.py                          ##
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

class PrinterManager(object):
    ############################################################################
    ## Constants                                                              ##
    ############################################################################

    ############################################################################
    ## Singleton                                                              ##
    ############################################################################
    _instance = None;
    @staticmethod
    def instance():
        if(PrinterManager._instance is None):
            PrinterManager._instance = PrinterManager();
        return PrinterManager._instance;


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        ## iVars ##
        self._print_job_done_callback = None;

    ############################################################################
    ## Init                                                                   ##
    ############################################################################
    def init(self):
        Logger.instance().log_debug("PrinterManager.init");


    ############################################################################
    ## Public Methods                                                         ##
    ############################################################################
    def print_photo(photo_filename, callback):
        msg = "PrinterManager.print_photo - {}".format(photo_filename);
        Logger.instance().log_debug(msg);

        #Set the callback.
        self._print_job_done_callback = callback;

        ##COWTODO: Print....

        #Check if anyone is listening that the print is done
        #and inform them the completion.
        #Set the callback as None to not hold any refs...
        if(self._print_job_done_callback is not None):
            self._print_job_done_callback();
            self._print_job_done_callback = None;
