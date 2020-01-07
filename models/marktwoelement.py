class MarkTwoElement:
    qtag = ""
    qid = ""
    qclass = []
    qattributes = []
    qinner = []
    opentag = ""
    closetag = ""
    qtext = ""

    def generateHtml(self) -> None:
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
            if t := type(attr) == type({}):
                for key in attr.keys():
                    self.opentag += f" {key}=\"{attr[key]}\""
                    break
            elif t == type(''):
                self.opentag += f" {attr}"
        self.opentag += ">"
        if not self.isAutoClosing():
            self.closetag = f"</{self.qtag}>"

    def isAutoClosing(self) -> bool:
        return self.qtag in ["area","base","br","col","embed",
             "hr","img","input","link","meta",
             "param","source","track","wbr"]
