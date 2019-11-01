import sys
from   models.ddownparser import DDownParser
from   models.pdf         import Pdf
from   optionparser       import parseOpts
from   test               import Test
import requests
import os

def printStatus(options):
    if not options["quiet"]:
        print(f"Processing: {options['singlefile']}")

def createDDown(options):
    ddown = DDownParser(options=options)
    return ddown

def createPdf(htmlstr,output,css):
    tmpcss = None
    exists = True
    existi = 0
    while exists:
        tmpcss =  f"{output}.tmp{existi}.css"
        exists =  os.path.exists(tmpcss)
        existi += 1
    with open(tmpcss,"w") as file:
        file.write(css)
    Pdf.makePdfFromString(htmlstr,f"{output}.pdf",css=tmpcss)
    os.remove(tmpcss)

def createHtmlDoc(htmlstr,output):
    from bs4 import BeautifulSoup
    soup       = BeautifulSoup(htmlstr,features="html.parser")
    prettyhtml = soup.prettify()
    with open(output,"w") as file:
        file.write(prettyhtml)

def runTests(options):
    print("*** Running Testing Suite ***")
    t = Test(options)

if __name__ == '__main__':
    options = parseOpts(sys.argv[1:])
    if options == None:
        print("Error getting opts.")
        sys.exit(2)
    elif options["output"] == None and\
         options["test"] == False:
        print("Include -o switch to define output file.")
        sys.exit(2)

    if options["test"] == True:
        runTests(options)
    else:
        printStatus(options)

        ddown = createDDown(options)

        if options["html"]:
            createHtmlDoc(ddown.html,f"{options['output']}.html")

        createPdf(ddown.html,options["output"],ddown.css)

        if not options["quiet"]:
            print(f"Successfully created {options['output']}.pdf")
