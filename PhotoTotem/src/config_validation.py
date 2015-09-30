import json;
import sys;
import os.path;

from logger import Logger;

def __build_str(name, *args):
    msg = "[" + name + "]" + " - ";
    msg += " ".join(map(str, args));
    return msg;

def validate(name, filename, required_keys):
    Logger.instance().log_debug("config_validation.validate [{}]".format(name));

    #Check if filename is valid.
    #Empty.
    if(len(filename) == 0):
        msg = __build_str(name, "Configuration Filename is empty.");
        Logger.instance().log_fatal(msg);

    #Not a valid file path.
    if(not os.path.isfile(filename)):
        msg = __build_str(name, "Configuration filename is invalid.",
                          "Filename: ({})".format(filename));
        Logger.instance().log_fatal(msg);

    #Check if is a valid json.
    try:
        file_contents = json.load(open(filename));
    except Exception, e:
        msg = __build_str(name, "Configuration file isn't a valid json.",
                          "Filename: ({})".format(filename),
                          "Exception: ({})".format(str(e)));
        Logger.instance().log_fatal(msg);


    #Check if file has the required keys.
    for key in required_keys:
        if(key not in file_contents):
            msg = __build_str(name, "Configuration file doesn't have required key.",
                              "Key: ({})".format(key),
                              "Filename: ({})".format(filename));
            Logger.instance().log_fatal(msg);

    return file_contents;
