import re
from   models.ddownelement import DDownElement

class DDownParser:
    options   = None
    qinput    = None
    qdocument = DDownElement()
    html      = None
    css       = None
    lvars     = None
    content   = None
    script    = None

    def __init__(self,options=None,testinput=None):
        self.qdocument.qtag = "document"
        self.qdocument.qid  = "Document"
        self.html = ''
        self.lvars = {}
        self.content = {}
        self.options = options

        startpass = False
        if options['singlefile'] != None:
            with open(options['singlefile'],'r') as file:
                doctxt = file.read()
                self.qinput = doctxt
                startpass = True
        if options['test'] and testinput != None:
            self.qinput = testinput
            startpass = True

        if startpass:
            arr = self.qinput.split('\n')
            self.getContent(arr)
            self.getLayoutVars(arr)
            self.getLayout(arr)
            self.getStyle(arr)
            self.getScript(arr)
            if self.script != None:
                self.html += f"\n<script>\n{self.script}\n</script>"

    def getContent(self,arr):
        try:
            contentstart  = arr.index('_CONTENT|')
            contentend    = arr.index('|CONTENT_')
            previousId    = None
            contentconcat = ''
            for i in range(contentstart+1,contentend):
                line = arr[i].lstrip().rstrip()
                if line[0:1] == '#':
                    kv            =  line.split(' ',1)
                    cid           =  kv[0][1:len(kv[0])]
                    contentconcat += kv[1].lstrip()
                    previousId    =  cid
                else:
                    contentconcat += f" {line}"
                if i == contentend-1 or arr[i+1].lstrip().rstrip()[0:1] == '#':
                    if contentconcat != None and contentconcat != '':
                        self.content[previousId] = DDownParser.checkContentForInline(contentconcat)
                        contentconcat =  ''

            # HOTFIX FOR UNECESSARY SPACES BETWEEN EMPTY TAGS
            for key in self.content.keys():
                block    = self.content[key]
                patt     = r"</*(li|ul|ol)>"
                matchobj = [(m.start(0),m.end(0)) for m in re.finditer(patt,block)]
                if len(matchobj) > 0:
                    newblock = ""
                    le = None
                    ls = None
                    itercount = 0
                    for s,e in matchobj:
                        if itercount > 0:
                            check = block[le:s]
                            if check == " ":
                                newpart = f"{block[s:e]}"
                            else:
                                newpart = f"{block[le:e]}"
                            newblock += newpart
                        else:
                            newblock = f"{block[s:e]}"
                        le = e
                        ls = s
                        itercount += 1
                    self.content[key] = newblock

            # HOTFIX FOR UNECESSARY SPACES AFTER TEXT IN TAG
            for key in self.content.keys():
                block = self.content[key]
                patt  = r"(?<=\S)\s(?=$)"
                matchobj = [(m.start(0),m.end(0)) for m in re.finditer(patt,block)]
                newblock = None
                if len(matchobj) > 0:
                    match    = matchobj[0]
                    newblock = block[0:match[0]]
                    self.content[key] = newblock

        except:
            if not self.options["quiet"] and\
               not self.options["test"]:
                print("No content block")

    @staticmethod
    def checkContentForInline(text):
        try:
            openclose = {
                         r"(?<!\\)_"          : "em",
                         r"(?<!\\)\*"         : "strong",
                         r"(?<![\\\-])-(?!-)" : "s",
                         r"(?<![\\])\|"       : "li"
                        }

            opendiffclose = {
                             "ul" : {
                                     "open"  : r"(?<![\\])\%\>",
                                     "close" : r"(?<![\\])\<\%"
                                    },
                             "ol" : {
                                     "open"  : r"(?<![\\])\$\>",
                                     "close" : r"(?<![\\])\<\$"
                                    }
                            }

            standalone    = {r"(?<!\\)[\s]*\-\-[\s]*" : "br"} # space due to how content processes
            linktext      = r"(?<=\[).+(?=\])"
            link          = r"(?<=\().+(?=\))"

            for tagname in opendiffclose.keys():
                openpat = opendiffclose[tagname]["open"]
                clospat = opendiffclose[tagname]["close"]
                text    = re.sub(openpat,f"\\<{tagname}\\>",text)
                text    = re.sub(clospat,f"\\</{tagname}\\>",text)

            for key in openclose.keys():
                matches = re.findall(key,text)
                count   = len(matches)
                evenodd = count%2
                for i in range(count-evenodd):
                    if i%2 == 0:
                        text = re.sub(key,f"<{openclose[key]}>",text,1)
                    elif i%2 == 1:
                        text = re.sub(key,f"</{openclose[key]}>",text,1)

            for key in standalone.keys():
                matches = re.findall(key,text)
                text = re.sub(key,f"<{standalone[key]}>",text)

            matchobj    = [(m.start(0),m.end(0)) for m in re.finditer(linktext,text)]
            match       = matchobj[0]
            linkstr     = text[match[0]:match[1]]
            removestr   = r"\["+linkstr+"\]"
            matchobj    = [(m.start(0),m.end(0)) for m in re.finditer(link,text)]
            match       = matchobj[0]
            linkhyper   = text[match[0]:match[1]]
            removehyper = r"\("+linkhyper+"\)"
            if linkstr not in (None,'') and linkhyper not in (None,''):
                text = re.sub(removestr,f"<a href=\"{linkhyper}\">{linkstr}</a>",text)
                text = re.sub(removehyper,"",text)
        except:
            pass

        text = text.replace("\\","")
        return text

    def getLayoutVars(self,arr):
        try:
            lvarstart = arr.index('@LAYOUT|')
            lvarend   = arr.index('|LAYOUT@')
            newarr    = []
            for i in arr[lvarstart+1:lvarend]:
                newarr.append(i.rstrip().lstrip())
            lvarstarts = []
            lvarends   = []
            lvarnames  = []
            try:
                for i in range(len(newarr)):
                    line = newarr[i].rstrip().lstrip()
                    lvarstarti = [(m.start(0),m.end(0)) for m in re.finditer(r"(?<=@)[a-zA-Z0-9]+(?=\|)",line)]
                    lvarendi   = [(m.start(0),m.end(0)) for m in re.finditer(r"\|[a-zA-Z0-9]*@",line)]
                    if len(lvarstarti) > 0:
                        lvarstarts.append(i)
                        lvarnames.append(line[lvarstarti[0][0]:lvarstarti[0][1]])
                    if len(lvarendi) > 0:
                        lvarends.append(i)

                for i in range(len(lvarstarts)):
                    vararr = newarr[lvarstarts[i]+1:lvarends[i]]
                    self.lvars[lvarnames[i]] = vararr
            except:
                pass
        except:
            pass

    def getLayout(self,arr):
        def countIds(variable,pattern):
            idcount = 0
            for l in variable:
                matches = [(m.start(0),m.end(0)) for m in re.finditer(p,l)]
                if len(matches) > 0:
                    idcount += 1
            return idcount

        def subIds(variable):
            idcount = 0
            for j in range(len(variable)):
                l = variable[j]
                matches = [(m.start(0),m.end(0)) for m in re.finditer(p,l)]
                if len(matches) > 0:
                    variable[j] = re.sub(p,f"#{ids[idcount]}",l,1)
                    idcount += 1
            return variable

        def constructElement(line):
            elementstr  = line
            qelement    = DDownElement()
            qelement,\
            elementstr  = DDownParser.checkGetTag(elementstr,qelement)
            qelement,\
            elementstr  = DDownParser.checkGetAttr(elementstr,qelement)
            qelement,\
            elementstr  = DDownParser.checkGetClass(elementstr,qelement)
            qelement,\
            elementstr  = DDownParser.checkGetId(elementstr,qelement)
            qelement.generateHtml()
            return qelement,elementstr

        try:
            layoutstart = arr.index('_LAYOUT|')
            layoutend   = arr.index('|LAYOUT_')
            newarr      = arr[layoutstart+1:layoutend]
            finalarr    = []
            nestpath    = [self.qdocument]
            nestcount   = 0
            for i in range(len(newarr)):
                line = newarr[i].lstrip().rstrip()
                lvarstarti = [(m.start(0),m.end(0)) for m in re.finditer(r"(?<=@)[a-zA-Z0-9]+(?=[#@])",line)]
                if len(lvarstarti) > 0:
                    varname = line[lvarstarti[0][0]:lvarstarti[0][1]]
                    var = None
                    layoutvars = None
                    try:
                        layoutvars = self.lvars.copy()
                        var = layoutvars[varname].copy()
                    except:
                        if not self.options["quiet"] and\
                           not self.options["test"]:
                            print(f"Found undefined variable [{varname}] in layout")
                        sys.exit(2)
                    ids = re.findall(r"(?<=#)[a-zA-Z0-9]+(?=[@#])",line)
                    p = r"#(?![a-zA-Z0-9]+)"
                    idcount = countIds(var,p)
                    if len(ids) == idcount:
                        var = subIds(var)
                    else:
                        if not self.options["quiet"] and\
                           not self.options["test"]:
                            print(f"Defined variable [{varname}] not given correct # of ids")
                        sys.exit(2)
                    for j in var:
                        finalarr.append(j)
                else:
                    finalarr.append(line)

            for i in range(len(finalarr)):
                inlineclose = False
                line = finalarr[i].lstrip().rstrip()
                elementstart = None
                elementend   = None

                try:
                    elementstart = line.index('_')
                    elementend   = line.index('|')
                except:
                    if not self.options["quiet"] and\
                       not self.options["test"]:
                        print(f'Malformed QTML on line {i}')
                    sys.exit(2)

                line = line.replace('|','',1)
                line = line.replace('_','',1)
                if line[len(line)-2:len(line)] == '|_':
                    inlineclose = True
                    line = line.replace('|_','',1)

                if elementstart < elementend:
                    qelement,\
                    elementstr = constructElement(line)

                    self.html += f"{qelement.opentag}"

                    if qelement.qid in self.content.keys():
                        self.html += f"{self.content[qelement.qid]}"

                    nestpath[nestcount].qinner.append(qelement)
                    nestpath.append(nestpath[nestcount].qinner[len(nestpath[nestcount].qinner)-1])
                    nestcount += 1
                if elementstart > elementend or inlineclose:
                    removedpath =  nestpath[nestcount:len(nestpath)]
                    removedpath =  removedpath[::-1]
                    for elem in removedpath:
                        self.html += f"{elem.closetag}"
                    nestpath    =  nestpath[0:nestcount]
                    nestcount   -= 1
        except:
            if not self.options["quiet"] and\
               not self.options["test"]:
                print("No layout block")

    @staticmethod
    def checkGetTag(elementstr,qelement):
        name = re.findall(r"^[a-zA-Z0-9]+",elementstr)
        qelement.qtag = name[0]
        elementstr = elementstr.replace(name[0],'',1)
        return qelement,elementstr

    @staticmethod
    def checkGetAttr(elementstr,qelement):
        attrs = re.findall(r"(?<=\[)[a-zA-Z0-9=,\./:\-\;]+(?=\])",elementstr)
        for match in attrs:
            elementstr = elementstr.replace(match,'',1)
            attrsplit = match.split(',')
            for attr in attrsplit:
                kv = attr.split('=')
                if len(kv) == 1:
                    qelement.qattributes.append(kv[0])
                elif len(kv) == 2:
                    qelement.qattributes.append({kv[0]:kv[1]})
        elementstr = elementstr.replace('[','')
        elementstr = elementstr.replace(']','')
        return qelement,elementstr

    @staticmethod
    def checkGetClass(elementstr,qelement):
        classes = re.findall(r"(?<=\.)[a-zA-Z0-9\-]+",elementstr)
        for qclass in classes:
            elementstr = elementstr.replace("."+qclass,'',1)
            qelement.qclass.append(qclass)
        return qelement,elementstr

    @staticmethod
    def checkGetId(elementstr,qelement):
        qids = re.findall(r"(?<=#)[a-zA-Z0-9]+",elementstr)
        for qid in qids:
            elementstr = elementstr.replace("#"+qid,'',1)
            qelement.qid = qid
        return qelement,elementstr

    def getStyle(self,arr):
        try:
            stylestart = arr.index('_STYLE|')
            styleend   = arr.index('|STYLE_')
            self.css    = ''
            for i in range(stylestart+1,styleend):
                line = arr[i].rstrip()
                self.css += f"{line}"
        except:
            pass

    def getScript(self,arr):
        try:
            scriptstart = arr.index('_SCRIPT|')
            scriptend   = arr.index('|SCRIPT_')
            self.script = ''
            for i in range(scriptstart+1,scriptend):
                line = arr[i].rstrip()
                self.script += f"{line}\n"
        except:
            pass
