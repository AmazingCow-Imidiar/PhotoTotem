#!/usr/bin/python
# coding=utf8
##----------------------------------------------------------------------------##
##                 █      █                                                   ##
##                 ████████                                                   ##
##               ██        ██                                                 ##
##              ███  █  █  ███    generate_build.py                           ##
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
import os;
import os.path;
import sys;
import getopt;
import copy;

#COWTODO: THIS FILE IS A SHIT BOX. REFACTOR IT.....
class Constants:
    FLAG_MAJOR    = "major";
    FLAG_MINOR    = "minor";
    FLAG_REVISION = "revision";
    FLAG_BUILD    = "build";

    FLAG_OUTPUT_PATH = "output";

    ALL_FLAGS = [
        FLAG_MAJOR,
        FLAG_MINOR,
        FLAG_REVISION,
        FLAG_BUILD,

        FLAG_OUTPUT_PATH + "="
    ];

class Globals:
    opt_major       = False;
    opt_minor       = False;
    opt_revision    = False;
    opt_build       = False;

    opt_output_path = None;

    current_version = None;
    next_version    = None;

def print_fatal(msg):
    print "[FATAL] -", str(msg);
    exit(1);

def copy_all_stuff():
    #Create the output folder.
    folder_name      = "AmazingPhotoTotem_" + version_as_str(Globals.next_version);
    full_output_path = os.path.join(Globals.opt_output_path, folder_name);

    os.system("mkdir -p {}".format(full_output_path));

    #Copy the info files to output folder.
    for filename in ["AUTHORS.txt",
                     "CHANGELOG.txt",
                     "COPYING.txt",
                     "Makefile",
                     "README.md",
                     "TODO.txt",
                     "VERSION.txt"]:
        os.system("cp {} {}".format(filename, full_output_path));

    #Copy the src folder to output folder.
    os.system("cp -r {} {}".format("src", full_output_path));

    #Remove the Dev Makefile from the copied src folder.
    os.system("rm {}".format(os.path.join(full_output_path, "src", "Makefile")));
    #Remove all the .pyc files from the copied src folder.
    os.system("rm {}".format(os.path.join(full_output_path, "src", "*.pyc")));

################################################################################
## Version Load/Save/Helpers Functions                                        ##
################################################################################
def load_version_number():
    if(not os.path.isfile("./VERSION.txt")):
        print_fatal("MISSING VERSION FILE");

    version_line = None;
    lines        = open("./VERSION.txt").readlines();

    #Search the file until a non empty or commented lien appears.
    for line in lines:
        line = line.replace("\n", "");
        if(len(line) == 0 or line[0] == "#"):
            continue;

        version_line = line;
        break;

    #Check if we can decode the version, i.e. it has only numbers
    #separated by the . char.
    try:
        Globals.current_version = map(int, version_line.split("."));
    except Exception, e:
        print_fatal("Error while reading version - {}".format(e));

    #Check if all version numbers are present.
    if(len(Globals.current_version) != 4):
        print_fatal("Error while reading version - Wrong version format.");


def save_version_number():
    version_file = open("./VERSION.txt", "r");

    lines = version_file.readlines();
    version_line_index = 0;

    #Search the file until a non empty or commented lien appears.
    for i in xrange(0, len(lines)):
        line = lines[i];
        line = line.replace("\n", "");
        if(len(line) == 0 or line[0] == "#"):
            continue;

        version_line_index = i;
        break;

    lines[version_line_index] = version_as_str(Globals.next_version) + "\n";

    version_file.close();

    version_file = open("./VERSION.txt", "w");
    version_file.writelines(lines);
    version_file.close();


def version_as_str(version_list):
    return ".".join(map(str, version_list));


################################################################################
## Create Releases Functions                                                  ##
################################################################################
def create_major_release():
    print "Creating a MAJOR release.";

    load_version_number();

    Globals.next_version = copy.deepcopy(Globals.current_version);
    Globals.next_version[0] += 1;
    Globals.next_version[1]  = 0;
    Globals.next_version[2]  = 0;
    Globals.next_version[3]  = 0;

    print "Current Version:", version_as_str(Globals.current_version);
    print "Next Version   :", version_as_str(Globals.next_version);

    save_version_number();

    copy_all_stuff();

def create_minor_release():
    print "Creating a MINOR release.";

    load_version_number();

    Globals.next_version = copy.deepcopy(Globals.current_version);
    Globals.next_version[1] += 1;
    Globals.next_version[2]  = 0;
    Globals.next_version[3]  = 0;

    print "Current Version:", version_as_str(Globals.current_version);
    print "Next Version   :", version_as_str(Globals.next_version);

    save_version_number();

    copy_all_stuff();

def create_revision_release():
    print "Creating a REVISION release.";

    load_version_number();

    Globals.next_version = copy.deepcopy(Globals.current_version);
    Globals.next_version[2] += 1;
    Globals.next_version[3]  = 0;

    print "Current Version:", version_as_str(Globals.current_version);
    print "Next Version   :", version_as_str(Globals.next_version);

    save_version_number();

    copy_all_stuff();


def create_build_release():
    print "Creating a BUILD release.";

    load_version_number();

    Globals.next_version = copy.deepcopy(Globals.current_version);
    Globals.next_version[3] += 1;

    print "Current Version:", version_as_str(Globals.current_version);
    print "Next Version   :", version_as_str(Globals.next_version);

    save_version_number();

    copy_all_stuff();


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    try:
        options = getopt.gnu_getopt(sys.argv[1:], "", Constants.ALL_FLAGS);
    except Exception, e:
        print_fatal(e);

    #Parse the command line options.
    for key, value in options[0]:
        key = key.lstrip("-");

        if  (key == Constants.FLAG_MAJOR   ): Globals.opt_major    = True;
        elif(key == Constants.FLAG_MINOR   ): Globals.opt_minor    = True;
        elif(key == Constants.FLAG_REVISION): Globals.opt_revision = True;
        elif(key == Constants.FLAG_BUILD   ): Globals.opt_build    = True;

        elif(key == Constants.FLAG_OUTPUT_PATH):
            Globals.opt_output_path = os.path.abspath(os.path.expanduser(value));


    #Check if only one build type was passed.
    if(not (Globals.opt_major ^ Globals.opt_minor ^ Globals.opt_revision ^ Globals.opt_build)):
        print "MAJOR   :", Globals.opt_major;
        print "MINOR   :", Globals.opt_minor;
        print "REVISION:", Globals.opt_revision;
        print "BUILD   :", Globals.opt_build;
        print_fatal("Only one build type must be passed.");

    #Check if the output path is a directory.
    if(Globals.opt_output_path is None or not os.path.isdir(Globals.opt_output_path)):
        print_fatal("Output path must be a valid directory.");

    if  (Globals.opt_major   ): create_major_release();
    elif(Globals.opt_minor   ): create_minor_release();
    elif(Globals.opt_revision): create_revision_release();
    elif(Globals.opt_build   ): create_build_release();


main();
