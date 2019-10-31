import getopt
import sys

def parseOpts(argv):
    opts        = None
    options     = {
                   "contentfile"  : None,
                   "layoutfile"   : None,
                   "cssfile"      : None,
                   "varfile"      : None,
                   "scriptfile"   : None,
                   "singlefile"   : None,
                   "output"       : None,
                   "quiet"        : False,
                   "html"         : False
                  }
    try:
        opts,args = getopt.getopt(
            argv,
            "c:l:s:i:o:v:j:qh",
            [
             "contentfile=",
             "layoutfile=",
             "cssfile=",
             "varfile=",
             "scriptfile=",
             "singlefile=",
             "outputfile="
            ]
        )

        for opt,arg in opts:
            if   opt == '-c': options["contentfile"] = arg
            elif opt == '-l': options["layoutfile"] = arg
            elif opt == '-s': options["cssfile"] = arg
            elif opt == '-v': options["varfile"] = arg
            elif opt == '-j': options["scriptfile"] = arg
            elif opt == '-i': options["singlefile"] = arg
            elif opt == '-q': options["quiet"] = True
            elif opt == '-h': options["html"] = True
            elif opt == '-o':
                options["output"] = arg

    except getopt.GetoptError:
        options = None

    return options
