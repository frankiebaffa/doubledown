#!/home/frankiebaffa/git/qtml/venv/bin/python3
import re
import sys
import pdfcrowd
import pdfkit

class Pdf:
    @staticmethod
    def makePdfFromString(html,name,css=None):
        options = {'page-size':'A4',
                   'margin-top':'1.00in',
                   'margin-right':'1.00in',
                   'margin-bottom':'1.00in',
                   'margin-left':'1.00in',
                   'quiet':''}
        if css != None:
            print('with css')
            pdfkit.from_string(html,name,options=options,css=css)
        else:
            pdfkit.from_string(html,name,options=options)

class QtmlElement:
    qtag        = None
    qid         = None
    qclass      = None
    qattributes = None
    qinner      = None
    opentag     = None
    closetag    = None
    qtext       = None

    def __init__(self):
        self.qtag        = None
        self.qid         = None
        self.qclass      = []
        self.qattributes = []
        self.qinner      = []
        self.opentag     = ''
        self.closetag    = ''

    def generateHtml(self):
        self.opentag += f"<{self.qtag}"
        if self.qid != None:
            self.opentag += f" id=\"{self.qid}\""
        if len(self.qclass) > 0:
            self.opentag += " class="
            delim = ""
            for qclass in self.qclass:
                self.opentag += f"{delim}{qclass}"
                delim = " "
            self.opentag += "\""
        for attr in self.qattributes:
            if type(attr) == type({}):
                for key in attr.keys():
                    self.opentag += f" {key}=\"{attr[key]}\""
            elif type(attr) == type(''):
                self.opentag += f" {attr}"
        self.opentag += ">"
        if not QtmlElement.isAutoClosing(self.qtag):
            self.closetag = f"</{self.qtag}>"

    @staticmethod
    def isAutoClosing(name):
        a = ["area","base","br","col","embed",
             "hr","img","input","link","meta",
             "param","source","track","wbr"]
        return name in a

    def __repr__(self):
        printid = None
        if self.qid == None:
            printid = "No ID"
        else:
            printid = self.qid
        return f"<{self.qtag} | {printid} | classes:{len(self.qclass)} | inner:{len(self.qinner)}>"

class QtmlParser:
    qinput    = None
    qdocument = QtmlElement()
    html      = None
    content   = None
    css       = None

    def __init__(self,singlefile=None,contentfile=None,layoutfile=None,cssfile=None):
        self.qdocument.qtag = "document"
        self.qdocument.qid  = "Document"
        self.html = ''
        self.content = {}
        if (singlefile != None):
            with open(singlefile,'r') as file:
                doctxt = file.read()
                self.qinput = doctxt
                arr = doctxt.split('\n')
                self.getContent(arr)
                self.getLayout(arr)
        elif (contentfile != None and layoutfile != None):
            with open(contentfile,'r') as file:
                doctxt = file.read()
                self.qinput = doctxt
                arr = doctxt.split('\n')
                self.getContent(arr)
            with open(layoutfile,'r') as file:
                doctxt = file.read()
                self.qinput = doctxt
                arr = doctxt.split('\n')
                self.getLayout(arr)

        if cssfile != None:
            self.css = cssfile

    def getContent(self,arr):
        contentstart = arr.index('_CONTENT|')
        contentend   = arr.index('|CONTENT_')
        previousId   = None
        for i in range(contentstart+1,contentend):
            line = arr[i].lstrip().rstrip()
            if line[0:1] == '#':
                kv                = line.split(' ',1)
                cid               = kv[0][1:len(kv[0])]
                self.content[cid] = kv[1].lstrip()
                previousId        = cid
            else:
                self.content[cid] += f" {line}"

    def getLayout(self,arr):
        layoutstart = arr.index('_LAYOUT|')
        layoutend   = arr.index('|LAYOUT_')
        nestpath    = [self.qdocument]
        nestcount   = 0
        testcount   = 0
        for i in range(layoutstart+1,layoutend):
            inlineclose = False
            testcount += 1
            line = arr[i].lstrip().rstrip()
            elementstart = None
            elementend   = None

            try:
                elementstart = line.index('_')
                elementend   = line.index('|')
            except:
                print(f'Malformed QTML on line {i}')
                sys.exit(2)

            line = line.replace('|','',1)
            line = line.replace('_','',1)
            if line[len(line)-2:len(line)] == '|_':
                inlineclose = True
                line = line.replace('|_','',1)

            if elementstart < elementend:
                elementstr  = line
                qelement    = QtmlElement()
                qelement,\
                elementstr  = QtmlParser.checkGetName(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetAttr(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetClass(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetId(elementstr,qelement)
                qelement.generateHtml()
                self.html += qelement.opentag

                if qelement.qid in self.content.keys():
                    self.html += self.content[qelement.qid]

                nestpath[nestcount].qinner.append(qelement)
                nestpath.append(nestpath[nestcount].qinner[len(nestpath[nestcount].qinner)-1])
                nestcount += 1
            if elementstart > elementend or inlineclose:
                removedpath =  nestpath[nestcount:len(nestpath)]
                removedpath =  removedpath[::-1]
                for elem in removedpath:
                    self.html += elem.closetag
                nestpath    =  nestpath[0:nestcount]
                nestcount   -= 1

    @staticmethod
    def checkGetName(elementstr,qelement):
        name = re.findall(r"^[a-zA-Z0-9]+",elementstr)
        qelement.qtag = name[0]
        elementstr = elementstr.replace(name[0],'',1)
        return qelement,elementstr

    @staticmethod
    def checkGetAttr(elementstr,qelement):
        attrs = re.findall(r"(?<=\[)[a-zA-Z0-9=,\.]+(?=\])",elementstr)
        for match in attrs:
            elementstr = elementstr.replace(match,'',1)
            attrsplit = match.split(',')
            for attr in attrsplit:
                kv = attr.split('=')
                if len(kv) == 1:
                    qelement.qattributes.append(kv[0])
                elif len(kv) == 2:
                    qelement.qattributes.append({kv[0]:kv[1]})
        elementstr = elementstr.replace('[','')
        elementstr = elementstr.replace(']','')
        return qelement,elementstr

    @staticmethod
    def checkGetClass(elementstr,qelement):
        classes = re.findall(r"(?<=\.)[a-zA-Z0-9]+",elementstr)
        for qclass in classes:
            elementstr = elementstr.replace(qclass,'',1)
            qelement.qclass.append(qclass)
        return qelement,elementstr

    @staticmethod
    def checkGetId(elementstr,qelement):
        qids = re.findall(r"(?<=#)[a-zA-Z0-9]+",elementstr)
        for qid in qids:
            elementstr = elementstr.replace(qid,'',1)
            qelement.qid = qid
        return qelement,elementstr

if __name__ == '__main__':
    qtml = QtmlParser(
            layoutfile='./test.layout.qtml',
            contentfile='./test.content.qtml',
            cssfile='./test.css'
            )
    if qtml.css != None:
        Pdf.makePdfFromString(qtml.html,'test.pdf',css=qtml.css)
    else:
        Pdf.makePdfFromString(qtml.html,'test.pdf')

