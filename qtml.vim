" Vim syntax file
" Language: QTML
" Maintainer: Frankie Baffa
" Latest Revision: 18 Oct 2019

if exists("b:current_syntax")
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

syntax spell toplevel

syn case ignore

syn match qtmlTagName contained containedin=qtmlCloseTag,qtmlOpenTag "\(_\)\@<=[a-zA-Z0-9]\+\(\.\||\|#\|\[\)\@="
syn match qtmlTagName contained containedin=qtmlCloseTag,qtmlOpenTag "\(|\)\@<=[a-zA-Z0-9]\+\(_\)\@="
syn match qtmlId      contained containedin=qtmlOpenTag              "\(#\)\@<=[a-zA-Z0-9]\+\(\.\||\|\[\)\@="
syn match qtmlClass   contained containedin=qtmlOpenTag              "\(\.\)\@<=[a-zA-Z0-9]\+\(\.\||\|#\|\[\)\@="

" Attributes
syn match  qtmlAttr         contained containedin=qtmlAtterList                                "[a-zA-Z]\+"
syn match  qtmlAttrVal      contained containedin=qtmlAtterList                                "[a-zA-Z0-9\.]\+"
syn match  qtmlAttrValDelim contained containedin=qtmlAtterList nextgroup=qtmlAttrVal          "="
syn match  qtmlAttrKey      contained containedin=qtmlAtterList nextgroup=qtmlAttrValDelim     "[a-zA-Z]\+"
syn match  qtmlAttrDelim    contained containedin=qtmlAtterList nextgroup=qtmlAttrKey,qtmlAttr ","

syn region qtmlAttrList contained containedin=qtmlOpenTag contains=qtmlAttr,qtmlAttrVal,qtmlAttrValDelim,qtmlAttrKey,qtmlAttrDelim start="\[" end="\]"

" Tag Elements
syn region qtmlOpenTag  contained containedin=qtmlLayout oneline contains=qtmlId,qtmlClass,qtmlTagName,qtmlAttrList start="_\(CONTENT\|LAYOUT\)\@!" end="\(CONTENT\|LAYOUT\)\@<!|"
syn region qtmlCloseTag contained containedin=qtmlLayout oneline contains=qtmlTagName                               start="|\(CONTENT\|LAYOUT\)\@!" end="\(CONTENT\|LAYOUT\)\@<!_"

" Content Id
syn match qtmlContentId contained containedin=qtmlContent nextgroup=qtmlInnerText "\(^\s*\)\@<=#[a-zA-Z0-9]\+\(\s\+\)\@="

" Content region
syn region  qtmlLayout  start=+^_LAYOUT|$+  end=+^|LAYOUT_$+  contains=qtmlOpenTag,qtmlCloseTag
syn region  qtmlContent start=+^_CONTENT|$+ end=+^|CONTENT_$+ contains=qtmlContentId
"syn match   qtmlProcTag +^\(__\|||\)\(LAYOUT\|CONTENT\)\(__\|||\)$+

hi def link qtmlProcTag      Comment
hi def link qtmlContent      Comment
hi def link qtmlLayout       Comment
hi def link qtmlContentId    Type
hi def link qtmlCloseTag     Exception
hi def link qtmlOpenTag      Exception
hi def link qtmlAttrList     Exception
hi def link qtmlAttrDelim    Comment
hi def link qtmlAttrKey      Title
hi def link qtmlAttrValDelim Special
hi def link qtmlAttrVal      Type
hi def link qtmlAttr         Title
hi def link qtmlClass        Type
hi def link qtmlId           Type
hi def link qtmlTagName      Title
