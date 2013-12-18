# -*- coding: utf-8 -*-

import ply.yacc as yacc

from LexicalAnalyzer import tokens
import AbstractSyntaxTree as AST

def p_program(p):
	''' program : statement '''
	p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
	''' program : statement program '''
	p[0] = AST.ProgramNode([p[1]] + p[2].children)

def p_statement(p):
	''' statement : group
		| slide '''
	p[0] = p[1]

def p_group(p):
	''' group : GROUP '(' params ')' '{' slidegroup '}' '''
	p[0] = AST.GroupNode([p[3]] + p[6])

def p_params(p):
	''' params : expression '''
	p[0] = AST.ParamsNode([p[1]])

def p_params_recursive(p):
	''' params : expression ',' params '''
	p[0] = AST.ParamsNode([p[1]] + p[3].children)

def p_params_nothing(p):
	''' params :'''
	p[0] = AST.ParamsNode()

def p_expression(p):
	''' expression : STRING
		| NUMBER '''
	if isinstance(p[1], int):
		p[0] = AST.NumberNode(int(p[1]))
	else:
		p[0] = AST.StringNode(str(p[1]))

def p_slidegroup(p):
	''' slidegroup : slide
		| slidefor '''
	p[0] = [p[1]]

def p_slidegroup_recursive(p):
	''' slidegroup : slide slidegroup
		| slidefor slidegroup '''
	p[0] = [p[1]] + p[2]

def p_slide(p):
	''' slide : SLIDE '(' params ')' '{' contentgroup '}' '''
	p[0] = AST.SlideNode([p[3]] + p[6])

def p_contentgroup(p):
	''' contentgroup : content '''
	p[0] = [p[1]]

def p_contentgroup_recursive(p):
	''' contentgroup : content contentgroup '''
	p[0] = [p[1]] + p[2]

def p_content(p):
	''' content : title
		| box
		| image
		| contenttext
		| list
		| contentfor '''
	p[0] = p[1]

def p_contenttext(p):
	''' contenttext : text
		| richtext '''
	p[0] = p[1]

def p_slidefor(p):
	''' slidefor : FOR '(' IDENTIFIER ',' NUMBER ',' NUMBER ')' '{' slidegroup '}' '''
	p[0] = AST.ForNode([AST.IdentifierNode(p[3]), AST.NumberNode(p[5]), AST.NumberNode(p[7])] + p[10])

def p_contentfor(p):
	''' contentfor : FOR '(' IDENTIFIER ',' NUMBER ',' NUMBER ')' '{' contentgroup '}' '''
	p[0] = AST.ForNode([AST.IdentifierNode(p[3]), AST.NumberNode(p[5]), AST.NumberNode(p[7])] + p[10])

def p_title(p):
	''' title : TITLE '(' complexstring ')' ';'	'''
	p[0] = AST.TitleNode(p[3])

def p_box(p):
	''' box : horizontalbox
		| verticalbox '''
	p[0] = p[1]

def p_horizontalbox(p):
	''' horizontalbox : HORIZONTALBOX '(' NUMBER ')' '{' contentgroup '}' '''
	p[0] = AST.BoxNode([AST.NumberNode(p[3])] + p[6], 'H')

def p_verticalbox(p):
	''' verticalbox : VERTICALBOX '(' NUMBER ')' '{' contentgroup '}' '''
	p[0] = AST.BoxNode([AST.NumberNode(p[3])] + p[6], 'V')

def p_image(p):
	''' image : IMAGE '(' complexstring ')' ';' '''
	p[0] = AST.ImageNode(p[3])

def p_text(p):
	''' text : TEXT '(' complexstring ')' ';' '''
	p[0] = AST.TextNode(p[3])

def p_richtext(p):
	''' richtext : RICHTEXT '(' ')' '{' elementgroup '}' '''
	p[0] = AST.RichTextNode(p[5])

def p_elementgroup(p):
	''' elementgroup : element '''
	p[0] = [p[1]]

def p_elementgroup_recursive(p):
	''' elementgroup : element elementgroup '''
	p[0] = [p[1]] + p[2]

def p_element(p):
	''' element : ELEMENT '(' complexstring ',' STRING ')' ';' '''
	p[0] = AST.ElementNode([p[3], AST.StringNode(p[5])])

def p_list(p):
	''' list : LIST '(' STRING ')' '{' textlist '}' '''
	p[0] = AST.ListNode([AST.StringNode(p[3])] + p[6])

def p_textlist(p):
	''' textlist : contenttext '''
	p[0] = [p[1]]

def p_textlist_recursive(p):
	''' textlist : contenttext textlist '''
	p[0] = [p[1]] + p[2]

def p_complexstring(p):
	''' complexstring : contentstring '''
	p[0] = AST.ComplexStringNode([p[1]])

def p_complexstring_recursive(p):
	''' complexstring : contentstring PLUS complexstring '''
	p[0] = AST.ComplexStringNode([p[1]] + p[3].children)

def p_contentstring_string(p):
	''' contentstring : STRING '''
	p[0] = AST.StringNode(p[1])

def p_contentstring_identifier(p):
	''' contentstring : IDENTIFIER '''
	p[0] = AST.IdentifierNode(p[1])

def p_error(p):
	if p:
		print ("Syntax error in line %d" % p.lineno)
		yacc.errok()
	else:
		print("Syntax error: unexpected end of file!")


def parse(program):
	return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys

	prog = open(sys.argv[1]).read()
	result = yacc.parse(prog)
	if result:
		print(result)

		import os

		graph = result.makegraphicaltree()
		name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
		graph.write_pdf(name)
		print("wrote ast to", name)
	else:
		print("Parsing returned no result!")