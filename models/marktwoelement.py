class MarkTwoElement:
    qtag        = None
    qid         = None
    qclass      = []
    qattributes = []
    qinner      = []
    opentag     = ''
    closetag    = ''
    qtext       = ''

    def getFullHtml(self):
        #def intoInner(elem,string):
        #    print(elem)
        #    string += f"{elem.opentag}"
        #    string += f"{elem.qtext}"
        #    for inner in elem.qinner:
        #        intoInner(inner,string)
        #    string += f"{elem.closetag}"
        #    return string
        htmlstr = ''
        #htmlstr = intoInner(self,htmlstr)
        print(self.qinner)
        return htmlstr


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
                    break
            elif type(attr) == type(''):
                self.opentag += f" {attr}"
        self.opentag += ">"
        if not MarkTwoElement.isAutoClosing(self.qtag):
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
        return f"<tag: {self.qtag} | id: {printid} | inner: {len(self.qinner)}>"
