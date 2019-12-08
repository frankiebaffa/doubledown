import sys
from   models.marktwoparser import MarkTwoParser
from   models.pdf         import Pdf
from   optionparser       import parseOpts
from   tests.testsuite    import TestSuite as Test
import requests
import os

def createMarkTwo(options):
    marktwo = MarkTwoParser(options=options)
    return marktwo

def createPdf(htmlstr,headhtmlstr,foothtmlstr,output,overrides):
    options = {}
    tmpcss = None
    exists = True
    existi = 0
    tmphead = None
    if headhtmlstr != None:
        exists = True
        existi = 0
        while exists:
            tmphead = f"{output}.head{existi}.html"
            exists = os.path.exists(tmphead)
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
            exists = os.path.exists(tmpfoot)
            existi += 1
        with open(tmpfoot,"w") as file:
            file.write(foothtmlstr)
        options["footer-html"] = tmpfoot

    Pdf.makePdfFromString(htmlstr,f"{output}.pdf",overrides,options=options)
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
        marktwo = createMarkTwo(options)

        if options["html"]:
            createHtmlDoc(marktwo.html,f"{options['output']}.html")

        createPdf(marktwo.html,marktwo.headhtml,marktwo.foothtml,options["output"],marktwo.overrides)

        if not options["quiet"]:
            print(f"Successfully created {options['output']}.pdf")
