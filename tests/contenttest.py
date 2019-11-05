from models.ddownparser import DDownParser

class ContentTest:
    cbopen    = "_CONTENT|\n"
    cbclos    = "\n|CONTENT_"
    name      = None
    accepted  = None
    testinput = None
    response  = None
    passed    = None

    def __init__(self,name,idstr,text,accepted):
        self.name      = name
        self.accepted  = {idstr:accepted}
        self.testinput = f"{self.cbopen}#{idstr} {text}{self.cbclos}"

    def __repr__(self):
        return f"<ContentTest: {self.name} = {self.passed}>"

    def run(self,options):
        self.response = DDownParser(options=options,
                                    testinput=self.testinput).content
        self.passed   = self.response == self.accepted

    @staticmethod
    def get():
        tests = []
        tests.append(ContentTest("Basic ID/Text Dictionary",
                                 "Id",
                                 "lorem ipsum",
                                 "lorem ipsum"))
        tests.append(ContentTest("Inline <br> Tag",
                                 "Break",
                                 "This has--\na break",
                                 "This has<br>a break"))
        tests.append(ContentTest("Inline <s> Tag",
                                 "Strike",
                                 "-This is striken.- This is not",
                                 "<s>This is striken.</s> This is not"))
        tests.append(ContentTest("Inline <strong> Tag",
                                 "BoldText",
                                 "*this is bold*",
                                 "<strong>this is bold</strong>"))
        tests.append(ContentTest("Inline <em> Tag",
                                 "ItalicTest",
                                 "_this is italic_",
                                 "<em>this is italic</em>"))
        tests.append(ContentTest("Inline Embedded <strong><em> Tags",
                                 "Embedded",
                                 "*bold _bold/italic_ bold*",
                                 "<strong>bold <em>bold/italic</em> bold</strong>"))
        tests.append(ContentTest("Link With Text",
                                 "Link",
                                 "[Reddit](https://reddit.com)",
                                 "<a href=\"https://reddit.com\">Reddit</a>"))
        tests.append(ContentTest("Inline <li> Tags",
                                 "List",
                                 "|This is a list item|\n|this is another|",
                                 "<li>This is a list item</li><li>this is another</li>"))
        tests.append(ContentTest("Inline <ul> Tag Embedded <li> Tags",
                                 "Unordered",
                                 "%>|This is a list|\n|This is another item|<%",
                                 "<ul><li>This is a list</li><li>This is another item</li></ul>"))
        tests.append(ContentTest("Inline <ol> Tag Embedded <li> Tags",
                                 "Ordered",
                                 "$>|This is a list|\n|This is another item|<$",
                                 "<ol><li>This is a list</li><li>This is another item</li></ol>"))
        tests.append(ContentTest("Inline Lists Embedded Lists",
                                  "ListBlock",
                                  "%>|Unordered|\n$>|Embedded ordered|<$<%\n$>|Ordered|\n%>|Embedded unordered|<%<$",
                                  "<ul><li>Unordered</li><ol><li>Embedded ordered</li></ol></ul><ol><li>Ordered</li><ul><li>Embedded unordered</li></ul></ol>"))
        return tests
