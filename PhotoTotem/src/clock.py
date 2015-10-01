# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    clock.py                                    ##
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


class BasicClock(object):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, time, tick_callback = None):

        ## iVars ##
        self.__tick_time            = time;
        self.__time_since_last_tick = None;
        self.__enabled              = False;
        self.__ticks_count          = 0;
        self.__tick_callback        = tick_callback;


    ############################################################################
    ## Set/Get Time                                                           ##
    ############################################################################
    def set_time(self, time):
        self.__time_since_last_tick = 0;
        self.__tick_time            = time;

    def get_time(self):
        return self.__tick_time;

    ############################################################################
    ## Start/Stop/Enabled                                                     ##
    ############################################################################
    def start(self):
        self.__enabled              = True;
        self.__time_since_last_tick = 0;
        self.__ticks_count          = 0;

    def stop(self):
        self.__enabled = False;

    def is_enabled(self):
        return self.__enabled;


    ############################################################################
    ## Ticks Count                                                            ##
    ############################################################################
    def get_ticks_count(self):
        return self.__ticks_count;


    ############################################################################
    ## Set/Get Callback                                                       ##
    ############################################################################
    def set_callback(self, callback):
        self.__tick_callback = callback;

    def get_callback(self):
        return self.__tick_callback;


    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        if(not self.__enabled):
            return;

        #Update the timer...
        self.__time_since_last_tick += dt;
        if(self.__time_since_last_tick >= self.__tick_time):
            self.__time_since_last_tick -= self.__tick_time;

            #Update the ticks count.
            self.__ticks_count += 1;

            #We have a valid callback?
            assert self.__tick_callback is not None;
            self.__tick_callback();



