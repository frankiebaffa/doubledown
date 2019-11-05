from tests.contenttest   import ContentTest
from tests.layouttest    import LayoutTest
from tests.htmltest      import HtmlTest
from tests.layoutvartest import LayoutVarTest

class TestSuite:
    allpass    = True
    tests      = []
    failcount  = 0

    def __init__(self,options):
        self._get()
        testtypes  = []
        testnames  = []
        teststats  = []
        for test in self.tests:
            test.run(options)

            tpass = None
            if test.passed: tpass = "Passed"
            else:           tpass = "Failed"

            if not test.passed:
                self.allpass    = False
                self.failcount += 1

            testtypes.append(f"{test.testtype}")
            testnames.append(f"{test.name}")
            teststats.append(f"{tpass}")

        if not options["quiet"]:
            TestSuite._printPassArrs(testtypes,testnames,teststats)

            print("\n")
        if self.allpass:
            count = len(self.tests)
            print(f"*** All {count} tests passed! ***")
        else:
            count = len(self.tests)
            print(f"*** {self.failcount} Failed Of {count} Tests ***")

    @staticmethod
    def _printPassArrs(testtypes,testnames,teststats):
        maxTypeLen = 0
        maxNameLen = 0
        maxStatLen = 0
        for i in range(len(testtypes)):
            if len(testtypes[i]) > maxTypeLen: maxTypeLen = len(testtypes[i])
            if len(testnames[i]) > maxNameLen: maxNameLen = len(testnames[i])
            if len(teststats[i]) > maxStatLen: maxStatLen = len(teststats[i])

        maxTypeLen += 1
        maxNameLen += 1
        maxStatLen += 1

        finalTypes = []
        finalNames = []
        finalStats = []
        topBorder  = "/"
        botBorder  = "\\"
        for i in range(maxTypeLen+maxNameLen+maxStatLen+5):
            topBorder += "-"
            botBorder += "-"
        topBorder += "\\"
        botBorder += "/"
        for ttype in testtypes:
            for j in range(maxTypeLen-len(ttype)):
                ttype += " "
            ttype  = f"| {ttype}"
            finalTypes.append(ttype)
        for tname in testnames:
            for j in range(maxNameLen-len(tname)):
                tname += " "
            tname  = f"| {tname}"
            finalNames.append(tname)
        for tstat in teststats:
            for j in range(maxStatLen-len(tstat)):
                tstat += " "
            tstat  = f"| {tstat}|"
            finalStats.append(tstat)

        print(topBorder)
        for i in range(len(finalTypes)):
            print(f"{finalTypes[i]}{finalNames[i]}{finalStats[i]}")
        print(botBorder)

    def _get(self):
        self.tests += ContentTest.get()
        self.tests += LayoutTest.get()
        self.tests += LayoutVarTest.get()
        self.tests += HtmlTest.get()
