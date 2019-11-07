import sys
from   models.ddownparser import DDownParser
from   models.pdf         import Pdf
from   optionparser       import parseOpts
from   tests.testsuite    import TestSuite as Test
import requests
import os

def createDDown(options):
    ddown = DDownParser(options=options)
    return ddown

def createPdf(htmlstr,headhtmlstr,foothtmlstr,output,css):
    options = {}
    tmpcss  = None
    exists  = True
    existi  = 0
    while exists:
        tmpcss =  f"{output}.tmp{existi}.css"
        exists =  os.path.exists(tmpcss)
        existi += 1
    with open(tmpcss,"w") as file:
        file.write(css)

    tmphead = None
    if headhtmlstr != None:
        exists = True
        existi = 0
        while exists:
            tmphead = f"{output}.head{existi}.html"
            exists  = os.path.exists(tmphead)
            existi += 1
        with open(tmphead,"w") as file:
            file.write(headhtmlstr)
        options["header-html"] = tmphead

    tmpfoot = None
    if foothtmlstr != None:
        exists = True
        existi = 0
        while exists:
            tmpfoot = f"{output}.foot{existi}.html"
            exists  = os.path.exists(tmpfoot)
            existi += 1
        with open(tmpfoot,"w") as file:
            file.write(foothtmlstr)
        options["footer-html"] = tmpfoot

    Pdf.makePdfFromString(htmlstr,f"{output}.pdf",options=options,css=tmpcss)
    os.remove(tmpcss)
    os.remove(tmphead)
    os.remove(tmpfoot)

def createHtmlDoc(htmlstr,output):
    from bs4 import BeautifulSoup
    soup       = BeautifulSoup(htmlstr,features="html.parser")
    prettyhtml = soup.prettify()
    with open(output,"w") as file:
        file.write(prettyhtml)

def runTests(options):
    print("*** Running Testing Suite ***\n")
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
        ddown = createDDown(options)

        if options["html"]:
            createHtmlDoc(ddown.html,f"{options['output']}.html")

        createPdf(ddown.html,ddown.headhtml,ddown.foothtml,options["output"],ddown.css)

        if not options["quiet"]:
            print(f"Successfully created {options['output']}.pdf")
