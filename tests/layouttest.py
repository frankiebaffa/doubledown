from models.marktwoparser import MarkTwoParser

class LayoutTest:
    testtype  = "LAYOUT"
    lbopen    = "_LAYOUT|\n"
    lbclos    = "\n|LAYOUT_"
    name      = None
    accepted  = None
    testinput = None
    response  = None
    passed    = None

    def __init__(self,name,testinput,accepted):
        self.name      = name
        self.accepted  = accepted
        self.testinput = f"{self.lbopen}{testinput}{self.lbclos}"

    def __repr__(self):
        return f"<LayoutTest: {self.name} = {self.passed}>"

    def run(self,options):
        self.response = MarkTwoParser(options=options,
                                    testinput=self.testinput).html
        self.passed   = self.response == self.accepted

    @staticmethod
    def get():
        tests = []
        tests.append(LayoutTest("Basic Layout",
                                ("_div|\n"
                                     "_p||_\n"
                                 "|div_"),
                                "<div><p></p></div>"))

        tests.append(LayoutTest("Id and Class",
                                ("_div#Id.class|\n"
                                     "_p#p1||_\n"
                                 "|div_"),
                                "<div id=\"Id\" class=\"class\"><p id=\"p1\"></p></div>"))

        tests.append(LayoutTest("Multi-Class",
                                ("_table#t1.tableOne.classTwo.whatever|\n"
                                     "_tbody|\n"
                                         "_tr|\n"
                                             "_td||_\n"
                                         "|tr_\n"
                                     "|tbody_\n"
                                 "|table_"),
                                "<table id=\"t1\" class=\"tableOne classTwo whatever\"><tbody><tr><td></td></tr></tbody></table>"))

        tests.append(LayoutTest("Attribute",
                                "_p#Id.class[hidden]||_",
                                "<p id=\"Id\" class=\"class\" hidden></p>"))

        tests.append(LayoutTest("Attribute With Value",
                                "_div[height=20,width=30]||_",
                                "<div height=\"20\" width=\"30\"></div>"))

        tests.append(LayoutTest("Href Attribute",
                                "_a[href=https://www.reddit.com]||_",
                                "<a href=\"https://www.reddit.com\"></a>"))

        tests.append(LayoutTest("Local Href Attribute",
                                "_a[href=/This/is/a/path/to/file.css]||_",
                                "<a href=\"/This/is/a/path/to/file.css\"></a>"))

        tests.append(LayoutTest("Full Attribute",
                                "_a[height=20,width=30,href=/this/is/a/path.css,hidden]||_",
                                "<a hidden height=\"20\" width=\"30\" href=\"/this/is/a/path.css\"></a>"))
        return tests
