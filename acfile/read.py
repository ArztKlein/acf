from sly import Lexer, Parser

from acfile.acf import ACF

class ACFLexer(Lexer):

    def __init__(self):
         self.nesting_level = 0

    tokens = {SECTION, STRING, NUMBER, PLUS, MINUS, MULT, DIVIDE, POWER, ASSIGN, LPAREN, RPAREN, VARIABLE}
    ignore = ' \t'

    literals = { '(', ')', '.' }

    # Tokens
    ASSIGN   = r'='
    DIVIDE   = r'/'
    MINUS    = r'-'
    MULT     = r'\*'
    NUMBER   = r'''[+ -]?[0-9]+([.][0-9]+)?'''
    PLUS     = r'\+'
    POWER    = r'\^'
    SECTION  = r'@[a-zA-Z_]+'
    STRING   = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''
    LPAREN   = r'\('
    RPAREN   = r'\)'
    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_("string")
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    @_("number")
    def NUMBER(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text


    def error(self, t):
        self.index += 1


class ACFParser(Parser):
    tokens = ACFLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', MULT, DIVIDE),
        ('right', POWER)
    )

    def __init__(self):
        self.services = {}
        self.variables = {}


    def get_variable(self, identifier):
        try:
            return self.variables[self.current_section][identifier]
        except KeyError:
            raise Exception(f"Variable {identifier} could not be found. Cross-section variables are not allowed.")
    

    def set_variable(self, name, value):
        self.variables[self.current_section][name] = value

    @_("VARIABLE ASSIGN expr")
    def statement(self, p):
        self.set_variable(p.VARIABLE, p.expr)

    @_("expr MINUS expr")
    def expr(self, p):
        return p.expr0 - p.expr1

    @_("expr PLUS expr")
    def expr(self, p):
        return p.expr0 + p.expr1

    @_("expr MULT expr")
    def expr(self, p):
        return p.expr0 * p.expr1

    @_("expr DIVIDE expr")
    def expr(self, p):
        return p.expr0 / p.expr1

    @_("expr POWER expr")
    def expr(self, p):
        return p.expr0 ** p.expr1
    
    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("STRING")
    def expr(self, p):
        return p.STRING

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_("VARIABLE")
    def expr(self, p):
        return self.get_variable(p.VARIABLE)

    @_("SECTION")
    def statement(self, p):
        section_name = p.SECTION[1:]

        self.current_section = section_name
        self.variables[section_name] = {}
    

    def get_service(self, name):
        return self.services[name]


def read_string(string, dict=False) -> ACF | dict:
    lines = string.readlines()

    # Remove any empty lines
    lines = list(filter(None, lines))

    return read_lines(lines, dict=dict)


def read_lines(lines: list[str], dict=False) -> ACF | dict:
    lexer = ACFLexer()
    parser = ACFParser()

    for line in lines:
        try:
            parser.parse(lexer.tokenize(line))
        except EOFError:
            break

    if dict:
        return parser.variables
    else:
        return ACF(parser.variables)
    

def read_file(path: str, dict=False) -> ACF | dict:
    with open(path, 'r') as f:
        return read_string(f.read(), dict=dict)