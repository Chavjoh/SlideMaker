import AbstractSyntaxTree as AST
from AbstractSyntaxTree import addToClass

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
	return self.tok[1:-1]

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
	return 'IDENTIFIER'

######################################################################
#                                ForNode                             #
######################################################################
@addToClass(AST.ForNode)
def assemble(self):
	return ''

######################################################################
#                               ParamsNode                           #
######################################################################
@addToClass(AST.ParamsNode)
def assemble(self):
	return self.children

if __name__ == "__main__":
	from SyntacticAnalyzer import parse
	import sys, os
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	assembled = ast.assemble()
	name = os.path.splitext(sys.argv[1])[0]+'.html'
	outfile = open(name, 'w')
	outfile.write(assembled)
	outfile.close()
	print ("Wrote output to", name)