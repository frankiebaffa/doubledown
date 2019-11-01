from models.ddownparser import DDownParser

class Test:
    name     = None
    teststr  = None
    accepted = None
    response = None
    passed   = None

    def __init__(self,teststr=None,accepted=None,response=None,passed=None):


class TestSuite:
    @staticmethod
    def runTests(options):
        runContentTests(options)

    @staticmethod
    def runContentTests(options):
        test = Test(
                    teststr  = "_CONTENT|\n#id1 lorem ipsum\n|CONTENT_",
                    accepted = {"id1":"lorem ipsum"},
                    response = DDownParser,
                    args     = {options=options,teststr=teststr},
                    passed   = response.content == accepted
                   )

        if passed:
            print("Test: Content")
