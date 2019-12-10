import re
import sys
from   models.marktwoelement import MarkTwoElement
from   utils.utils import arrFind, regexHas, regexHasOne

class MarkTwoParser:
    options = None
    qinput = None
    document = MarkTwoElement()
    html = ''
    css = None
    lvars = {
        "lcr": [
                "<table style='width:100%;table-layout:fixed;' class='lcrContainer'>",
                "<tbody>",
                "<tr>",
                "<td id style='width:50%;text-align:left;'></td>",
                "<td id style='width:50%;text-align:center;'></td>",
                "<td id style='width:50%;text-align:right;'></td>",
                "</tr>",
                "</tbody>",
                "</table>"
        ],
            "lr": [
                    "<table style='width:100%;table-layout:fixed;' class='lrContainer'>",
                    "<tbody>",
                    "<tr>",
                    "<td id style='width:50%;text-align:left;'></td>",
                    "<td id style='width:50%;text-align:right;'></td>",
                    "</tr>",
                    "</tbody>",
                    "</table>"
        ]
    }
    content = {}
    script = None
    overrides = {
                    "page-size":None,
                    "margin-top":None,
                    "margin-right":None,
                    "margin-bottom":None,
                    "margin-left":None
                  }
    constants = {
                    "indent":None
                  }

    def __init__(self,options=None):
        self.document.qtag = "document"
        self.document.qid  = "Document"
        self.options = options

    def createArrayRemoveComments(self):
        if self.qinput != None:
            arr = self.qinput.split('\n')
            for i in range(len(arr)):
                line = arr[i]
                try:
                    indexofcomment = line.index("!#")
                    line = line[0:indexofcomment]
                    line = re.sub(r"\s*$","",line)
                    arr[i] = line
                except:
                    pass
            return arr
        else:
            return None

    @staticmethod
    def getConfFromMkTwo(options=None):
        mktp = MarkTwoParser(options=options)
        arr = mktp.createArrayRemoveComments()
        confstart = arrFind('<!CONF>',arr)
        confend   = arrFind('<!/CONF>',arr)
        has = MarkTwoParser._blockStartEnd(confstart,confend,"Configuration Block")
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
        return mktp.overrides

    @staticmethod
    def parseHtmlFromMkTwo(options=None,loc=None):
        mktp = MarkTwoParser(options=options)
        startpass = False
        if options['singlefile'] != None:
            with open(options['singlefile'],'r') as file:
                doctxt = file.read()
                mktp.qinput = doctxt
                startpass = True
        if options['test'] and testinput != None:
            mktp.qinput = testinput
            startpass = True

        if startpass:
            arr = mktp.createArrayRemoveComments()
            mktp.getLayoutVars(arr)
            mktp._parse(arr,loc)
            mktp.getStyle(arr)
            mktp.getScript(arr)
            if mktp.css != None:
                mktp._appendStyle()
            if mktp.script != None:
                mktp._appendScripts()
        mktp.document.getFullHtml()
        return mktp.html

    @staticmethod
    def _blockStartEnd(s,e,b,quiet=False):
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

    def _parse(self, arr, loc=None):
        self.getContent(arr,loc=loc)
        self.getLayout(arr,loc=loc)

    def _appendStyle(self):
        self.html     += f"\n<style>\n{self.css}\n</style>"

    def _appendScripts(self):
        self.html     += f"\n<script>\n{self.script}\n</script>"

    def getContent(self,arr,loc=None):
        locstr = None
        if loc == None: locstr = "main"
        else: locstr = loc
        contentstart = None
        contentend = None
        if loc == None:
            locstr = "main"
            contentstart  = arrFind('<!CONTENT>',arr)
            contentend    = arrFind('<!/CONTENT>',arr)
        elif loc == "footer":
            locstr = loc
            contentstart  = arrFind('<!FOOTCONTENT>',arr)
            contentend    = arrFind('<!/FOOTCONTENT>',arr)
        elif loc == "header":
            locstr = loc
            contentstart  = arrFind('<!HEADCONTENT>',arr)
            contentend    = arrFind('<!/HEADCONTENT>',arr)

        has = MarkTwoParser._blockStartEnd(contentstart,contentend,f"Content Block ({locstr})")
        if has:
            previousId    = None
            contentconcat = ''
            for i in range(contentstart+1,contentend):
                #line = re.sub(r"^[\s\t]+","",arr[i],1)
                line = arr[i].lstrip().rstrip()
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
                        contentconcat = MarkTwoParser.checkContentForInline(contentconcat)
                        contentconcat = self.checkContentForVars(contentconcat)
                        self.content[previousId] = contentconcat
                        contentconcat =  ''

            # HOTFIX FOR UNECESSARY SPACES BETWEEN EMPTY TAGS
            for key in self.content.keys():
                block    = self.content[key]
                patt     = r"(?<!\s)\>\s\<"
                block    = re.sub(patt,"><",block)
                self.content[key] = block

            # HOTFIX FOR UNECESSARY SPACES AFTER TEXT IN TAG
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
        lvarstart = arrFind('<!LAYOUTVARS>',arr)
        lvarend   = arrFind('<!/LAYOUTVARS>',arr)
        has = MarkTwoParser._blockStartEnd(lvarstart,lvarend,"Layout Variable Block")
        if has:
            newarr    = []
            for i in arr[lvarstart+1:lvarend]:
                newarr.append(i.rstrip().lstrip())
            lvarnames  = []
            lvarstarts = []
            lvarends   = []
            for i in range(len(newarr)):
                line = newarr[i]
                lvarname = re.findall(r"(?<=<@)[a-zA-Z0-9\_\-]+",line)
                if len(lvarname) > 0 and not len(lvarname) > 1:
                    lvarnames.append(lvarname[0])
                elif len(lvarname) > 1:
                    print("Multiple variables declared on same line. Invalid statement")
                    sys.exit(2)
            for lvarname in lvarnames:
                start   = arrFind(f"<@{lvarname}>", newarr)
                end     = arrFind(f"<@/{lvarname}>", newarr)
                lvararr = newarr[start+1:end]
                self.lvars[lvarname] = lvararr

    def getLayout(self,arr,loc=None):
        def constructElement(line):
            elementstr    = line
            qelement      = MarkTwoElement()
            ename         = re.findall(r"[a-zA-Z0-9]+",elementstr)[0]
            qelement.qtag = ename
            elementstr    = elementstr.replace(ename,'',1).rstrip().lstrip()
            eattrs        = re.findall(r"[a-zA-Z0-9]+(?=\=[\'\"][a-zA-Z0-9\-\_\:\%\; ]+[\'\"])",elementstr)
            if len(eattrs) > 0:
                for attr in eattrs:
                    val = re.findall(f"(?<={attr}=[\'\"])[a-zA-Z0-9\-\_\:\%\; ]+(?=[\'\"])",elementstr)[0]
                    if attr == 'id':
                        qelement.qid = val
                    if attr == 'class':
                        classes = val.split(' ')
                        for clas in classes:
                            if clas.rstrip().lstrip() != '':
                                qelement.qclass.append(clas)
                    if attr != 'class' and attr != 'id':
                        qelement.qattributes.append({attr:val})
                    substr     = f"{attr}=[\'\"]{val}[\"\']"
                    elementstr = re.sub(substr,'',elementstr).rstrip().lstrip()
            eprops        = re.findall(r"[a-zA-Z0-9]+(?!\=)",elementstr)
            eid           = re.findall(r"(?<=id=[\'\"])[a-zA-Z0-9]+(?=[\'\"])",elementstr)
            if len(eid) > 0:
                qelement.qid = eid[0]
                elementstr   = elementstr.replace(eid[0],'',1)
                elementstr   = re.sub(r"id=[\'\"][\'\"]",'',elementstr).lstrip().rstrip()
            qelement.generateHtml()
            return qelement

        def generateDocument(arr):
            nestpath    = []
            nestpath = [self.document]
            nestcount   = 0
            for i in range(len(arr)):
                inlineclose = False
                line = arr[i].lstrip().rstrip()

                #openp  = r"<[a-zA-Z0-9][a-zA-Z0-9\'\"\=\;\:\% ]+>"
                openp  = r"<(?!\/)[\S\s]+>"
                eopen  = re.findall(openp,line)
                openi  = [(m.start(0),m.end(0)) for m in re.finditer(openp,line)]
                hasopen = False
                if len(eopen) == 1:
                    eopen = eopen[0]
                    hasopen = True

                closep   = r"</[a-zA-Z0-9]+>"
                eclose   = re.findall(closep,line)
                closei   = [(m.start(0),m.end(0)) for m in re.finditer(closep,line)]
                closetag = None
                hasclose = False
                if len(eclose) == 1:
                    eclose = eclose[0]
                    hasclose = True
                    closetag = re.findall(r"(?<=<\/)[a-zA-Z0-9]+(?=>)",line)[0]

                estart = -1
                if len(openi) > 0:
                    estart = openi[0][0]

                eend = -1
                if len(closei) > 0:
                    eend = closei[0][0]

                if hasopen or hasclose:
                    autoclose   = line.count('/>') == 1
                    line        = line.replace('<','',1)
                    if not autoclose:
                        line = line.replace('>','',1)
                    else:
                        line = line.replace('/>','',1)
                        hasclose = True
                    ename       = re.findall(r"[a-zA-Z0-9]+",line)[0]
                    closepat    = f"</{ename}>"
                    inlineclose = line.count(closepat) == 1
                    if inlineclose:
                        line = line.replace(closepat,'')
                        hasclose = True

                    if hasopen:
                        qelement = constructElement(line)
                        self.html += f"{qelement.opentag}"

                        if qelement.qid in self.content.keys():
                            qelement.qtext = f"{self.content[qelement.qid]}"
                            self.html += f"{self.content[qelement.qid]}"

                        #nestpath[nestcount]\
                        #    .qinner.append(qelement)

                        #nestpath.append(
                        #    nestpath[nestcount]\
                        #        .qinner[len(
                        #            nestpath[nestcount]\
                        #                .qinner
                        #        )-1]
                        #)
                        nestpath.append(qelement)
                        nestcount += 1
                    if hasclose:
                        removedpath =  nestpath[nestcount:len(nestpath)]
                        removedpath =  removedpath[::-1]
                        for elem in removedpath:
                            self.html += f"{elem.closetag}"
                        nestpath    =  nestpath[0:nestcount]
                        nestcount   -= 1

        locstr = None
        if loc == None: locstr = "main"
        else: locstr = loc
        layoutstart = None
        layoutend = None
        if loc == None:
            locstr = "main"
            layoutstart  = arrFind('<!LAYOUT>',arr)
            layoutend    = arrFind('<!/LAYOUT>',arr)
        elif loc == "footer":
            locstr = loc
            layoutstart  = arrFind('<!FOOTLAYOUT>',arr)
            layoutend    = arrFind('<!/FOOTLAYOUT>',arr)
        elif loc == "header":
            locstr = loc
            layoutstart  = arrFind('<!HEADLAYOUT>',arr)
            layoutend    = arrFind('<!/HEADLAYOUT>',arr)
        has = MarkTwoParser._blockStartEnd(layoutstart,layoutend,f"Layout Block ({locstr})")
        if has:
            newarr      = arr[layoutstart+1:layoutend]
            finalarr    = []

            # replacevariables
            for i in range(len(newarr)):
                line = newarr[i].lstrip().rstrip()
                lvar = re.findall(r"(?<=<@)[a-zA-Z0-9\-\_]+",line)
                if len(lvar) > 0:
                    varname = lvar[0]
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
                    ids = re.findall(r"(?<=#)[a-zA-Z0-9]+(?=[\/#])",line)
                    idcount = 0
                    blankidp = r"(?<=\s)id(?=(\s|>))"
                    for eline in var:
                        idcount += len(re.findall(blankidp,eline))
                    if len(ids) == idcount:
                        idtopull = 0
                        for vline in var:
                            vlinehasid = regexHasOne(blankidp,vline)
                            if vlinehasid:
                                eid = ids[idtopull]
                                var[var.index(vline)] = re.sub(blankidp,f"id='{eid}'",vline,count=1)
                                idtopull += 1
                    else:
                        if not self.options["quiet"] and\
                           not self.options["test"]:
                            print(f"Defined variable [{varname}] not given correct # of ids")
                        sys.exit(2)
                    for j in var:
                        finalarr.append(j)
                else:
                    finalarr.append(line)
            # end replacevariables
            generateDocument(finalarr)

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
        stylestart = arrFind('<!CSS>',arr)
        styleend   = arrFind('<!/CSS>',arr)
        has = MarkTwoParser._blockStartEnd(stylestart,styleend,f"Style Block")
        if has:
            self.css    = ''
            for i in range(stylestart+1,styleend):
                line = arr[i].rstrip()
                self.css += f"{line}"

    def getScript(self,arr):
        scriptstart = arrFind('<!JS>',arr)
        scriptend   = arrFind('<!/JS>',arr)
        has = MarkTwoParser._blockStartEnd(scriptstart,scriptend,f"Script Block")
        if has:
            self.script = ''
            for i in range(scriptstart+1,scriptend):
                line = arr[i].rstrip()
                self.script += f"{line}\n"
