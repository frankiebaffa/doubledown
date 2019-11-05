from tests.contenttest   import ContentTest
from tests.layouttest    import LayoutTest
from tests.htmltest      import HtmlTest
from tests.layoutvartest import LayoutVarTest

class TestSuite:
    allpass    = True
    teststatus = ""
    tests      = []

    def __init__(self,options):
        self._get()
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

    def _get(self):
        self.tests += ContentTest.get()
        self.tests += LayoutTest.get()
        self.tests += HtmlTest.get()
        self.tests += LayoutVarTest.get()
