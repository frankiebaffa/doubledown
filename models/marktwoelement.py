from dataclasses import dataclass, field
from typing import List

@dataclass
class MarkTwoElement:
    qtag: str = field(repr=True, init=False, compare=True)
    qid: str = field(repr=True, init=False, compare=True)
    qclass: List[str] = field(default_factory=list, repr=True, init=False, compare=True)
    qattributes: list = field(default_factory=list, repr=False, init=False, compare=True)
    qinner: list = field(default_factory=list, repr=False, init=False, compare=True)
    opentag: str = field(default='', repr=False, init=False, compare=True)
    closetag: str = field(default='', repr=False, init=False, compare=True)
    qtext: str = field(default='', repr=False, init=False, compare=True)

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

    def isAutoClosing(self):
        a = ["area","base","br","col","embed",
             "hr","img","input","link","meta",
             "param","source","track","wbr"]
        return self.qtag in a
