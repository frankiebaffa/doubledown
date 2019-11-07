import pdfcrowd
import pdfkit

class Pdf:
    @staticmethod
    def makePdfFromString(html,name,css=None,options={}):
        options['page-size'] = 'Letter'
        options['margin-top'] = '1.00in'
        options['margin-right'] = '1.00in'
        options['margin-bottom'] = '1.00in'
        options['margin-left'] = '1.00in'
        options['quiet'] = ''
        if css != None:
            pdfkit.from_string(html,name,options=options,css=css)
        else:
            pdfkit.from_string(html,name,options=options)
