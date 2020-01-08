class MarkTwoElement:
    def __init__(self):
        self.tag = None
        self.id = None
        self.clas = []
        self.attributes = []
        self.inner = []
        self.opentag = ""
        self.closetag = ""
        self.htmlstr = ""

    def generateHtmlTags(self) -> None:
        self.opentag += f"<{self.tag}"
        if self.id != None:
            self.opentag += f" id=\"{self.id}\""
        if len(self.clas) > 0:
            self.opentag += " class=\""
            delim = ""
            for clas in self.clas:
                self.opentag += f"{delim}{clas}"
                delim = " "
            self.opentag += "\""
        for attr in self.attributes:
            if t := type(attr) == type({}):
                for key in attr.keys():
                    self.opentag += f" {key}=\"{attr[key]}\""
                    break
            elif t == type(''):
                self.opentag += f" {attr}"
        self.opentag += ">"
        if not self.isAutoClosing():
            self.closetag = f"</{self.tag}>"

    def isAutoClosing(self) -> bool:
        return self.tag in ["area","base","br","col","embed",
             "hr","img","input","link","meta",
             "param","source","track","wbr"]
