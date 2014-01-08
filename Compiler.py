#-*-coding:utf8-*-

import csv
import AbstractSyntaxTree as AST
from AbstractSyntaxTree import addToClass

vars = {}

######################################################################
#                              ProgramNode                           #
######################################################################
@addToClass(AST.ProgramNode)
def assemble(self):
	self.html = ""
	with open('templates/header.tpl') as file_header:
		self.html += file_header.read()
	for c in self.children:
		self.html += c.assemble()
	with open('templates/footer.tpl') as file_footer:
		self.html += file_footer.read()
	return self.html

######################################################################
#                               GroupNode                            #
######################################################################
def caseGroupTitle(p, node):
	node.title = p.assemble()

def caseGroupStyle(p, node):
	tab = p.assemble().replace(' ', '').split(',')
	for style in tab:
		subtab = style.split(':')
		if subtab[0] == 'background':
			node.html += " data-background=\"" + subtab[1] + "\""

switchGroupParams = {
	0: caseGroupTitle,
	1: caseGroupStyle,
}

@addToClass(AST.GroupNode)
def assemble(self):
	self.html = ""
	self.html += "<section"
	params = self.children[0].assemble()
	for i, p in enumerate(params):
		if i >= len(switchGroupParams):
			break
		switchGroupParams[i](p,self)
	self.html += ">\n"
	self.html += "<div class=\"sectiontitle\">" + self.title + "</div>\n"
	for c in self.children[1:]:
		self.html += c.assemble() + "\n"
	self.html += "</section>\n"
	return self.html

######################################################################
#                               SlideNode                            #
######################################################################
def caseSlideStyleBackground(p, node):
	node.html += " data-background=\"" + p + "\""

def caseSlideStyleTransition(p, node):
	node.html += " data-transition=\"" + p + "\""

switchSlideStyle = {
	'background': caseSlideStyleBackground,
	'transition': caseSlideStyleTransition,
}

def caseSlideStyle(p, node):
	tab = p.assemble().replace(' ', '').split(',')
	for style in tab:
		subtab = style.split(':')
		if subtab[0] in switchSlideStyle.keys():
			switchSlideStyle[subtab[0]](subtab[1], node)

switchSlideParams = {
	0: caseSlideStyle,
}

@addToClass(AST.SlideNode)
def assemble(self):
	self.html = ""
	self.html += "<section"
	params = self.children[0].assemble()
	for i, p in enumerate(params):
		if i >= len(switchSlideParams):
			break
		switchSlideParams[i](p,self)
	self.html += ">\n"
	for c in self.children[1:]:
		self.html += c.assemble() + "\n"
	self.html += "</section>\n"
	return self.html

######################################################################
#                                BoxNode                             #
######################################################################
@addToClass(AST.BoxNode)
def assemble(self):
	self.html = ""
	self.html += "<table cellpadding=\"0\" border=\"0\" cellspacing=\"" + str(self.children[0].assemble()) + "\">\n"
	if (self.orientation == 'H'):
		self.html += "<tr>\n"
		for c in self.children[1:]:
			self.html += "<td>" + c.assemble() + "</td>\n"
		self.html += "</tr>\n"
	else:
		for c in self.children[1:]:
			self.html += "<tr><td>" + c.assemble() + "</td></tr>\n"
	self.html += "</table>\n"
	return self.html

######################################################################
#                               TitleNode                            #
######################################################################
@addToClass(AST.TitleNode)
def assemble(self):
	self.html = ""
	self.html += "<h3>" + self.children[0].assemble() + "</h3>\n"
	return self.html

######################################################################
#                               TextNode                             #
######################################################################
@addToClass(AST.TextNode)
def assemble(self):
	self.html = ""
	self.html += self.children[0].assemble() + "\n"
	return self.html

######################################################################
#                              RichTextNode                          #
######################################################################
@addToClass(AST.RichTextNode)
def assemble(self):
	self.html = ""
	for c in self.children:
		self.html += c.assemble()
	return self.html

######################################################################
#                              ElementNode                           #
######################################################################
@addToClass(AST.ElementNode)
def assemble(self):
	self.html = ""
	self.html += "<span style=\""
	self.html += self.children[1].assemble().replace(',',';')
	self.html += "\">"
	self.html += self.children[0].assemble()
	self.html += "</span>\n"
	return self.html

######################################################################
#                               ImageNode                            #
######################################################################
@addToClass(AST.ImageNode)
def assemble(self):
	self.html = ""
	self.html += "<img src=\""
	self.html += self.children[0].assemble()
	self.html += "\" />\n"
	return self.html

######################################################################
#                               ListNode                             #
######################################################################
@addToClass(AST.ListNode)
def assemble(self):
	self.html = ""
	sense = self.children[0].assemble()
	if sense == "ordered":
		self.html += "<ol>\n"
	elif sense == "unordered":
		self.html += "<ul>\n"
	for c in self.children[1:]:
		self.html += "<li>" + c.assemble() + "</li>\n"
	if sense == "ordered":
		self.html += "</ol>\n"
	elif sense == "unordered":
		self.html += "</ul>\n"
	return self.html

######################################################################
#                              NumberNode                            #
######################################################################
@addToClass(AST.NumberNode)
def assemble(self):
	return self.tok

######################################################################
#                               StringNode                           #
######################################################################
@addToClass(AST.StringNode)
def assemble(self):
	cleaned_string = self.tok[1:-1]

	cleaned_string = cleaned_string.replace("\\\"", "\"");

	return cleaned_string

######################################################################
#                            ComplexStringNode                       #
######################################################################
@addToClass(AST.ComplexStringNode)
def assemble(self):
	self.html = ""
	for c in self.children:
		self.html += c.assemble()
	return self.html

######################################################################
#                               Identifier                           #
######################################################################
@addToClass(AST.IdentifierNode)
def assemble(self):
	global vars
	self.html = ""
	if str(self.tok) not in vars.keys():
		print ("Identifier ", self.tok, " undefined")
		exit(-1)
	self.html += str(vars[str(self.tok)])
	return self.html

######################################################################
#                                ForNode                             #
######################################################################
@addToClass(AST.ForNode)
def assemble(self):
	global vars
	self.html = ""
	if str(self.children[0].tok) in vars.keys():
		print("Identifier ", self.children[0].tok, " already defined")
		exit(-1)
	for i in range(int(self.children[1].assemble()), int(self.children[2].assemble()) + 1):
		vars[str(self.children[0].tok)] = i
		for c in self.children[3:]:
			self.html += c.assemble()
	vars.pop(str(self.children[0].tok), None)
	return self.html

######################################################################
#                               ParamsNode                           #
######################################################################
@addToClass(AST.ParamsNode)
def assemble(self):
	return self.children

######################################################################
#                               TableNode                            #
######################################################################
def caseSlideStyleBackground(p, node):
	node.html += " data-background=\"" + p + "\""

def caseSlideStyleTransition(p, node):
	node.html += " data-transition=\"" + p + "\""

def caseTableParamColStart(p, node):
	node.col_start = int(p)

def caseTableParamColCount(p, node):
	node.col_count = int(p)

def caseTableParamRowStart(p, node):
	node.row_start = int(p)

def caseTableParamRowCount(p, node):
	node.row_count = int(p)

switchTableParams = {
	'col-start': caseTableParamColStart,
	'col-count': caseTableParamColCount,
	'row-start': caseTableParamRowStart,
	'row-count': caseTableParamRowCount,
}

@addToClass(AST.TableNode)
def assemble(self):
	self.html = ""
	with open(self.children[0].assemble()) as csvfile:
		csvcontent = csv.reader(csvfile, delimiter=';')
		self.table = []
		for row in csvcontent:
			self.table.append([])
			for cell in row:
				self.table[len(self.table)-1].append(cell)
		self.col_start = 1
		self.row_start = 1
		self.row_count = len(self.table)
		self.col_count = 0
		if self.row_count != 0:
			self.col_count = len(self.table[0])
		if len(self.children) > 1:
			params = dict(item.split(":") for item in self.children[1].assemble().split(','))
			for key in params.keys():
				switchTableParams[key.strip()](params[key].strip(), self)
		self.html += "<table>\n"
		for row in self.table[self.row_start-1:self.row_start-1+self.row_count]:
			self.html += "<tr>\n"
			for cell in row[self.col_start-1:self.col_start-1+self.col_count]:
				self.html += "<td>" + cell + "</td>\n"
			self.html += "</tr>\n"
		self.html += "</table>\n"
	return self.html

if __name__ == "__main__":
	from SyntacticAnalyzer import parse
	import sys, os
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	assembled = ast.assemble()
	name = 'compile/' + os.path.basename(os.path.splitext(sys.argv[1])[0]) + '.html'
	outfile = open(name, 'w')
	outfile.write(assembled)
	outfile.close()
	print ("Wrote output to", name)