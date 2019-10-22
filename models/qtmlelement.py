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
            self.opentag += " class=\""
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
