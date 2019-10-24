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
                    "output"     : None,
                    "quiet"      : False,
                    "html"       : False
                  }
    try:
        opts,args = getopt.getopt(
            argv,
            "c:l:s:i:o:qh",
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
    hasOut = False
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
        elif opt == '-h':
            options["html"] = True
        elif opt == '-o':
            options["output"] = arg
            hasOut = True
    if not hasOut:
        print("Include -o switch and define output file.")
        sys.exit(2)
    return options
