import sys
from   models.ddownparser import DDownParser
from   models.pdf        import Pdf
from   optionparser      import parseOpts
import requests

def printStatus(options):
    if not options["quiet"]:
        if options['layoutfile'] != None:
            print(f"Layout : {options['layoutfile']}")
        if options['contentfile'] != None:
            print(f"Content: {options['contentfile']}")
        if options['singlefile'] != None:
            print(f"Layout : {options['singlefile']}")
            print(f"Content: {options['singlefile']}")
        if options['cssfile'] != None:
            print(f"CSS    : {options['cssfile']}")

def createDDown(options):
    ddown = DDownParser(
            layoutfile    = options['layoutfile'],
            contentfile   = options['contentfile'],
            singlefile    = options['singlefile']
            )
    return ddown

def createPdf(htmlstr,cssfile,output):
    if cssfile != None:
        Pdf.makePdfFromString(htmlstr,output,css=cssfile)
    else:
        Pdf.makePdfFromString(htmlstr,output)

def createHtmlDoc(htmlstr,output):
    from bs4 import BeautifulSoup
    soup       = BeautifulSoup(htmlstr,features="html.parser")
    prettyhtml = soup.prettify()
    with open(output,"w") as file:
        file.write(prettyhtml)

if __name__ == '__main__':
    options = parseOpts(sys.argv[1:])
    printStatus(options)
    ddown = createDDown(options)
    if options["html"]: createHtmlDoc(ddown.html,f"{options['output']}.html")
    createPdf(ddown.html,options["cssfile"],f"{options['output']}.pdf")
    print('*** success!')
    sys.exit(2)
