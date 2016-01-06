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
        self._tick_time            = time;
        self._time_since_last_tick = None;
        self._enabled              = False;
        self._ticks_count          = 0;
        self._tick_callback        = tick_callback;


    ############################################################################
    ## Set/Get Time                                                           ##
    ############################################################################
    def set_time(self, time):
        self._time_since_last_tick = 0;
        self._tick_time            = time;

    def get_time(self):
        return self._tick_time;


    ############################################################################
    ## Start/Stop/Enabled                                                     ##
    ############################################################################
    def start(self):
        self._enabled              = True;
        self._time_since_last_tick = 0;
        self._ticks_count          = 0;

    def stop(self):
        self._enabled = False;

    def is_enabled(self):
        return self._enabled;


    ############################################################################
    ## Ticks Count                                                            ##
    ############################################################################
    def get_ticks_count(self):
        return self._ticks_count;


    ############################################################################
    ## Set/Get Callback                                                       ##
    ############################################################################
    def set_callback(self, callback):
        self._tick_callback = callback;

    def get_callback(self):
        return self._tick_callback;


    ############################################################################
    ## Update                                                                 ##
    ############################################################################
    def update(self, dt):
        if(not self._enabled):
            return;

        #Update the timer...
        self._time_since_last_tick += dt;
        if(self._time_since_last_tick >= self._tick_time):
            self._time_since_last_tick -= self._tick_time;

            #Update the ticks count.
            self._ticks_count += 1;

            #We have a valid callback?
            assert self._tick_callback is not None;
            self._tick_callback();



