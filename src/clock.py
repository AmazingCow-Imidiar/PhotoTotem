# coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        clock.py                                  ##
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



