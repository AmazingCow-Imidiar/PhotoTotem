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
#Python
import os;
from multiprocessing import Process;
#Project
from   logger      import Logger;

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
    def print_photo(self, photo_filename, callback):
        msg = "PrinterManager.print_photo - {}".format(photo_filename);
        Logger.instance().log_debug(msg);

        ##COWTODO: Print....
        p = Process(target = self._print,
                    args   = (photo_filename, callback));
        p.start();

    ##
    def _print(self, photo_filename, callback):
        #Check if anyone is listening that the print is done
        #and inform them the completion.
        #Set the callback as None to not hold any refs...
        print "PRINTING... ", photo_filename;
        os.system("ls -1 /home/n2omatt/Documents/Projects/AmazingCow/Proprietary/CuteQuotes/CuteQuotes/programs/favq_fetcher/quotes_download");
        os.system("ls -1 /home/n2omatt/Documents/Projects/AmazingCow/Proprietary/CuteQuotes/CuteQuotes/programs/favq_fetcher/quotes_download");
        os.system("ls -1 /home/n2omatt/Documents/Projects/AmazingCow/Proprietary/CuteQuotes/CuteQuotes/programs/favq_fetcher/quotes_download");

        callback();
