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

def createPdf(htmlstr,cssfile):
    if cssfile != None:
        Pdf.makePdfFromString(htmlstr,'test.pdf',css=cssfile)
    else:
        Pdf.makePdfFromString(htmlstr,'test.pdf')

if __name__ == '__main__':
    options = parseOpts(sys.argv[1:])
    printStatus(options)
    qtml = createQtml(options)
    createPdf(qtml.html,options["cssfile"])
    print('*** success!')
    sys.exit(2)
