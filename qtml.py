import re

class QtmlElement:
    qtag        = None
    qid         = None
    qclass      = None
    qattributes = None
    qinner      = None

    def __init__(self):
        self.qtag        = None
        self.qid         = None
        self.qclass      = []
        self.qattributes = []
        self.qinner      = []

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

    def __init__(self,qfilepath):
        self.qdocument.qtag = "document"
        self.qdocument.qid  = "Document"
        with open(qfilepath,'r') as file:
            doctxt = file.read()
            self.qinput = doctxt
            arr = doctxt.split('\n')
            QtmlParser.mainLoop(self,arr)

    def mainLoop(self,arr):
        QtmlParser.getLayout(self,arr)

    def getLayout(self,arr):
        layoutstart = arr.index('_LAYOUT|')
        layoutend   = arr.index('|LAYOUT_')
        nestpath    = [self.qdocument]
        nestcount   = 0
        for i in range(layoutstart+1,layoutend):
            line = arr[i].lstrip()
            elementstart = None
            elementend   = None
            try:
                elementstart = line.index('_')
                elementend   = line.index('|')
            except:
                print(f'Malformed QTML on line {i}')
            if elementstart < elementend:
                elementstr  = line[elementstart+1:elementend]
                inlineclose   = False
                try:
                    lineend    = line[elementend+1:len(line)]
                    closepipe  = lineend.index('|')
                    closeunder = lineend.index('_')
                    if closepipe < closeunder:
                        inlineclose = True
                except:
                    continue
                qelement    = QtmlElement()
                qelement,\
                elementstr  = QtmlParser.checkGetName(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetAttr(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetClass(elementstr,qelement)
                nestpath[nestcount].qinner.append(qelement)
                #if not inlineclose:
                nestpath.append(nestpath[nestcount].qinner[len(nestpath[nestcount].qinner)-1])
                nestcount += 1
                #else:
            else:
                nestcount -= 1

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
        classstart = None
        classes = re.findall(r"(?<=\.)[a-zA-Z0-9]+",elementstr)
        for qclass in classes:
            elementstr = elementstr.replace(qclass,'',1)
            qelement.qclass.append(qclass)
        return qelement,elementstr

if __name__ == '__main__':
    QtmlParser('./test.qtml')
