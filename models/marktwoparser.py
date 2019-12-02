# TODO: Switch layout syntax to standard
#       HTML syntax

import re
from   models.marktwoelement import MarkTwoElement

def arrFind(p,a):
    try:
        return a.index(p)
    except:
        return -1

def blockStartEnd(s,e,b,quiet=False):
    started         = s > -1
    ended           = e > -1
    placementproper = s < e
    if started and ended and placementproper:
        return True
    elif started and not ended:
        print(f"{b} is an unclosed block. Exiting.")
        sys.exit(1)
    elif not started and ended:
        print(f"{b} is never started and attempted closing. Exiting.")
        sys.exit(1)
    elif started and ended and not placementproper:
        print(f"{b} is improperly defined. Exiting.")
        sys.exit(1)
    elif not started and not ended:
        if not quiet: print(f"{b} not defined.")
        return False

class MarkTwoParser:
    options     = None
    qinput      = None
    qdocument   = MarkTwoElement()
    html        = None
    css         = None
    lvars       = None
    content     = None
    script      = None
    hdocument   = MarkTwoElement()
    headarr     = None
    headcontent = None
    headhtml    = None
    fdocument   = MarkTwoElement()
    footarr     = None
    foothtml    = None
    footcontent = None
    overrides   = {
                    "page-size":None,
                    "margin-top":None,
                    "margin-right":None,
                    "margin-bottom":None,
                    "margin-left":None
                  }
    constants   = {
                    "indent":None
                  }

    def __init__(self,options=None,testinput=None):
        self.qdocument.qtag = "document"
        self.qdocument.qid  = "Document"
        self.hdocument.qtag = "document"
        self.hdocument.qid  = "Document"
        self.fdocument.qtag = "document"
        self.fdocument.qid  = "Document"
        self.html = ''
        self.headhtml = ''
        self.foothtml = ''
        self.lvars = MarkTwoParser._getDefaultLayoutVars()
        self.content = {}
        self.headcontent = {}
        self.footcontent = {}
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

            # remove comments from array
            for i in range(len(arr)):
                line = arr[i]
                try:
                    indexofcomment = line.index("!#")
                    line = line[0:indexofcomment]
                    line = re.sub(r"\s*$","",line)
                    arr[i] = line
                except:
                    pass

            arr = self.pullHeader(arr)
            arr = self.pullFooter(arr)
            self.getConf(arr)
            self.getLayoutVars(arr)
            self._parse(arr)
            self.getStyle(arr)
            self.getScript(arr)
            if self.headarr != None:
                self._parse(self.headarr,loc="header")
            if self.footarr != None:
                self._parse(self.footarr,loc="footer")
            if self.css != None:
                self._appendStyle()
            if self.script != None:
                self._appendScripts()

    def _parse(self, arr, loc=None):
        self.getContent(arr,loc=loc)
        self.getLayout(arr,loc=loc)

    def _appendStyle(self):
        self.html     += f"\n<style>\n{self.css}\n</style>"
        self.headhtml += f"\n<style>\n{self.css}\n</style>"
        self.foothtml += f"\n<style>\n{self.css}\n</style>"

    def _appendScripts(self):
        self.html     += f"\n<script>\n{self.script}\n</script>"
        self.headhtml += f"\n<script>\n{self.script}\n</script>"
        self.foothtml += f"\n<script>\n{self.script}\n</script>"

    @staticmethod
    def _getDefaultLayoutVars():
        lvars = {
                 # THREE INLINE TEXT ELEMENTS ALIGNED LEFT, CENTER, RIGHT; RESPECTIVELY
                 "lcr":[
                        "_table.lcrContainer[style=width:100%;table-layout:fixed;]|",
                        "_tbody|",
                        "_tr|",
                        "_td#[style=width:50%;text-align:left;]||_",
                        "_td#[style=width:50%;text-align:center;]||_",
                        "_td#[style=width:50%;text-align:right;]||_",
                        "|tr_",
                        "|tbody_",
                        "|table_"
                       ],
                 # TWO INLINE TEXT ELEMENTS ALIGNED LEFT, RIGHT; RESPECTIVELY
                 "lr": [
                        "_table.lrContainer[style=width:100%;table-layout:fixed;]|",
                        "_tbody|",
                        "_tr|",
                        "_td#[style=width:50%;text-align:left]||_",
                        "_td#[style=width:50%;text-align:right;]||_",
                        "|tr_",
                        "|tbody_",
                        "|table_"
                       ]
                }
        
        return lvars

    def pullHeader(self,arr):
        contentstart = arrFind('_HEADCONTENT|',arr)
        contentend   = arrFind('|HEADCONTENT_',arr)
        has = blockStartEnd(contentstart,contentend,"Content Block (header)",quiet=True)
        if has:
            newarr = ['_CONTENT|']
            for i in range(contentstart+1,contentend):
                newarr.append(arr[i])
            newarr.append('|CONTENT_')
            arr = arr[0:contentstart]+arr[contentend+1:len(arr)]

        layoutstart = arrFind('_HEADLAYOUT|',arr)
        layoutend   = arrFind('|HEADLAYOUT_',arr)
        has = blockStartEnd(layoutstart,layoutend,"Layout Block (header)",quiet=True)
        if has:
            newarr.append('_LAYOUT|')
            for i in range(layoutstart+1,layoutend):
                newarr.append(arr[i])
            newarr.append('|LAYOUT_')
            arr = arr[0:layoutstart]+arr[layoutend+1:len(arr)]
            self.headarr = newarr

        return arr

    def pullFooter(self,arr):
        contentstart = arrFind('_FOOTCONTENT|',arr)
        contentend   = arrFind('|FOOTCONTENT_',arr)
        has = blockStartEnd(contentstart,contentend,"Content Block (footer)",quiet=True)
        if has:
            newarr = ['_CONTENT|']
            for i in range(contentstart+1,contentend):
                newarr.append(arr[i])
            newarr.append('|CONTENT_')
            arr = arr[0:contentstart]+arr[contentend+1:len(arr)]

        layoutstart = arrFind('_FOOTLAYOUT|',arr)
        layoutend   = arrFind('|FOOTLAYOUT_',arr)
        has = blockStartEnd(layoutstart,layoutend,"Layout Block (footer)",quiet=True)
        if has:
            newarr.append('_LAYOUT|')
            for i in range(layoutstart+1,layoutend):
                newarr.append(arr[i])
            newarr.append('|LAYOUT_')
            arr = arr[0:layoutstart]+arr[layoutend+1:len(arr)]
            self.footarr = newarr

        return arr

    def getConf(self,arr,):
        confstart = arrFind('_CONF|',arr)
        confend   = arrFind('|CONF_',arr)
        has = blockStartEnd(confstart,confend,"Configuration Block")
        if has:
            for i in range(confstart+1,confend):
                line = arr[i].lstrip().rstrip()
                key  = re.findall(r"\S+(?==)",line)
                val  = re.findall(r"(?<==)\S+",line)
                if len(key) > 0 and len(val) > 0:
                    try:
                        self.overrides[key[0]]
                        self.overrides[key[0]] = val[0]
                    except:
                        try:
                            self.constants[key[0]]
                            self.constants[key[0]] = val[0]
                        except:
                            print(f"Invalid configuration option: '{key[0]}'.")

    def getContent(self,arr,loc=None):
        locstr = None
        if loc == None: locstr = "main"
        else: locstr = loc
        contentstart  = arrFind('_CONTENT|',arr)
        contentend    = arrFind('|CONTENT_',arr)
        has = blockStartEnd(contentstart,contentend,f"Content Block ({locstr})")
        if has:
            previousId    = None
            contentconcat = ''
            for i in range(contentstart+1,contentend):
                line = re.sub(r"^[\s\t]+","",arr[i],1)
                if line[0:1] == '#':
                    kv            =  re.split(r":",line)
                    kv[1]         =  kv[1].lstrip()
                    cid           =  kv[0][1:len(kv[0])]
                    contentconcat += kv[1]
                    previousId    =  cid
                else:
                    contentconcat += f" {line}"
                if i == contentend-1 or arr[i+1].lstrip().rstrip()[0:1] == '#':
                    if contentconcat != None and contentconcat != '':
                        if loc == None:
                            contentconcat = MarkTwoParser.checkContentForInline(contentconcat)
                            contentconcat = self.checkContentForVars(contentconcat)
                            self.content[previousId] = contentconcat
                        elif loc == "header":
                            contentconcat = MarkTwoParser.checkContentForInline(contentconcat)
                            contentconcat = self.checkContentForVars(contentconcat)
                            self.headcontent[previousId] = contentconcat
                        elif loc == "footer":
                            contentconcat = MarkTwoParser.checkContentForInline(contentconcat)
                            contentconcat = self.checkContentForVars(contentconcat)
                            self.footcontent[previousId] = contentconcat
                        contentconcat =  ''

            # HOTFIX FOR UNECESSARY SPACES BETWEEN EMPTY TAGS
            if loc == None:
                for key in self.content.keys():
                    block    = self.content[key]
                    patt     = r"(?<!\s)\>\s\<"
                    block    = re.sub(patt,"><",block)
                    self.content[key] = block
            if loc == "header":
                for key in self.headcontent.keys():
                    block    = self.headcontent[key]
                    patt     = r"(?<!\s)\>\s\<"
                    block    = re.sub(patt,"><",block)
                    self.headcontent[key] = block
            if loc == "footer":
                for key in self.footcontent.keys():
                    block    = self.footcontent[key]
                    patt     = r"(?<!\s)\>\s\<"
                    block    = re.sub(patt,"><",block)
                    self.footcontent[key] = block

            # HOTFIX FOR UNECESSARY SPACES AFTER TEXT IN TAG
            if loc == None:
                for key in self.content.keys():
                    block = None
                    block = self.content[key]
                    patt  = r"(?<=\S)\s(?=$)"
                    matchobj = [(m.start(0),m.end(0)) for m in re.finditer(patt,block)]
                    newblock = None
                    if len(matchobj) > 0:
                        match    = matchobj[0]
                        newblock = block[0:match[0]]
                        self.content[key] = newblock
            elif loc == "header":
                for key in self.headcontent.keys():
                    block = None
                    block = self.headcontent[key]
                    patt  = r"(?<=\S)\s(?=$)"
                    matchobj = [(m.start(0),m.end(0)) for m in re.finditer(patt,block)]
                    newblock = None
                    if len(matchobj) > 0:
                        match    = matchobj[0]
                        newblock = block[0:match[0]]
                        self.headcontent[key] = newblock
            if loc == "footer":
                for key in self.footcontent.keys():
                    block = None
                    block = self.footcontent[key]
                    patt  = r"(?<=\S)\s(?=$)"
                    matchobj = [(m.start(0),m.end(0)) for m in re.finditer(patt,block)]
                    newblock = None
                    if len(matchobj) > 0:
                        match    = matchobj[0]
                        newblock = block[0:match[0]]
                        self.footcontent[key] = newblock

    @staticmethod
    def checkContentForLiteral(text):
        getliteralsections   = r"(?<!\\){{.*?(?<!\\)}}"
        literalsections      = re.findall(getliteralsections,text)
        getcharstoliteralize = r"[^a-zA-Z0-9\s\t\n\.,]"
        for literalsection in literalsections:
            if literalsection.find("{{") == 0 and literalsection.rfind("}}") == len(literalsection)-2:
                newliteralsection = f"{literalsection[2:len(literalsection)-2]}"
                charstoliteralize = re.findall(getcharstoliteralize,newliteralsection)
                charstoliteralize = list(set(charstoliteralize))
                for char in charstoliteralize:
                    newliteralsection = newliteralsection.replace(char, f"\\{char}")
                newliteralsection = newliteralsection.rstrip().lstrip()
                text = text.replace(literalsection, newliteralsection)
        return text

    @staticmethod
    def checkContentForInline(text):
        try:
            openclose = {
                         r"(?<!\\)_"          : "em",
                         r"(?<!\\)\*"         : "strong",
                         r"(?<![\\\-])-(?!-)" : "s",
                         r"(?<![\\])\|"       : "li",
                         r"(?<![\\])\^"       : "sup",
                         r"(?<![\\])\~"       : "sub"
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

            text = MarkTwoParser.checkContentForLiteral(text)

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

    def checkContentForVars(self,content):
        def wrapVar(p):
            return r"(?<!\\)@"+p+r"(?<!\\)@"

        contentvars = [
                        {
                            "name"       :"pagebreak",
                            "pattern"    :wrapVar(r"pagebreak"),
                            "replacement":"<div style='page-break-before:always;display:block;width:0px;height:0px;'></div>"
                        }
                      ]
        dynamicvars = [
                        {
                            "name"       :r"indent",
                            "modpattern" :r"(?<=indent)[0-9]+",
                            "pattern"    :wrapVar(r"indent[0-9]+"),
                            "modifier"   :"width",
                            "replacement":"<span style='display:inline-block;margin:0px;padding:0px;width:{width}px;'></span>"
                        }
                      ]
        for var in contentvars:
            content = re.sub(var["pattern"],var["replacement"],content)

        for var in dynamicvars:
            pat       = var["pattern"]
            foundvars = re.findall(pat,content)
            for dynvar in foundvars:
                mod = re.findall(var["modpattern"],dynvar)[0]
                replacement = re.sub(r"{"+var["modifier"]+"}",mod,var["replacement"])
                content = re.sub(dynvar,replacement,content)

        for var in dynamicvars:
            pat       = wrapVar(var["name"])
            foundvars = re.findall(pat,content)
            for convar in foundvars:
                if self.constants[var["name"]] != None:
                    mod = self.constants[var["name"]]
                    replacement = re.sub(r"{"+var["modifier"]+"}",mod,var["replacement"])
                    content = re.sub(convar,replacement,content)
                else:
                    print("Instance of constant variable without declaration of constant")
        return content

    def getLayoutVars(self,arr):
        lvarstart = arrFind('@LAYOUT|',arr)
        lvarend   = arrFind('|LAYOUT@',arr)
        has = blockStartEnd(lvarstart,lvarend,"Layout Variable Block")
        if has:
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

    def getLayout(self,arr,loc=None):
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
            qelement    = MarkTwoElement()
            qelement,\
            elementstr  = MarkTwoParser.checkGetTag(elementstr,qelement)
            qelement,\
            elementstr  = MarkTwoParser.checkGetAttr(elementstr,qelement)
            qelement,\
            elementstr  = MarkTwoParser.checkGetClass(elementstr,qelement)
            qelement,\
            elementstr  = MarkTwoParser.checkGetId(elementstr,qelement)
            qelement.generateHtml()
            return qelement,elementstr

        locstr = None
        if loc == None: locstr = "main"
        else: locstr = loc
        layoutstart = arrFind('_LAYOUT|',arr)
        layoutend   = arrFind('|LAYOUT_',arr)
        has = blockStartEnd(layoutstart,layoutend,f"Layout Block ({locstr})")
        if has:
            newarr      = arr[layoutstart+1:layoutend]
            finalarr    = []
            nestpath    = []
            if loc == None:
                nestpath = [self.qdocument]
            elif loc == "header":
                nestpath = [self.hdocument]
            elif loc == "footer":
                nestpath = [self.fdocument]
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

                    if loc == None:
                        self.html += f"{qelement.opentag}"
                    elif loc == "header":
                        self.headhtml += f"{qelement.opentag}"
                    elif loc == "footer":
                        self.foothtml += f"{qelement.opentag}"

                    if loc == None:
                        if qelement.qid in self.content.keys():
                            self.html += f"{self.content[qelement.qid]}"
                    elif loc == "header":
                        if qelement.qid in self.headcontent.keys():
                            self.headhtml += f"{self.headcontent[qelement.qid]}"
                    elif loc == "footer":
                        if qelement.qid in self.footcontent.keys():
                            self.foothtml += f"{self.footcontent[qelement.qid]}"

                    nestpath[nestcount].qinner.append(qelement)
                    nestpath.append(nestpath[nestcount].qinner[len(nestpath[nestcount].qinner)-1])
                    nestcount += 1
                if elementstart > elementend or inlineclose:
                    removedpath =  nestpath[nestcount:len(nestpath)]
                    removedpath =  removedpath[::-1]
                    for elem in removedpath:
                        if loc == None:
                            self.html += f"{elem.closetag}"
                        elif loc == "header":
                            self.headhtml += f"{elem.closetag}"
                        elif loc == "footer":
                            self.foothtml += f"{elem.closetag}"
                    nestpath    =  nestpath[0:nestcount]
                    nestcount   -= 1

    @staticmethod
    def checkGetTag(elementstr,qelement):
        name = re.findall(r"^[a-zA-Z0-9]+",elementstr)
        qelement.qtag = name[0]
        elementstr = elementstr.replace(name[0],'',1)
        return qelement,elementstr

    @staticmethod
    def checkGetAttr(elementstr,qelement):
        attrsnoval = re.findall(r"(?<=[\[,])[a-zA-Z]+(?=[,\]])",elementstr)
        for match in attrsnoval:
            qelement.qattributes.append(match)

        attrswval  = re.findall(r"(?<=[\[,])[a-zA-Z]+=[a-zA-Z0-9=\./:\-\;%]+(?=[,\]])",elementstr)
        for match in attrswval:
            kv = match.split("=")
            qelement.qattributes.append({kv[0]:kv[1]})

        allattrstorem = re.findall(r"\[[a-zA-Z0-9=\./:\-\;%,]+\]",elementstr)
        for match in allattrstorem:
            elementstr = elementstr.replace(match,"")

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
        stylestart = arrFind('_STYLE|',arr)
        styleend   = arrFind('|STYLE_',arr)
        has = blockStartEnd(stylestart,styleend,f"Style Block")
        if has:
            self.css    = ''
            for i in range(stylestart+1,styleend):
                line = arr[i].rstrip()
                self.css += f"{line}"

    def getScript(self,arr):
        scriptstart = arrFind('_SCRIPT|',arr)
        scriptend   = arrFind('|SCRIPT_',arr)
        has = blockStartEnd(scriptstart,scriptend,f"Script Block")
        if has:
            self.script = ''
            for i in range(scriptstart+1,scriptend):
                line = arr[i].rstrip()
                self.script += f"{line}\n"
