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

class LayoutTest:
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
        self.response = DDownParser(options=options,
                                    testinput=self.testinput).html
        self.passed   = self.response == self.accepted

class FinalHtmlTest:
    name      = None
    accepted  = None
    testinput = None
    response  = None
    passed    = None

    def __init__(self,name,layoutin,contentin,accepted):
        self.name = name
        self.testinput  = f"_CONTENT|\n{contentin}\n|CONTENT_\n\n"
        self.testinput += f"_LAYOUT|\n{layoutin}\n|LAYOUT_"
        print(self.testinput)
        self.accepted = accepted

    def __repr__(self):
        return f"<FinalHtmlTest: {self.name} = {self.passed}>"

    def run(self,options):
        self.response = DDownParser(options=options,
                                    testinput=self.testinput).html
        self.passed   = self.response == self.accepted

class TestSuite:
    allpass    = True
    teststatus = ""
    tests      = []

    def __init__(self,options):
        self.contentTests()
        for test in self.tests:
            test.run(options)
            self.teststatus  += f"{test.name}:\n"
            self.teststatus  += f"Proper   : {test.accepted}\n"
            self.teststatus  += f"Response : {test.response}\n"
            self.teststatus  += f"Passed   : {test.passed}\n\n"
            if not test.passed:
                self.allpass = False

        with open('test.txt','w') as file:
            if not options["quiet"]:
                print(self.teststatus)
        if self.allpass:
            print("*** All tests passed! ***")
        else:
            print("*** Test failed ***")

    def contentTests(self):
        # Content Tests
        self.tests.append(ContentTest("Basic ID/Text Dictionary",
                                      "Id",
                                      "lorem ipsum",
                                      "lorem ipsum"))
        self.tests.append(ContentTest("Inline <br> Tag",
                                      "Break",
                                      "This has--\na break",
                                      "This has<br>a break"))
        self.tests.append(ContentTest("Inline <s> Tag",
                                      "Strike",
                                      "-This is striken.- This is not",
                                      "<s>This is striken.</s> This is not"))
        self.tests.append(ContentTest("Inline <strong> Tag",
                                      "BoldText",
                                      "*this is bold*",
                                      "<strong>this is bold</strong>"))
        self.tests.append(ContentTest("Inline <em> Tag",
                                      "ItalicTest",
                                      "_this is italic_",
                                      "<em>this is italic</em>"))
        self.tests.append(ContentTest("Inline Embedded <strong><em> Tags",
                                      "Embedded",
                                      "*bold _bold/italic_ bold*",
                                      "<strong>bold <em>bold/italic</em> bold</strong>"))
        self.tests.append(ContentTest("Link With Text",
                                      "Link",
                                      "[Reddit](https://reddit.com)",
                                      "<a href=\"https://reddit.com\">Reddit</a>"))
        self.tests.append(ContentTest("Inline <li> Tags",
                                      "List",
                                      "|This is a list item|\n|this is another|",
                                      "<li>This is a list item</li><li>this is another</li>"))
        self.tests.append(ContentTest("Inline <ul> Tag Embedded <li> Tags",
                                      "Unordered",
                                      "%>|This is a list|\n|This is another item|<%",
                                      "<ul><li>This is a list</li><li>This is another item</li></ul>"))
        self.tests.append(ContentTest("Inline <ol> Tag Embedded <li> Tags",
                                      "Ordered",
                                      "$>|This is a list|\n|This is another item|<$",
                                      "<ol><li>This is a list</li><li>This is another item</li></ol>"))
        self.tests.append(ContentTest("Inline Lists Embedded Lists",
                                       "ListBlock",
                                       "%>|Unordered|\n$>|Embedded ordered|<$<%\n$>|Ordered|\n%>|Embedded unordered|<%<$",
                                       "<ul><li>Unordered</li><ol><li>Embedded ordered</li></ol></ul><ol><li>Ordered</li><ul><li>Embedded unordered</li></ul></ol>"))

        # Layout Tests
        self.tests.append(LayoutTest("Basic Layout",
                                     ("_div|\n"
                                          "_p||_\n"
                                      "|div_"),
                                     "<div><p></p></div>"))

        self.tests.append(LayoutTest("Id and Class",
                                     ("_div#Id.class|\n"
                                          "_p#p1||_\n"
                                      "|div_"),
                                     "<div id=\"Id\" class=\"class\"><p id=\"p1\"></p></div>"))

        self.tests.append(LayoutTest("Multi-Class",
                                     ("_table#t1.tableOne.classTwo.whatever|\n"
                                          "_tbody|\n"
                                              "_tr|\n"
                                                  "_td||_\n"
                                              "|tr_\n"
                                          "|tbody_\n"
                                      "|table_"),
                                     "<table id=\"t1\" class=\"tableOne classTwo whatever\"><tbody><tr><td></td></tr></tbody></table>"))

        self.tests.append(LayoutTest("Attribute Test",
                                     "_p#Id.class[hidden]||_",
                                     "<p id=\"Id\" class=\"class\" hidden></p>"))

        self.tests.append(LayoutTest("Attribute Value",
                                     "_div[height=20,width=30]||_",
                                     "<div height=\"20\" width=\"30\"></div>"))

        self.tests.append(LayoutTest("Href Attribute",
                                     "_a[href=https://www.reddit.com]||_",
                                     "<a href=\"https://www.reddit.com\"></a>"))

        self.tests.append(LayoutTest("Local Href Attribute",
                                     "_a[href=/This/is/a/path/to/file.css]||_",
                                     "<a href=\"/This/is/a/path/to/file.css\"></a>"))

        self.tests.append(LayoutTest("Full Attribute",
                                     "_a[height=20,width=30,href=/this/is/a/path.css,hidden]||_",
                                     "<a height=\"20\" width=\"30\" href=\"/this/is/a/path.css\" hidden></a>"))

        # Final String Tests
        self.tests.append(FinalHtmlTest("Single Element",
                                        "_p#Id||_",
                                        "#Id Paragraph Tag",
                                        "<p id=\"Id\">Paragraph Tag</p>"))
        self.tests.append(FinalHtmlTest("Multi Element",
                                        ("_div|\n"
                                            "_p#Id||_\n"
                                         "|div_"),
                                        "#Id lorem ipsum",
                                        "<div><p id=\"Id\">lorem ipsum</p></div>"))
        self.tests.append(FinalHtmlTest("Complex Nesting / Elements",
                                        ("_div#Id.class[width=20,height=30,hidden]|\n"
                                             "_p#P1[onclick=someMethod]||_\n"
                                             "_table|\n"
                                                 "_tbody|\n"
                                                     "_tr|\n"
                                                         "_td#TD1||_\n"
                                                         "_td#TD2||_\n"
                                                         "_td#TD3||_\n"
                                                     "|tr_\n"
                                                 "|tbody_\n"
                                             "|table_\n"
                                         "|div_"),
                                        ("#P1 This is a paragraph\n"
                                         "#TD1 Cell 1"
                                         "#TD2 Cell 2"
                                         "#TD3 Cell 3"),
                                         ))
