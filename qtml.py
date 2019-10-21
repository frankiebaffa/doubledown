import re

class QtmlElement:
    qtag        = None
    qid         = None
    qclass      = None
    qattributes = None
    qinner      = None

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
            elementstr  = line[elementstart:elementend]
            qelement    = QtmlElement()

            qelement.qattributes\
           ,elementstr           = QtmlParser.checkGetAttr(elementstr)
            qelement.qclass\
           ,elementstr           = QtmlParser.checkGetClass(elementstr)

    @staticmethod
    def checkGetAttr(elementstr):
        attrs = re.findall(r"\[[a-zA-Z0-9=,]+\]",elementstr)
        print(attrs)
        return False,elementstr

    @staticmethod
    def checkGetClass(elementstr):
        classstart = None
        classes = re.findall(r"(?<=\.)[a-zA-Z0-9]+",elementstr)
        print(classes)
        return False,elementstr
