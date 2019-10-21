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
        return f"<{self.qtag} | {printid} | classes:{len(self.qclass)}>"

class QtmlDocument:
    qtmlelements = []

class QtmlParser:
    qinput    = None
    qoutput   = None
    qdocument = None

    def __init__(self,qfilepath):
        with open(qfilepath,'r') as file:
            doctxt = file.read()
            arr = doctxt.split('\n')
            QtmlParser.mainLoop(arr)

    @staticmethod
    def mainLoop(arr):
        QtmlParser.getLayout(arr)

    @staticmethod
    def getLayout(arr):
        layoutstart = arr.index('_LAYOUT|')
        layoutend   = arr.index('|LAYOUT_')
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
                qelement    = QtmlElement()
                qelement,\
                elementstr  = QtmlParser.checkGetName(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetAttr(elementstr,qelement)
                qelement,\
                elementstr  = QtmlParser.checkGetClass(elementstr,qelement)
                print(qelement)
            else:
                # nothing yet
                continue

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
