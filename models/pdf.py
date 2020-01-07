import pdfcrowd
import pdfkit

class Pdf:
    @staticmethod
    def makePdfFromString(html: str, name: str, overrides: dict,
            options: dict) -> None:
        if overrides['page-size'] != None:
            options['page-size'] = overrides['page-size']
        else:
            options['page-size'] = 'Letter'
        if overrides['margin-top'] != None:
            options['margin-top'] = overrides['margin-top']
        else:
            options['margin-top'] = '1.00in'
        if overrides['margin-right'] != None:
            options['margin-right'] = overrides['margin-right']
        else:
            options['margin-right'] = '1.00in'
        if overrides['margin-bottom'] != None:
            options['margin-bottom'] = overrides['margin-bottom']
        else:
            options['margin-bottom'] = '1.00in'
        if overrides['margin-left'] != None:
            options['margin-left'] = overrides['margin-left']
        else:
            options['margin-left'] = '1.00in'
        options['quiet'] = ''
        pdfkit.from_string(html,name,options=options)
