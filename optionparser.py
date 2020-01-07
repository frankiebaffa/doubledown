import getopt
import sys
from marktwoerrors import MarkTwoOptionError
from typing import Dict, List

def analyzeOpts(options: Dict[str,str]) -> Dict[str,str]:
    if options['singlefile'][-4:] != ".mk2":
        options['singlefile'] += ".mk2"

    if options['singlefile'] != None and options['output'] == None:
        options['output'] = options['singlefile'][0:-4]

    return options

def parseOpts(argv: List[str]) -> Dict[str,str]:
    opts = None
    options = {
            "singlefile" : None,
            "output" : None,
            "quiet" : False,
            "html" : False,
            "test" : False
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
            if opt == '-i':
                options["singlefile"] = arg
            elif opt == '-o':
                options["output"] = arg
            elif opt == '-q':
                options["quiet"] = True
            elif opt == '-h':
                options["html"] = True
            elif opt == '-t':
                options["test"] = True

    except getopt.GetoptError as e:
        raise MarkTwoOptionError(parent=e,
                specific_message="Illegal option passed.")

    return analyzeOpts(options)
