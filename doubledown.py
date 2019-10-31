import sys
from   models.ddownparser import DDownParser
from   models.pdf        import Pdf
from   optionparser      import parseOpts
import requests
import os

def printStatus(options):
    if not options["quiet"]:
        if options['layoutfile'] != None:
            print(f"Layout   : {options['layoutfile']}")
        if options['contentfile'] != None:
            print(f"Content  : {options['contentfile']}")
        if options['singlefile'] != None:
            print(f"Layout   : {options['singlefile']}")
            print(f"Content  : {options['singlefile']}")
        if options['cssfile'] != None:
            print(f"CSS      : {options['cssfile']}")
        if options['output'] != None:
            print(f"Out      : {options['output']}")
        if options['html'] != None:
            print(f"HtmlFile : {options['html']}")

def createDDown(options):
    ddown = DDownParser(
            layoutfile    = options['layoutfile'],
            contentfile   = options['contentfile'],
            singlefile    = options['singlefile']
            )
    return ddown

def createPdf(htmlstr,cssfile,output,css):
    if cssfile != None:
        Pdf.makePdfFromString(htmlstr,f"{output}.pdf",css=cssfile)
    else:
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

if __name__ == '__main__':
    options = parseOpts(sys.argv[1:])
    if options == None:
        print("Error getting opts.")
        sys.exit(2)
    elif options["output"] == None:
        print("Include -o switch to define output file.")
        sys.exit(2)

    printStatus(options)

    ddown = createDDown(options)

    if options["html"]:
        createHtmlDoc(ddown.html,f"{options['output']}.html")

    createPdf(ddown.html,options["cssfile"],options["output"],ddown.css)

    if not options["quiet"]: print('*** success!')
