from models.ddownparser import DDownParser

class LayoutVarTest:
    name      = None
    lvarname  = None
    accepted  = None
    testinput = None
    response  = None
    passed    = None

    def __init__(self,name,lvarname,layoutin,accepted):
        self.name      = name
        self.lvarname  = lvarname
        self.testinput = f"@LAYOUT|\n@{lvarname}|\n{layoutin}\n|{lvarname}@\n|LAYOUT@"
        self.accepted  = accepted

    def __repr__(self):
        return f"<LayoutVarTest: {self.name} = {self.passed}>"

    def run(self,options):
        self.response = DDownParser(options=options,
                                    testinput=self.testinput).lvars[self.lvarname]
        self.passed   = self.response == self.accepted

    @staticmethod
    def get():
        tests = []
        tests.append(LayoutVarTest("Basic Var",
                                   "var",
                                   ("_div.varContainer|\n"
                                        "_p#||_\n"
                                        "_p#||_\n"
                                        "_p#||_\n"
                                    "|div_"),
                                   ['_div.varContainer|',
                                        '_p#||_',
                                        '_p#||_',
                                        '_p#||_',
                                    '|div_']))
        return tests
