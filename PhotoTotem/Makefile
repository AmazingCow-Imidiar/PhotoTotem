##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    Makefile 			                          ##
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

#Where the Photo Totem will be installed.
DST_DIR=~/Desktop/PhotoTotem

install:
	@ echo " - Amazing Photo Totem Installer - "

	@ #Remove old installations...
	@ rm -rf $(DST_DIR);

	@ #Copy the folder to destination and remove
	@ #this makefile fromt it.
	@ cp -R . $(DST_DIR);
	@ rm $(DST_DIR)/Makefile;

	@ echo "Installed..."
