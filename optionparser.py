import getopt
import sys

def parseOpts(argv):
    contentfile = None
    layoutfile  = None
    cssfile     = None
    opts        = None
    options     = {
                    "contentfile": None,
                    "layoutfile" : None,
                    "cssfile"    : None,
                    "singlefile" : None,
                    "quiet"      : False
                  }
    try:
        opts,args = getopt.getopt(
            argv,
            "c:l:s:i:q",
            [
                "contentfile=",
                "layoutfile=",
                "cssfile=",
                "singlefile="
            ]
        )
    except getopt.GetoptError:
        print('Error getting opts')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-c':
            options["contentfile"] = arg
        elif opt == '-l':
            options["layoutfile"] = arg
        elif opt == '-s':
            options["cssfile"] = arg
        elif opt == '-i':
            options["singlefile"] = arg
        elif opt == '-q':
            options["quiet"] = True
    return options
