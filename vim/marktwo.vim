" Vim syntax file
" Language:		   MarkTwo
" Maintainer:	   Frankie Baffa
" Latest Revision: 18 Oct 2019

if exists("b:current_syntax")
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

syntax spell toplevel

syn case ignore

" Imports
syn include @css	<sfile>:p:h/css.vim
syn include @js		<sfile>:p:h/javascript.vim

" Conf Overrides
syn region	marktwoConf		contains=marktwoConfKey,marktwoConfVal,marktwoConfSep,marktwoConfCon	start=+^_CONF|$+ end=+^|CONF_$+
syn match	marktwoConfKey	contained	containedin=marktwoConf										"\(^[ \t]*\)\@<=\S\+\(=\)\@="
syn match	marktwoConfVal	contained	containedin=marktwoConf										"\(=\)\@<=\S\+\($\)"
syn match	marktwoConfSep	contained	containedin=marktwoConf										"\(^[ \t]*\S\+\)\@<==\(\S\+$\)\@="
syn match	marktwoConfCon	contained	containedin=marktwoConf										"\(^[ \t]*\)\@<=[a-zA-Z0-9]\+\(=\)\@!$"

syn match marktwoTagName contained containedin=marktwoCloseTag,marktwoOpenTag "\(_\)\@<=[a-zA-Z0-9]\+\(\.\||\|#\|\[\)\@="
syn match marktwoTagName contained containedin=marktwoCloseTag,marktwoOpenTag "\(|\)\@<=[a-zA-Z0-9]\+\(_\)\@="
syn match marktwoId		 contained containedin=marktwoOpenTag,marktwoVarTag   "\(#\)\@<=[a-zA-Z0-9]\+\(\.\||\|\[\|@\|#\)\@="
syn match marktwoClass	 contained containedin=marktwoOpenTag			   "\(\.\)\@<=[a-zA-Z0-9]\+\(\.\||\|#\|\[\)\@="

" Attributes
syn match  marktwoAttr		   contained containedin=marktwoAtterList								 "[a-zA-Z]\+"
syn match  marktwoAttrVal	   contained containedin=marktwoAtterList								 "[a-zA-Z0-9\.\-\/:]\+"
syn match  marktwoAttrValDelim contained containedin=marktwoAtterList nextgroup=marktwoAttrVal			"="
syn match  marktwoAttrKey	   contained containedin=marktwoAtterList nextgroup=marktwoAttrValDelim		"[a-zA-Z]\+"
syn match  marktwoAttrDelim    contained containedin=marktwoAtterList nextgroup=marktwoAttrKey,marktwoAttr ","

syn region marktwoAttrList contained containedin=marktwoOpenTag contains=marktwoAttr,marktwoAttrVal,marktwoAttrValDelim,marktwoAttrKey,marktwoAttrDelim start="\[" end="\]"

syn match marktwoVarName contained containedin=marktwoVarName "\(@\)\@<=[a-zA-Z0-9]\+"

" Tag Elements
"syn region marktwoVarTag   contained containedin=marktwoLayout,marktwoHeadLayout,marktwoFootLayout				  oneline contains=marktwoId,marktwoVarName							 start="@\([a-zA-Z0-9]\)\@="	 end="@"
"syn region marktwoOpenTag  contained containedin=marktwoLayoutVar,marktwoLayout,marktwoHeadLayout,marktwoFootLayout oneline contains=marktwoId,marktwoClass,marktwoTagName,marktwoAttrList start="_\(CONTENT\|LAYOUT\)\@!" end="\(CONTENT\|LAYOUT\)\@<!|"
"syn region marktwoCloseTag contained containedin=marktwoLayoutVar,marktwoLayout,marktwoHeadLayout,marktwoFootLayout oneline contains=marktwoTagName									 start="|\(CONTENT\|LAYOUT\)\@!" end="\(CONTENT\|LAYOUT\)\@<!_"
syn region	marktwoLayoutOpenTag			start="<\(\/\)\@<!"	end=">"										contains=marktwoLayoutTagName,marktwoLayoutOpenTagPropName,marktwoLayoutOpenTagProp						containedin=marktwoLayout,marktwoLayoutVar	oneline
syn region	marktwoLayoutCloseTag			start="<\(\/\)\@<=" end=">"										contains=marktwoLayoutTagName													containedin=marktwoLayout,marktwoLayoutVar 	oneline
syn match	marktwoLayoutTagName			"\(<[\/]*\)\@<=[a-zA-Z0-9]\+"									containedin=marktwoLayoutOpenTag,marktwoLayoutCloseTag
syn region	marktwoLayoutOpenTagPropName	start="\(\s\)\@<=\([a-zA-Z0-9]\+=\)\(\'\|\"\)" end="\(\"\|\'\)"	containedin=marktwoLayoutOpenTag												contains=marktwoLayoutOpenTagPropVal			oneline
syn match	marktwoLayoutOpenTagPropVal		"\(id=\(\'\|\"\)\)\@<=[a-zA-Z0-9]\+"							containedin=marktwoLayoutOpenTagPropName
syn match	marktwoLayoutOpenTagProp		"\(<\)\@<![\s]\+[a-zA-Z0-9]\+\(\s\|>\)\@="						containedin=marktwoLayoutOpenTag

" Content Id
syn region	marktwoContentVar	contained containedin=marktwoContentText																oneline	start="\(\\\)\@<!@\(\S\+\)\@=" end="\(\S\+\)\@<=\(\\\)\@<!@"
syn region	marktwoContentText	contained containedin=marktwoContent,marktwoHeadContent,marktwoFootContent	contains=marktwoContentVar			start="\(\([ \t]*\)\@<=#[a-zA-Z0-9]\+\:\($\n^\)*[ \t]*\)\@<=\S"	end="$\n\(^[ \t]*#[a-zA-Z0-9]\+\:\|^|\(CONTENT\|HEADCONTENT\|FOOTCONTENT\)_$\)\@="
"																																																										end="^\(\(\(^[\t\s]*\)\@<=#[a-zA-Z0-9]\+\([\t\s]\+\)\@=\)\|^\(|CONTENT_\||HEADCONTENT_\||FOOTCONTENT_\)\@=\)\@="
syn match	marktwoInlineChar	contained containedin=marktwoContentText																		"\(\\\)\@<!\(%>\|<%\|\$>\|<\$\||\|_\|\*\|-\|\^\|\~\)"
syn match	marktwoContentId	contained containedin=marktwoContent,marktwoHeadContent,marktwoFootContent	nextgroup=marktwoContentText		"\(^[ \t]*\)\@<=#[a-zA-Z0-9]\+\:"

" Literal Block
syn region	marktwoLiteralContent	contained containedin=marktwoLiteralBlock	start=+\(\(\\\)\@<!{{[ \t]*\($\n^\)*[ \t]*\)\@<=\S+ end=+\S\([ \t]*\([$\n^\)*[ \t]*\(\\\)\@<!}}\)\)\@=+
syn region	marktwoLiteralBlock		contained containedin=marktwoContentText	start="\(\\\)\@<!{{" end="\(\\\)\@<!}}"

" Layout Variable
syn region marktwoLayoutVar contained containedin=marktwoLayoutVarSec start="@\(CONTENT\|LAYOUT\)\@![a-zA-Z0-9]\+|" end="|\(CONTENT\|LAYOUT\)\@![a-zA-Z0-9]\+@" contains=@html extend

syn region marktwoScriptInner contained containedin=marktwoScript start="\(_SCRIPT|\)\@<=$" end="^\(|SCRIPT_\)\@=" contains=@js

" Content regions
syn region marktwoComment	   start=+!#+ end=+$+ oneline containedin=ALL
syn region marktwoHeadLayout   start=+_HEADLAYOUT|$+  end=+|HEADLAYOUT_$+  contains=marktwoOpenTag,marktwoCloseTag
syn region marktwoHeadContent  start=+_HEADCONTENT|$+ end=+|HEADCONTENT_$+ contains=marktwoContentId,marktwoContentText
syn region marktwoFootLayout   start=+_FOOTLAYOUT|$+  end=+|FOOTLAYOUT_$+  contains=marktwoOpenTag,marktwoCloseTag
syn region marktwoFootContent  start=+_FOOTCONTENT|$+ end=+|FOOTCONTENT_$+ contains=marktwoContentId,marktwoContentText
syn region marktwoLayout	   start=+_LAYOUT|$+  end=+|LAYOUT_$+  contains=@html extend
syn region marktwoLayoutVarSec start=+^@LAYOUT|$+  end=+^|LAYOUT@$+  contains=marktwoLayoutVar
syn region marktwoContent	   start=+_CONTENT|$+ end=+|CONTENT_$+ contains=marktwoContentId,marktwoContentText
syn region marktwoStyle		   start=+^_STYLE|$+   end=+^|STYLE_$+	 contains=@css
syn region marktwoScript	   start="\(^\)\@<=_SCRIPT|\($\)\@="  end="\(^\)\@<=|SCRIPT_\($\)\@="  contains=marktwoScriptInner

hi def link marktwoConf           Comment
hi def link marktwoConfKey        Title
hi def link marktwoConfVal        Number
hi def link marktwoConfSep        Exception
hi def link marktwoConfCon        Title

hi def link marktwoComment		  Comment
hi def link marktwoScript		  Comment
hi def link marktwoStyle		  Comment
hi def link marktwoContent		  Comment
hi def link marktwoHeadLayout	  Comment
hi def link marktwoHeadContent	  Comment
hi def link marktwoFootLayout	  Comment
hi def link marktwoFootContent	  Comment
hi def link marktwoLayoutVarSec   Comment
hi def link marktwoHtml			  Comment
hi def link marktwoLayout		  Comment
hi def link marktwoLiteralBlock   Exception
hi def link marktwoLiteralContent Title
hi def link marktwoScriptInner	  Normal
hi def link marktwoStyleIdent	  Special
hi def link marktwoStyleRegion	  Exception
hi def link marktwoStyleKey		  Title
hi def link marktwoStyleValue	  Type
hi def link marktwoContentId	  Type
hi def link marktwoContentText	  Title
hi def link marktwoContentVar	  Special
hi def link marktwoInlineChar	  Comment
hi def link marktwoInnerText	  Special
hi def link marktwoLayoutVar	  Special
hi def link marktwoOpenTag		  Exception
hi def link marktwoVarTag		  Exception
hi def link marktwoCloseTag		  Exception
hi def link marktwoAttrList		  Exception
hi def link marktwoAttrDelim	  Comment
hi def link marktwoAttrKey		  Title
hi def link marktwoAttrValDelim   Special
hi def link marktwoAttrVal		  Type
hi def link marktwoAttr			  Title
hi def link marktwoClass		  Type
hi def link marktwoId			  Type
hi def link marktwoTagName		  Title
hi def link marktwoVarName		  Special

hi def link marktwoLayoutOpenTag			Exception
hi def link marktwoLayoutCloseTag			Exception
hi def link marktwoLayoutTagName			Title
hi def link marktwoLayoutOpenTagPropName	Type
hi def link marktwoLayoutOpenTagPropVal		Special
hi def link marktwoLayoutOpenTagProp		Type
