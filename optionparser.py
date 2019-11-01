import getopt
import sys

def parseOpts(argv):
    opts        = None
    options     = {
                   "singlefile"   : None,
                   "output"       : None,
                   "quiet"        : False,
                   "html"         : False,
                   "test"         : False
                  }
    try:
        opts,args = getopt.getopt(
            argv,
            "i:o:qht",
            [
             "singlefile=",
             "outputfile="
            ]
        )

        for opt,arg in opts:
            if   opt == '-i': options["singlefile"] = arg
            elif opt == '-o': options["output"] = arg
            elif opt == '-q': options["quiet"] = True
            elif opt == '-h': options["html"] = True
            elif opt == '-t': options["test"] = True

    except getopt.GetoptError:
        options = None

    return options
