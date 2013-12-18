# -*- coding: utf-8 -*-

import ply.lex as lex
import codecs

reserved_words = (
	'For',
)

tokens = (
	'GROUP',
	'SLIDE',
	'VERTICALBOX',
	'HORIZONTALBOX',
	'TITLE',
	'TEXT',
	'RICHTEXT',
	'ELEMENT',
	'IMAGE',
	'LIST',
	'TABLE',
	'PLUS',
	'NUMBER',
	'STRING',
	'IDENTIFIER',
) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();,{}'

def t_GROUP(t):
	r'Group'
	return t

def t_SLIDE(t):
	r'Slide'
	return t

def t_VERTICALBOX(t):
	r'VerticalBox'
	return t

def t_HORIZONTALBOX(t):
	r'HorizontalBox'
	return t

def t_TITLE(t):
	r'Title'
	return t

def t_TEXT(t):
	r'Text'
	return t

def t_RICHTEXT(t):
	r'RichText'
	return t

def t_ELEMENT(t):
	r'Element'
	return t

def t_IMAGE(t):
	r'Image'
	return t

def t_LIST(t):
	r'List'
	return t

def t_TABLE(t):
	r'Table'
	return t

def t_FOR(t):
	r'For'
	return t

def t_COMMENTSINGLE(t):
	r'//.*'
	pass

def t_COMMENTMULTI(t):
	r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
	pass

def t_PLUS(t):
	r'[+]'
	return t

def t_NUMBER(t):
	r'[0-9]+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
		t.value = 0
	return t

def t_STRING(t):
	r'"((\\\\")|[^"\r\n])*"'
	return t

def t_IDENTIFIER(t):
	r'[a-zA-Z]+'
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
	print("Illegal character ", repr(t.value[0]), " at line ", repr(t.lexer.lineno))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys

	prog = codecs.open(sys.argv[1], encoding='utf-8').read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok:
			break
		print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
