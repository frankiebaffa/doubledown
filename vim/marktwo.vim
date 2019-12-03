" Vim syntax file
" Language:			MarkTwo
" Maintainer:		Frankie Baffa
" Latest Revision:	18 Oct 2019
" TODO:				Fix issue with including
"					CSS and JS syntax files

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

" Comment
syn match	comment
			\	contained
			\	containedin=ALLBUT,contentBlockLiteralRegion
			\	"\(\\\)\@<!\!#\(\s\|\t\|\S\)*$"
hi def link	comment Comment

" Configuration Block
syn	region	confBlockRegion
			\	contains=confBlockKey,confBlockVal,confBlockCon,confBlockSep
			\	start="\(^[ \t]*\)\@<=<!CONF>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/CONF>\($\)\@="
syn	match	confBlockKey
			\	contained
			\	containedin=confBlockRegion
			\	"\(^[ \t]*\)\@<=[a-zA-Z0-9\-]\+\(=\)\@="
syn match	confBlockVal
			\	contained
			\	containedin=confBlockRegion
			\	"\(=\)\@<=[a-zA-Z0-9\.]\+\($\)\@="
syn	match	confBlockCon
			\	contained
			\	containedin=confBlockRegion
			\	"\(^[ \t]*\)\@<=[a-zA-Z0-9\-]\+\($\)\@="
syn	match	confBlockSep
			\	contained
			\	containedin=confBlockRegion
			\	"\(^[ \t]*[a-zA-Z0-9\-]\+\)\@<==\([a-zA-Z0-9\.]\+$\)\@="
hi def link confBlockRegion Exception
hi def link confBlockKey	Title
hi def link	confBlockVal	Number
hi def link confBlockCon	Title
hi def link confBlockSep	Special

" Content Block
syn	region	contentBlockRegion
			\	contains=contentBlockId,contentBlockContent
			\	start="\(^[ \t]*\)\@<=<!CONTENT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/CONTENT>\($\)\@="
syn match	contentBlockId
			\	contained	containedin=contentBlockRegion	nextgroup=contentBlockContent	"\(^[ \t]*\)\@<=#[a-zA-Z0-9\-\_]\+\(:\)\@="
syn region	contentBlockContent
			\	contained
			\	containedin=contentBlockRegion
			\	start="\(\(^[ \t]*\)\@<=#[a-zA-Z0-9\-\_]\+:\)\@<=\(\s\|\t\|$\)"
			\	end="$\n\(^[ \t]*#[a-zA-Z0-9\-\_]\+:\|^[ \t]*<!\/\(CONTENT\|FOOTCONTENT\|HEADCONTENT\)>$\)\@="
syn match	contentBlockSpecial
			\	contained
			\	containedin=contentBlockContent
			\	"\(\\\)\@<!\(-\|_\||\|\$>\|<\$\|%>\|<%\)"
syn region	contentBlockLiteralRegion
			\	contained
			\	containedin=contentBlockContent
			\	start="\(\\\)\@<!{{"
			\	end="\(\\\)\@<!}}"
hi def link	contentBlockRegion			Exception
hi def link contentBlockId				Number
hi def link contentBlockContent			Title
hi def link contentBlockSpecial			Special
hi def link contentBlockLiteralRegion	String

" FootContent Block
syn	region footContentBlockRegion
			\	contains=contentBlockId,contentBlockContent
			\	start="\(^[ \t]*\)\@<=<!FOOTCONTENT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/FOOTCONTENT>\($\)\@="
hi def link	footContentBlockRegion	Exception

" HeadContent Block
syn	region	headContentBlockRegion
			\	contains=contentBlockId,contentBlockContent
			\	start="\(^[ \t]*\)\@<=<!HEADCONTENT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/HEADCONTENT>\($\)\@="
hi def link	headContentBlockRegion	Exception

" Shared Between Layout and Layout Var Blocks
syn region	openTag
			\	contained
			\	containedin=layoutVarBlockVarDef,layoutBlockRegion
			\	contains=tagName,tagKey,tagValWrap,tagProp
			\	start="<\(!\|\/\|@\|\/@\)\@!"
			\	end=">"
syn region	closeTag
			\	contained
			\	containedin=layoutVarBlockVarDef,layoutBlockRegion
			\	contains=tagName
			\	start="<\/\(@\)\@!"
			\	end=">"
syn	match	tagName
			\	contained
			\	containedin=openTag,closeTag																	"\(<[\/]*\)\@<=[a-zA-Z0-9]\+"
syn match	tagKey
			\	contained
			\	containedin=openTag	nextgroup=tagValWrap
			\	"\(\s\)\@<=[a-zA-Z0-9\-\_]\+\(=\)\@="
syn region	tagValWrap
			\	contained
			\	containedin=openTag
			\	contains=tagVal
			\	start="=\(\"\|\'\)"
			\	end="\(\"\|\'\)"
syn match	tagVal
			\	contained
			\	containedin=tagValWrap
			\	"\(=\(\"\|\'\)\)\@<=[a-zA-Z0-9\;:\%\-\_]\+\(\"\|\'\)\@="
syn match	tagProp
			\	contained
			\	containedin=openTag
			\	"\(\s\)\@<=[a-zA-Z0-9\-\_]\+\(\s\|>\|\/>\)\@="
hi def link	opentag		None
hi def link closeTag	None
hi def link tagName		Title
hi def link tagKey		Special
hi def link tagValWrap	PreProc
hi def link	tagVal		Number
hi def link tagProp		Number

" Layout Var Block
syn	region	layoutVarBlockRegion
			\	contains=layoutVarBlockVarDef
			\	start="\(^[ \t]*\)\@<=<!LAYOUTVARS>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/LAYOUTVARS>\($\)\@="
syn region	layoutVarBlockVarDef
			\	contains=openTag,closeTag
			\	contained
			\	containedin=layoutVarBlockRegion
			\	start="\(^[ \t]*\)\@<=<@[a-zA-Z0-9]\+>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<@\/[a-zA-Z0-9]\+>\($\)\@="
hi def link	layoutVarBlockRegion	Exception
hi def link layoutVarBlockVarDef	Special

" Layout Block
syn	region	layoutBlockRegion
			\	contains=openTag,closeTag,layoutBlockVarInst
			\	start="\(^[ \t]*\)\@<=<!LAYOUT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/LAYOUT>\($\)\@="
syn region	layoutBlockVarInst
			\	contained
			\	containedin=layoutBlockRegion
			\	contains=layoutBlockVarName,layoutBlockVarId
			\	start="\(^[ \t]*\)\@<=<@"
			\	end="\/>"
syn match	layoutBlockVarName
			\	contained
			\	containedin=layoutBlockVarInst
			\	"\(<@\)\@<=[a-zA-Z0-9\-\_]\+\(\#\|\/>\)\@="
syn match	layoutBlockVarId
			\	contained
			\	containedin=layoutBlockVarInst
			\	"\(<@[a-zA-Z0-9\-\_]\+\|[a-zA-Z0-9\-\_]\)\@<=#[a-zA-Z0-9\-\_]\+\(#\|\/>\)\@="
hi def link	layoutBlockRegion	Exception
hi def link layoutBlockVarInst	Special
hi def link layoutBlockVarName	Title
hi def link layoutBlockVarId	Number

" FootLayout Block
syn	region	footLayoutBlockRegion
			\	contains=openTag,closeTag,layoutBlockVarInst
			\	start="\(^[ \t]*\)\@<=<!FOOTLAYOUT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/FOOTLAYOUT>\($\)\@="
hi def link	footLayoutBlockRegion	Exception

" HeadLayout Block
syn	region	headLayoutBlockRegion
			\	contains=openTag,closeTag,layoutBlockVarInst
			\	start="\(^[ \t]*\)\@<=<!HEADLAYOUT>\($\)\@="
			\	end="\(^[ \t]*\)\@<=<!\/HEADLAYOUT>\($\)\@="
hi def link	headLayoutBlockRegion	Exception

" CSS Block
syn	region	cssBlockRegion
			\	start="<!CSS>"
			\	end="<!\/CSS>"
"			\	contains=@css
hi def link	cssBlockRegion	Exception

" JS Block
syn region	jsBlockRegion
			\	start="<!JS>"
			\	end="<!\/JS>"
"			\	contains=@js
hi def link	jsBlockRegion	Exception
