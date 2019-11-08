from tests.contenttest   import ContentTest
from tests.layouttest    import LayoutTest
from tests.htmltest      import HtmlTest
from tests.layoutvartest import LayoutVarTest
from tests.footervartest import FooterHtmlTest

def tryIndex(s,t):
    x = -1
    try:
        x = s.index(t)
    except:
        pass
    return x

class TestSuite:
    allpass    = True
    tests      = []
    failcount  = 0

    def __init__(self,options):
        self._get()
        testtypes = []
        testnames = []
        teststats = []
        testrespo = []
        testaccep = []
        testcount = []
        tcount    = 1
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
            testrespo.append(f"{test.response}")
            testaccep.append(f"{test.accepted}")
            testcount.append(f"{tcount}")
            tcount += 1

        if not options["quiet"]:
            TestSuite._prettyPrintArrs([testcount.copy(),testtypes.copy(),testnames.copy(),teststats.copy()])
            if not self.allpass:
                fcount = []
                ftypes = []
                fnames = []
                fstats = []
                frespo = []
                faccep = []
                for i in range(len(testtypes)):
                    if tryIndex(teststats[i],"Failed") != -1:
                        fcount.append(testcount[i])
                        ftypes.append(testtypes[i])
                        fnames.append(testnames[i])
                        fstats.append(teststats[i])

                        srtdiff = 0
                        enddiff = 0
                        for j in range(len(testrespo[i])):
                            acpt    = testaccep[i]
                            resp    = testrespo[i]
                            if (acpt != resp):
                                srtcomp = 0
                                endcomp = 0
                                if j-5>=0:
                                    srtdiff = j-5
                                else:
                                    srtcomp = 5-j
                                    srtdiff = 0
                                if j+5+srtcomp<=len(testrespo[j]):
                                    enddiff=j+5+srtcomp
                                else:
                                    endcomp = len(testrespo[j])-j
                                    enddiff = len(testrespo[j])

                                if j-endcomp>=0:srtdiff=j-endcomp
                                break

                        frespo.append(testrespo[i][srtdiff:enddiff])
                        faccep.append(testaccep[i][srtdiff:enddiff])
                TestSuite._prettyPrintArrs([fcount,ftypes,fnames,fstats,frespo,faccep])
            print("\n")

        if self.allpass:
            count = len(self.tests)
            print(f"*** All {count} tests passed! ***")
        else:
            count = len(self.tests)
            print(f"*** {self.failcount} Failed Of {count} Tests ***")

    def _get(self):
        self.tests += ContentTest.get()
        self.tests += LayoutTest.get()
        self.tests += LayoutVarTest.get()
        self.tests += HtmlTest.get()
        self.tests += FooterHtmlTest.get()

    # where tarr is a 2d array in which the
    # 2nd dimensions are of equal length
    @staticmethod
    def _prettyPrintArrs(a):
        tarr = a
        marr = []
        farr = []
        for n in tarr:
            marr.append(0)
            farr.append([])
        for i in range(len(tarr)):
            for j in range(len(tarr[0])):
                if len(tarr[i][j])>marr[i]:marr[i]=len(tarr[i][j])
        for i in range(len(marr)):marr[i]+=1

        for i in range(len(tarr)):
            for j in range(len(tarr[i])):
                for k in range(marr[i]-len(tarr[i][j])):
                    tarr[i][j] += " "
                if   i!=len(tarr)-1:tarr[i][j]=f"| {tarr[i][j]}"
                elif i==len(tarr)-1:tarr[i][j]=f"| {tarr[i][j]}|"
                farr[i].append(tarr[i][j])

        topborder = "/"
        botborder = "\\"
        printstr  = ""
        for i in range(len(farr[0])):
            for j in range(len(farr)):
                printstr += farr[j][i]
                for k in range(len(farr[j][i])):
                    if i == 0:
                        topborder += "-"
                        botborder += "-"
            printstr += "\n"
        topborder  = topborder[0:len(topborder)-2]
        botborder  = botborder[0:len(botborder)-2]
        topborder += "\\\n"
        botborder += "/\n"

        print(f"{topborder}{printstr}{botborder}")
