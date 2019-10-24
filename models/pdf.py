import pdfcrowd
import pdfkit

class Pdf:
    @staticmethod
    def makePdfFromString(html,name,css=None):
        options = {'page-size':'Letter',
                   'margin-top':'1.00in',
                   'margin-right':'1.00in',
                   'margin-bottom':'1.00in',
                   'margin-left':'1.00in',
                   'quiet':''}
        if css != None:
            pdfkit.from_string(html,name,options=options,css=css)
        else:
            pdfkit.from_string(html,name,options=options)
