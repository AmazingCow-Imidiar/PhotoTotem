# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    base_scene.py                               ##
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
#Pygame
import pygame;
from logger import Logger;

################################################################################
## Sprite                                                                     ##
################################################################################
class Sprite(pygame.sprite.Sprite):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self, surface = None):
        pygame.sprite.Sprite.__init__(self);
        self.rect = pygame.rect.Rect(0,0,0,0);
        if(surface is not None):
            self.update_image(surface);

    ############################################################################
    ## Image Methods                                                          ##
    ############################################################################
    def load_image(self, filename):
        surface = pygame.image.load(filename);
        self.update_image(surface);

    def update_image(self, surface):
        self.image   = surface;
        self.rect[2] = self.image.get_width();
        self.rect[3] = self.image.get_height();

    ############################################################################
    ## Positions Setter/Getters                                               ##
    ############################################################################
    def set_position(self, pos):
        self.rect[0] = pos[0];
        self.rect[1] = pos[1];
    def get_position(self):
        return self.rect[0], self.rect[1];

    ############################################################################
    ## Size Setter/Getters                                                    ##
    ############################################################################
    def get_size(self):
        return self.rect[2], self.rect[3];
    def get_size_w(self):
        return self.rect[2];
    def get_size_h(self):
        return self.rect[3];



class Button(Sprite):
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        Sprite.__init__(self);
        #COWTODO: Remove.
        print "Button.__init__";

        ## iVars #
        self.__normal_surface  = None;
        self.__pressed_surface = None;

        self.__click_callback = None;


    ############################################################################
    ## Set Image Methods                                                      ##
    ############################################################################
    def load_images(self, normal_filename, pressed_filename):
        self.__normal_surface  = pygame.image.load(normal_filename);
        self.__pressed_surface = pygame.image.load(pressed_filename);

        self.reset();


    ############################################################################
    ## Callback Methods                                                       ##
    ############################################################################
    def set_click_callback(self, callback):
        self.__click_callback = callback;


    ############################################################################
    ## State Methods                                                          ##
    ############################################################################
    def reset(self):
        self.__set_normal_state();

    def __set_pressed_state(self):
        self.update_image(self.__pressed_surface);

    def __set_normal_state(self):
        self.update_image(self.__normal_surface);


    def handle_events(self, event):
        #Check which type of event and pass to handler.
        if(event.type == pygame.locals.MOUSEBUTTONDOWN):
            self.__onMouseButtonDown();
        elif(event.type == pygame.locals.MOUSEBUTTONUP):
            self.__onMouseButtonUp();
        elif(event.type == pygame.locals.MOUSEMOTION):
            self.__onMouseMotion();


    ############################################################################
    ## Mouse Events                                                           ##
    ############################################################################
    def __onMouseButtonDown(self):
        #COWTODO: Comment.
        pos = pygame.mouse.get_pos();
        if(self.rect.collidepoint(pos)):
            self.__set_pressed_state();

    def __onMouseButtonUp(self):
        #COWTODO: Comment.
        self.reset();
        pos = pygame.mouse.get_pos();
        if(self.rect.collidepoint(pos) and self.__click_callback is not None):
            self.__click_callback();

    def __onMouseMotion(self):
        #COWTODO: Comment.
        #COWTODO: Implement.
        pass;