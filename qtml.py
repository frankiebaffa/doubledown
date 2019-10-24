#!/home/frankiebaffa/git/qtml/venv/bin/python3
import sys
from   models.qtmlparser import QtmlParser
from   models.pdf        import Pdf
from   optionparser      import parseOpts

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

def createQtml(options):
    qtml = QtmlParser(
            layoutfile = options['layoutfile'],
            contentfile= options['contentfile'],
            singlefile = options['singlefile']
            )
    return qtml

def createPdf(htmlstr,cssfile,output):
    if cssfile != None:
        Pdf.makePdfFromString(htmlstr,output,css=cssfile)
    else:
        Pdf.makePdfFromString(htmlstr,output)

def createHtmlDoc(htmlstr):
    with open("test.html","w") as file:
        file.write(htmlstr)

if __name__ == '__main__':
    options = parseOpts(sys.argv[1:])
    printStatus(options)
    qtml = createQtml(options)
    if options["html"]: createHtmlDoc(qtml.html)
    createPdf(qtml.html,options["cssfile"],options["output"])
    print('*** success!')
    sys.exit(2)
