from strings_with_arrows import *

all_num = '0123456789'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
special_chars = "$?@\^`#"
ident_special_chars = "$:?@\^\"`~#"

space_delim = " "
arithmetic_operator = "+-*/%"
relational_operator = '><==!<=>=!='
lineEnd_delim = " ;"
newline_delim = '\n'
symbols = ""
ident_delim = " ,+-*/%><!=&|)/{/}\']\"/~" + arithmetic_operator
closing_delim = arithmetic_operator + relational_operator + space_delim
num_delim = arithmetic_operator + space_delim + ',' + ' &&||' + relational_operator + ")]"
equal_delim = alphanum + "({"
block_delim = '{ \n '
loop_delim = ' ('
inner_delim = '>> '
outer_delim = '<< '
bool_delim = space_delim + lineEnd_delim + '\n' + ')'
delim0 = space_delim + alphanum
delim1 = delim0 + '\"' + '('
delim2 = delim0  + '('
delim3 = delim0 + newline_delim



#errors
error = []

#TOKENS

#reserved words
TAKEOFF = 'takeoff' #Start
LANDING = 'landing' #End

GALAXY = 'galaxy()'

#data types
INTEL = 'intel'
GRAVITY = 'gravity'
STAR = 'star'
BANG = 'bang'
VOID = 'void'
STRING = 'string'
VAR = 'var'
#data structure
ENTITY = 'entity'
#input and output statements
INNER = 'inner'
OUTER = 'outer'
#conditional statements
IF = 'if'
ELSE = 'else'
ELSEIF = 'elseif'
SHIFT = 'shift'
TRACE = 'trace'
#looping statements
FORCE = 'force'
WHIRL = 'whirl'
DO = 'do'
#loop control statements
BLAST = 'blast'
SKIP = 'skip'
#other statements
SATURN = 'saturn'
FORM = 'form'
LAUNCH = 'launch'
UNIVERSE = 'universe'
TRUE = 'true'
FALSE = 'false'


#OPERATORS

#assignment operators | done
EQUAL = '=' 
PLUS_EQUAL = '+='
MINUS_EQUAL = '-='
MUL_EQUAL = '*='
DIV_EQUAL = '/='
#unary operators | done
INCRE = '++'
DECRE = '--'
#relational operators | done
E_EQUAL = '=='
NOT_EQUAL = '!='
LESS_THAN = '<'
GREATER_THAN = '>'
LESS_THAN_EQUAL = '<='
GREATER_THAN_EQUAL = '>='
#mathematical operators | done
PLUS = '+' #it can also use in string operator
MINUS = '-'
MUL = '*'
DIV = '/'
MODULUS = '%'
#logical operators
NOT_OP = '!'
AND_OP = '&&'
OR_OP = '||'
#other symbols
LPAREN = '('
RPAREN = ')'
SLBRACKET = '['
SRBRACKET = ']'
CLBRACKET = '{'
CRBRACKET = '}'
N_TAB = '\\t'
N_LINE = '\\n'
SHARP = '##'
Q_MARK = "\""
SQ_MARK = "\'"
S_COMET = '/*'
M_OPEN_COMET = '//*'
M_END_COMET =  '*//'
SEMICOLON = ';'
COLON = ':'
UNDERSCORE = "_"
NEWLINE= "\\n"
IN = ">>"
OUT = "<<"
TILDE = "~"

#literals

IDENTIFIER = 'IDENTI'
COMMA = ','
SPACE = "space"

EOF = 'EOF'

COMMENT = 'COMMENT'


class Error:
    def __init__ (self,pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self. details = details

    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        fileDetail = f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        errorDetail, arrowDetail = string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result, fileDetail, errorDetail, arrowDetail

class IllegalCharError(Error):
    #the lexer comes across a character it doesn't support
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character ', details)

class DelimiterError(Error):
    def __init__(self,pos_start, pos_end, details, char):
        super().__init__(pos_start, pos_end, f"Invalid Delimiter for '{char}'", "Cause -> " + str(details))
        
class InvalidSyntaxError(Error):
    def __init__(self,pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance (self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
    def __init__(self, token, value=None, pos_start=None, pos_end=None):
        self.token = token
        self.value = value
    
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end
    
    def __repr__(self):
        if self.value: return f'{self.value} : {self.token}'
        return f'{self.token}'


#LEXER

class Lexer:
    
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        # current char is the current pos if the pos is less than the length of the text
        self.current_char = self.text[self.pos.idx] if self.pos.idx <= len(self.text)-1 else None

    def make_tokens(self):
        
        tokens = []
        errors = []
        string = ""

        while self.current_char is not None:
            """ if self.current_char in special_chars:
                errors.extend([f"Invalid symbol: {self.current_char}"])
                self.advance() """
            # if self.current_char in ' \t':
            #     tokens.append(Token(N_TAB, "\\t", pos_start = self.pos))
            #     self.advance()
            if self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n", pos_start = self.pos))
                self.advance()
            #elif self.current_char in ' ':
              #  tokens.append(Token(SPACE, "\" \"", pos_start = self.pos))
             #   self.advance()
            elif self.current_char in all_letters:
                result, error = self.make_word()
                
                errors.extend(error)
                tokens.append(result)
                    
            elif self.current_char in all_num:
                result, error = self.make_number()
                
                errors.extend(error)
                
                
                if self.current_char == None or self.current_char == EOF:
                    errors.extend([f"Invalid delimiter for {result.value}. Cause: ' {self.current_char} '"])
                else:
                    tokens.append(result)
                
                    
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=, ==)
                self.advance()
                if self.current_char == '=':
                    
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (delim1 + '['):
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(E_EQUAL, "==")) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(EQUAL, "=", pos_start = self.pos)) #for == symbol
                        
                    
                    
            elif self.current_char == '<': #relational operator
                self.advance()        
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (delim2 + space_delim):
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(LESS_THAN_EQUAL, "<=")) #for == symbol
                elif self.current_char == '<':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' << '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' << '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(OUT, "<<", pos_start = self.pos))
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (delim2 + space_delim+alphanum):
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(LESS_THAN, "<"))
                    
                  
            elif self.current_char == '>': 
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(GREATER_THAN_EQUAL, ">="))
                elif self.current_char == '>':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' >> '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in all_letters+space_delim:
                        errors.extend([f"Invalid delimiter for ' >> '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(IN, ">>", pos_start = self.pos))
                    
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in alphanum + '(' + space_delim:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(GREATER_THAN, ">"))
                    
                
            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (delim1 + '['):
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(PLUS_EQUAL, "+=", pos_start = self.pos)) #for == symbol
                    
                elif self.current_char == '+': #for ++ incre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' ++ '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (lineEnd_delim + alphanum + ')'):
                        errors.extend([f"Invalid delimiter for '++'. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(INCRE, "++")) #for == symbol
                else:
    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' + '! Cause: {self.current_char}"])
                        continue
                        
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' + ' ! Cause: {self.current_char}"])
                        continue
                        
                    tokens.append(Token(PLUS, "+", pos_start = self.pos)) #for == symbol
                    
                        
                    
            elif self.current_char == '-': 
                self.advance()
                if self.current_char == '=': #for -=symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(MINUS_EQUAL, "-=", pos_start = self.pos)) 
                elif self.current_char == '-': #for -- decre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in (lineEnd_delim + alphanum + ')'):
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(DECRE, "--")) 
                elif self.current_char in all_num:
                    result, error = self.make_number()
                    result = Token(result.token, result.value * -1)
                    tokens.append(result)
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(MINUS, "-", pos_start = self.pos)) 
                
            elif self.current_char == '*': 
                self.advance()
                if self.current_char == "/":
                    self.advance()
                    if self.current_char == "/":
                        self.advance()
                        if self.current_char == None:
                            tokens.append(Token(M_END_COMET, "*//"))

                elif self.current_char == "=":
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(MUL_EQUAL, "*=", pos_start = self.pos)) 
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(MUL, "*", pos_start = self.pos))    
                        
                
                
            elif self.current_char == '/': 
                self.advance()
                if self.current_char == '=': #for /= symbol
                    
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(DIV_EQUAL, "/=", pos_start, self.pos))
                elif self.current_char == '/': #for 
                    self.advance()
                    if self.current_char == "*":
                        tokens.append(Token(M_OPEN_COMET, "//*"))
                        self.advance()# for multi comment
                        comment = ""
                        while self.current_char != "*":
                            
                            self.advance()
                            if self.current_char == "*":
                                break
                            if self.current_char == None:
                                break
                            comment += self.current_char
                            print("CURRENT CHAR IN TOKEN: ", self.current_char)
                        print("CURRENT CHAR AFTER LOOP: ", self.current_char)
                        
                        if self.current_char == "*":
                            self.advance()
                            if self.current_char == "/":
                                self.advance()
                                if self.current_char == "/":
                                    tokens.append(Token(COMMENT, f"{comment}"))# for single comet
                                    tokens.append(Token(M_END_COMET, "*//"))# for single comet
                                    self.advance()
                                else:
                                    continue
                            else:
                                continue
                elif self.current_char == "*":
                    tokens.append(Token(S_COMET, "/*", pos_start = self.pos))# for single comet
                    #self.advance()
                    comment = ""
                    while self.current_char != "\n":
                        self.advance()
                        comment += self.current_char
                        print("CURRENT CHAR IN TOKEN: ", self.current_char)
                    tokens.append(Token(COMMENT, f"{comment}"))# for single comet
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(DIV, "/"))
                
            elif self.current_char == '%':
                
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == None:
                    #errors.extend([f"Invalid delimiter for ' % '. Cause: ' {self.current_char} '"])
                    errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '%')])
                    #self.advance()
                    continue
                if self.current_char not in delim2:
                    errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '%')])
                    
                    continue
                tokens.append(Token(MODULUS, "%", pos_start=self.pos))
                
            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == '=':  
                    self.advance()
                    pos_start = self.pos.copy()
                    if self.current_char == None:
                        errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=')])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=')])
                        continue
                    tokens.append(Token(NOT_EQUAL, "!=")) #for != symbol
                else:
                    if self.current_char == None:
                        errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        continue
                    tokens.append(Token(NOT_OP, "!", pos_start = self.pos))
                    
            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' & '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' & '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(AND_OP, "&&"))
                    
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    #self.advance()
            elif self.current_char == '|': #return error
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '"])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '"])
                        continue
                    tokens.append(Token(OR_OP, "||"))
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    
            elif self.current_char == '(': #other operator
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in delim1 + ')' + alphanum + '':
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(LPAREN, "(",  pos_start = self.pos ))
            elif self.current_char == ')':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ) '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in closing_delim + '{' + ';' + space_delim + '\n' + ')':
                    errors.extend([f"Invalid delimiter for ' ) '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(RPAREN, ")", pos_start = self.pos))
            elif self.current_char == '[':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in delim0 + space_delim:
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(SLBRACKET, "["))
            elif self.current_char == ']':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in lineEnd_delim:
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(SRBRACKET, "]"))
            elif self.current_char == '{':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in delim3:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(CLBRACKET, "{", pos_start = self.pos))
            elif self.current_char == '}':
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(CRBRACKET, "}", pos_start = self.pos))
                    continue
                if self.current_char not in delim3:
                    errors.extend([f"Invalid delimiter for 'closing curly bracket'. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(CRBRACKET, "}", pos_start = self.pos))
            
            elif self.current_char == "\"":
                pos_start = self.pos.copy()
                string, error = self.make_string()
                tokens.append(Token(STRING, f"{string}", pos_start, self.pos))
                self.advance()
                # if self.current_char == None:
                #     errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '"])
                #     continue
                # if self.current_char not in lineEnd_delim+'),' + delim0:
                #     errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '"])
                #     continue
                # tokens.append(Token(Q_MARK, "\""))
                
                errors.extend(error)
                
            elif self.current_char == '\'':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' \' '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in lineEnd_delim+'),':
                    errors.extend([f"Invalid delimiter for ' \' '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(SQ_MARK, "\'"))
            elif self.current_char == ',':
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(COMMA, ",", pos_start = self.pos))
            elif self.current_char == ";":
                
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(SEMICOLON, ";", pos_start = self.pos))
                    continue
                if self.current_char not in newline_delim + space_delim + '}' + alphanum + "-+":
                    errors.extend([f"Invalid delimiter for ' ; '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(SEMICOLON, ";", pos_start = self.pos))
            elif self.current_char == ":":
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' : '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in newline_delim:
                    errors.extend([f"Invalid delimiter for ' : '. Cause: ' {self.current_char} '"])
                    continue
                #TODO fix delimiter
                tokens.append(Token(COLON, ":"))
            elif self.current_char == "~":
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '"])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '"])
                    continue
                tokens.append(Token(TILDE, "~"))

            else:
                #errors.extend([f"Invalid character: {self.current_char}"])
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                errors.extend([IllegalCharError(pos_start, self.pos, "'" + char  + "'" )])
                #errors.extend(IllegalCharError("'" + char  + "'" ))


        '''
        for item in tokens:
            if item.token != TAKEOFF:
                errors.extend(["Program cannot start without takeoff!"])
                break
            break
        
        
        if tokens[-1].token != LANDING:
            errors.extend(["Please input landing to end the program!"])
        
        '''
        '''
        if errors:
            return [], errors
        else:
        '''
        tokens.append(Token(EOF, pos_start = self.pos))
        return tokens, errors       

    def make_number(self):
        dec_count = 0
        num_count = 0
        num_str = ''
        dot_count = 0
        errors = []
        #not used ata to
        reached_limit_intel = False
        pos_start = self.pos.copy()
        

        while self.current_char is not None and self.current_char in all_num + '.':
            if dec_count == 4:
                if dot_count == 0:
                    if self.current_char in all_num:
                        errors.append(f"Invalid number delimiter for'{num_str}'. Cause: {self.current_char}")
                        
                        return [], errors
                    else:
                        Token(INTEL, int(num_str), pos_start, self.pos), errors
                else:
                    if self.current_char in all_num:
                        errors.append(f"Invalid number delimiter for'{num_str}'. Cause: {self.current_char}")
                        
                        return [], errors
                    else:
                        return Token(GRAVITY, float(num_str), pos_start, self.pos), errors
            if num_count == 9:
                
                if self.current_char in all_num:
                    errors.append(f"Invalid number delimiter for'{num_str}'. Cause: {self.current_char}")
                    
                    return [], errors
                    
            if self.current_char == '.':
                if dot_count == 1: 
                    errors.append(f"Invalid character '{self.current_char}' in number.")
                    break
                dot_count += 1
                num_str += '.'
                
            else:
                if '.' in num_str:
                    if num_count > 9:
                        break   
                    dec_count += 1
                    num_count -= 1
                
                num_count += 1
                num_str += self.current_char
            self.advance()
        
        # check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            # while self.current_char is not None and self.current_char.isalpha():
            #     num_str += self.current_char
            #     #added this advance para maskip nya yung identifier if ever
            #     self.advance()
            errors.append(f"Invalid delimiter for number: {num_str}")    
            if errors:
                return [], errors
               
            

       #TODO need maread kapag may 0
            if dot_count == 0:
                #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
                return Token(INTEL, int(num_str), pos_start, self.pos), errors
            else:
                return Token(GRAVITY, float(num_str), pos_start, self.pos), errors
        
        if dot_count == 0:
            #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
            return Token(INTEL, int(num_str), pos_start, self.pos), errors
        else:
            return Token(GRAVITY, float(num_str), pos_start, self.pos), errors
       
        
    #takes in the input character by character then translates them into words then tokens
    def make_word(self):
        
        ident = ""  
        ident_count = 0
        errors = []
        
        while self.current_char != None:
            #here cinocontrol number ng identifiers
            if ident_count == 10:
                #errors.extend([f"Exceeded identifier limit! Limit: 10 characters. Characters entered: {ident_count}. Cause: {ident}"]) 
                ident += self.current_char
                self.advance()
                if self.current_char in space_delim + ident_delim + ';' +'(,' + '\n':  
                       
                    return Token(IDENTIFIER, ident, pos_start = self.pos), errors
                else:
                    
                    errors.extend([f"Invalid delimiter for: {ident}. Cause: {self.current_char}"])
                    
                    break
                
           
            
            if self.current_char == "b":
                if ident_count == 10:
                    break
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "l":
                    if ident_count == 10:
                        break
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "a":
                        if ident_count == 10:
                            break
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "s":
                            if ident_count == 10:
                                break
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "t":
                                if ident_count == 10:
                                    break
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for blast! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in lineEnd_delim:
                                    errors.extend([f'Invalid delimiter for blast! Cause: {self.current_char}'])
                                    return [], errors

                                return Token(BLAST, "blast", pos_start = self.pos), errors
                            
                                
                
            if self.current_char == "d": #do
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == None:
                        errors.extend([f'Invalid delimiter for do! Cause: {self.current_char}'])
                        return [], errors
                    if self.current_char not in block_delim:
                        errors.extend([f'Invalid delimiter for do! Cause: {self.current_char}'])
                        return [], errors
                    return Token(DO, "do", pos_start = self.pos), errors
                
                
            if self.current_char == "e": #else, else if, entity
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "l":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "s":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "i":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "f":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for elseif! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in block_delim + "(":
                                        errors.extend([f'Invalid delimiter for elseif! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(ELSEIF, "elseif"), errors
                            else:
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for else! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in block_delim:
                                    errors.extend([f'Invalid delimiter for else! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(ELSE, "else"),errors
                            
                elif self.current_char == "n":
                    if ident_count == 10:
                        break
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "t":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "y":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for entity! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in block_delim:
                                        errors.extend([f'Invalid delimiter for entity! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(ENTITY, "entity"), errors
                                    
                
            if self.current_char == "i": #if, inner, intel
                ident += self.current_char
                self.advance()
                ident_count += 1 
                if self.current_char == "f":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == None:
                        errors.extend([f'Invalid delimiter for if! Cause: {self.current_char}'])
                        return [], errors
                    if self.current_char not in loop_delim:
                        errors.extend([f'Invalid delimiter for if! Cause: {self.current_char}'])
                        return [], errors
                    return Token(IF, "if", pos_start = self.pos), errors
                elif self.current_char == "n":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for inner! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in inner_delim:
                                    errors.extend([f'Invalid delimiter for inner! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(INNER, "inner", pos_start = self.pos), errors
                        
            if self.current_char == "f": #false, force, form
                ident += self.current_char
                self.advance()
                ident_count += 1 
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "s":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in bool_delim + ',':
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(FALSE, "false", pos_start = self.pos), errors
                            
                            
                    
                elif self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "c":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for force! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in loop_delim:
                                    errors.extend([f'Invalid delimiter for force! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(FORCE, "force"), errors
                            

                        elif self.current_char == "m":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for form! Cause: {self.current_char}'])
                                    return [], errors
                            if self.current_char not in space_delim:
                                errors.extend([f'Invalid delimiter for form! Cause: {self.current_char}'])
                                return [], errors
                            return Token(FORM, "form", pos_start = self.pos), errors
                        
            if self.current_char == "g": #landing, launch
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "a":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "x":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "y":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for galaxy! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in "( " + space_delim:
                                        errors.extend([f'Invalid delimiter for galaxy! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(GALAXY, "galaxy", pos_start = self.pos), errors               
                
            if self.current_char == "l": #landing, launch
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "i":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "n":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "g":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == None:
                                            errors.extend([f'Invalid delimiter for landing! Cause: {self.current_char}'])
                                            return [], errors
                                        if self.current_char not in lineEnd_delim:
                                            errors.extend([f'Invalid delimiter for landing! Cause: {self.current_char}'])
                                            return [], errors
                                        return Token(LANDING, "landing", pos_start = self.pos), errors
                                    
                    elif self.current_char == "u": #launch
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "n":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "c":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "h":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for launch! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in space_delim:
                                        errors.extend([f'Invalid delimiter for launch! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(LAUNCH, "launch"), errors
                                    
                
            if self.current_char == "o": #outer
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "u":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for outer! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in outer_delim:
                                    errors.extend([f'Invalid delimiter for outer! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(OUTER, "outer"), errors
                
            if self.current_char == "s": #saturn, shift, skip, star
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "u":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "n":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for saturn! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in lineEnd_delim:
                                        errors.extend([f'Invalid delimiter for saturn! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(SATURN, "saturn", pos_start = self.pos), errors
                
                elif self.current_char == "h":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "f":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "t":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for shift! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in loop_delim:
                                        errors.extend([f'Invalid delimiter for shift! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(SHIFT, "shift"), errors

                elif self.current_char == "k":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "p":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for skip! Cause: {self.current_char}'])
                                        return [], errors
                                if self.current_char not in lineEnd_delim:
                                    errors.extend([f'Invalid delimiter for skip! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(SKIP, "skip"), errors
            
            if self.current_char == "t": #takeoff, trace, true
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "k":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "o":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "f":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "f":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == None:
                                            errors.extend([f'Invalid delimiter for takeoff! Cause: {self.current_char}'])
                                            return [], errors
                                        if self.current_char not in lineEnd_delim:
                                            errors.extend([f'Invalid delimiter for takeoff! Cause: {self.current_char}'])
                                            return [], errors
                                        return Token(TAKEOFF, "takeoff", pos_start=self.pos), errors
                    
                elif self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "a":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "c":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "e":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for trace! Cause: {self.current_char}'])
                                        return [], errors
                                    if self.current_char not in space_delim:
                                        errors.extend([f'Invalid delimiter for trace! Cause: {self.current_char}'])
                                        return [], errors
                                    return Token(TRACE, "trace"), errors
                                
                        elif self.current_char == "u":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()     
                                ident_count += 1    
                                if self.current_char == None:
                                        errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}'])
                                        return [], errors
                                if self.current_char not in bool_delim + ',':
                                    errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(TRUE, "true", pos_start = self.pos), errors
                
            if self.current_char == "u": #universe
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "n":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "v":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "r":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    if self.current_char == "s":
                                        ident += self.current_char
                                        self.advance()
                                        ident_count += 1
                                        if self.current_char == "e":
                                            ident += self.current_char
                                            self.advance()
                                            ident_count += 1
                                            if self.current_char == None:
                                                errors.extend([f'Invalid delimiter for universe! Cause: {self.current_char}'])
                                                return [], errors
                                            if self.current_char not in space_delim:
                                                errors.extend([f'Invalid delimiter for universe! Cause: {self.current_char}'])
                                                return [], errors
                                            return Token(UNIVERSE, "universe", pos_start =self.pos), errors
                
            if self.current_char == "v": #void
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                errors.extend([f'Invalid delimiter for void! Cause: {self.current_char}'])
                                return [], errors
                            if self.current_char not in bool_delim:
                                errors.extend([f'Invalid delimiter for void! Cause: {self.current_char}'])
                                return [], errors
                            return Token(VOID, "void"), errors
                        
                elif self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == None:
                            errors.extend([f'Invalid delimiter for var! Cause: {self.current_char}'])
                            return [], errors
                        if self.current_char not in space_delim:
                            errors.extend([f'Invalid delimiter for var! Cause: {self.current_char}'])
                            return [], errors
                        return Token(VAR, "var", pos_start = self.pos), errors
                  
                            
            if self.current_char == "w": #whirl
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "h":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "r":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "l":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for whirl! Cause: {self.current_char}'])
                                    return [], errors
                                if self.current_char not in loop_delim:
                                    errors.extend([f'Invalid delimiter for whirl! Cause: {self.current_char}'])
                                    return [], errors
                                return Token(WHIRL, "whirl", pos_start = self.pos), errors
                else:
                    ident_count += 1
                    if ident_count > 10:
                        errors.extend([f"Exceeded identifier limit! Characters entered: {ident_count}"])
                        
                       
            
            else:
                if ident_count == 10:
                    errors.extend([f"Invalid delimiter for: {ident}. Cause: {self.current_char}"])           
                    return [], errors
                
                if self.current_char == None:
                    break
                if self.current_char in (lineEnd_delim + ident_delim + CLBRACKET + CRBRACKET + space_delim + '(' + ':' + '\n'):
                    break
               
                
                if self.current_char in "\n":
                    break
                
                if self.current_char == UNDERSCORE:
                    ident_count += 1
                    ident += str(self.current_char)
                    self.advance()
                if self.current_char.isdigit() == True:
                    ident_count += 1
                    ident += str(self.current_char)
                    self.advance()
                else:
                    ident_count += 1
                    ident += self.current_char
                    self.advance()

                for item in ident:
                    if item in ident_special_chars:
                        errors.extend([f"Identifiers cannot have special characters! Cause: {item}"])
                        return [], errors
        
                        
        ###self.advance()
        if self.current_char == None:
            errors.extend([f"Invalid delimiter for {ident}. Cause: ' {self.current_char} '"])
            return [], errors
        
        

             
        # if ident_count == 10:
        #     #errors.extend([f"Exceeded identifier limit! Limit: 10 characters. Characters entered: {ident_count}. Cause: {ident}"])           
        #     return Token(IDENTIFIER, ident), errors

        
        if errors:
            return [], errors
        else:
            return Token(IDENTIFIER, ident, pos_start = self.pos), errors
        #print(ident_count)
        # pwede return Token(IDENTIFIER, ident), errors dito basta dalawa den yung value sa nag call (ex: result, error = cat.make_word)
        #
            
    def make_string(self):
        
        string = ""
        errors = []
        self.advance()
        while self.current_char != "\"" and self.current_char != None :
            
            string += self.current_char
            self.advance()
        if self.current_char == "\"":
            return string, errors

        else:
            errors.append("Expected closing quotation mark!")
            return [], errors
       
                  
#NODES
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self) -> str:
        return f'{self.tok}'
    

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self. right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

#PARSE RESULT

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        
        return res
    
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#PARSER
    
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.if_stmt_encountered = False
        self.landing = False

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    #* parse takes the list of tokens then  deciedes which functions to execute based on the token
    def parse(self):
        res =  []
        error = []

        while self.current_tok.token == NEWLINE:
            self.advance()
            
        if self.current_tok.token == S_COMET:
            
            print("FOUND A COMMENT TOKEN IN PARSE")
            self.advance()
            while self.current_tok.token != NEWLINE:
                self.advance()
            self.advance()
            print("after comment:", self.current_tok)
        if self.current_tok.token == M_OPEN_COMET:
            while self.current_tok.token != M_END_COMET:
                self.advance()
                
        
        
        if self.current_tok.token != TAKEOFF:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Type 'takeoff' start the program!"))
            return [], error
        else:
            self.advance()
            if self.current_tok.token != SEMICOLON:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon!"))
                return [], error
            else:
                self.advance()
                
            

        # * basically yung parse lang pero walang form

        while True:
            # if self.current_tok.token == SEMICOLON:
            #     print("semicolon")
            #     self.advance()
            if self.current_tok.token == M_OPEN_COMET:
                while self.current_tok.token != M_END_COMET:
                    self.advance()
                    if self.current_tok.token == EOF:
                        break
                self.advance()

            if self.current_tok.token != S_COMET and self.current_tok.token != NEWLINE and self.current_tok.token != S_COMET and self.current_tok.token != UNIVERSE and self.current_tok.token != VAR and self.current_tok.token != FORM and self.current_tok.token != GALAXY and self.current_tok.token != M_OPEN_COMET and self.current_tok.token != M_END_COMET and self.current_tok.token !=  LANDING :
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid syntax outside galaxy!"))
                break
            else:
                self.advance()
                
            if self.current_tok.token == S_COMET:
            
                print("FOUND A COMMENT TOKEN IN PARSE")
                self.advance()
                while self.current_tok.token != NEWLINE:
                    self.advance()
                self.advance()
                print("after comment:", self.current_tok)
        
            
                     
            #VAR DECLARATION  DAT MAY GLOBAL
            if self.current_tok.token in UNIVERSE:
                self.advance()          
                if self.current_tok.token in VAR: 
                    print("this is a var token")
                    var, var_error = self.var_dec()
                    if var_error:
                        error.extend(var_error)
                        break
                    #res.append(var)
                    #self.advance()
                    print("current token from global var dec parse: ", self.current_tok)
                    
                    if self.current_tok.token != SEMICOLON:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon from var dec parse!"))
                    else:
                        self.advance()
                        res.append(["SUCCESS from global declaration!"])
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid global variable declaration!"))
                    break

            # ? pwede i-bring back pag need specific
            # if self.current_tok.token in VAR:
            #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid global declaration!"))
            #     break
            
            

            #functions
            if self.current_tok.token == FORM:
                print("youve got a form token")
                form_res, form_error = self.init_form()

                if form_error:
                    for err in form_error:
                        error.append(err)
                    break
                else:
                    res.extend(form_res)

            if self.current_tok.token == GALAXY:
                
                print("youve got a galaxy token")
                g_res, g_error = self.galaxy()

                if g_error:
                    for err in g_error:
                        error.append(err)
                    break
                else:
                    res.extend(g_res)

            if self.current_tok.token == LANDING:
                self.advance()
                if self.current_tok.token == SEMICOLON:
                    self.landing = True
                    return res, error
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Semicolon expected for 'landing'!"))
            
            # if self.current_tok.token == CRBRACKET:
            #     break

            if self.current_tok.token == EOF:
                # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "INVALID MAIN SCOPE"))
                break

        if self.current_tok.token == EOF:
            if self.landing ==  True:
                return res, error
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'landing' to end the program!"))
                return res, error



        return res, error
    
    #* controls what happens when the compiler encounters the galaxy token
    def galaxy(self):
        res = []
        error = []
        self.advance()
        #print("init form tok:  ", self.current_tok.token)
        
        if self.current_tok.token == LPAREN:
            print("found left paren")
            self.advance()
            
            if self.current_tok.token == IDENTIFIER:
                #self.advance()
                print("current token from form is: ", self.current_tok.token)
                self.advance()
                if self.current_tok.token == COMMA:
                    print("you found a comma in the params!")
                    #if comma yung current, find identifier, next, then if comma, next, and repeat
                    c_error = self.comma()
                    if c_error:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                    
                    print("current token after comma: ", self.current_tok.token)
                if self.current_tok.token != RPAREN:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                    self.advance()
                else: 
                    #res.append("SUCCESS from form!")
                    self.advance()
                    if self.current_tok.token in NEWLINE:
                        self.advance()
                    if self.current_tok.token == CLBRACKET:
                        print("left curly bracket")
                        
                        self.advance()

                        while self.current_tok.token == NEWLINE:
                            self.advance()
                        form_res, form_error = self.body()
                        print("form res: ", res)
                        if form_error:
                            print("THERES  AN ERROR INSIDE THE FUNCTION SCOPE")
                            for err in form_error:
                                error.append(err)
                            return [], error
                        else:
                            print("successful galaxy!")
                            for f_res in form_res:
                                res.extend(f_res)
                                print("f res: ", f_res)
                            
                        
                        print("CURRENT TOK FROM GALAXY: ", self.current_tok)
                        if self.current_tok.token != CRBRACKET:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets in galaxy!"))
                            
                        else:
                            res.append("SUCCESS from GALAXY!")
                            self.advance()
                            
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Galaxy definition missing!"))
                        self.advance()
            elif self.current_tok.token == RPAREN:
                self.advance()
                if self.current_tok.token in NEWLINE:
                    self.advance()
                if self.current_tok.token == CLBRACKET:
                    print("left curly bracket")
                    
                    self.advance()

                    while self.current_tok.token == NEWLINE:
                        self.advance()
                    form_res, form_error = self.body()
                    print("form res: ", form_res)
                    if form_error:
                        print("THERES  AN ERROR INSIDE THE FUNCTION SCOPE")
                        for err in form_error:
                            error.append(err)
                        return [], error
                    else:
                        print("successful galaxy!")
                        for f_res in form_res:
                            res.extend(f_res)
                            print("f res: ", f_res)
                            
                        
                        print("CURRENT TOK FROM FORM: ", self.current_tok)
                        if self.current_tok.token != CRBRACKET:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets in galaxy!"))
                            
                        else:
                            res.append("SUCCESS from GALAXY!")
                            self.advance()
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Galaxy definition missing!"))
                    self.advance()

            #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parameter id!"))   
        #form add(a, b)
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parentheses for parameters!"))
            return res, error
    
        return res, error

    #* body controls the user defined functions as well as the main gaalxy function
    def body(self):
        res =  []
        error = []

        
        # * basically yung parse lang pero walang form

        while True:
            if self.is_statement():
                if self.current_tok.token == M_OPEN_COMET:
                    print("found multi line comment")
                    while self.current_tok.token != M_END_COMET:
                        self.advance()
                        if self.current_tok.token == EOF:
                            break
                    self.advance()
                if self.current_tok.token == S_COMET:
                    self.advance()
                    while self.current_tok.token != NEWLINE:
                        self.advance()
                # if self.current_tok.token == SEMICOLON:
                #     print("semicolon")
                #     self.advance()
                if self.current_tok.token == NEWLINE:
                    self.advance()

                #not working yung intel
                if self.current_tok.token in INTEL:
                    res = self.expr()
                    print("this is a binary operation")

                #--INITIALIZATION OF IDENTIFIERS
                if self.current_tok.token == IDENTIFIER:
                    self.advance()
                    #-- if it's a function call
                    if self.current_tok.token == LPAREN:
                        c_form, call_form_error = self.call_form()
                        print("token after call form: ", self.current_tok.token)
                        #self.advance()
                        print('call form result:', c_form)
                        if call_form_error:
                            error.extend(call_form_error)
                            break
                        else:
                            self.advance()
                            if self.current_tok.token in SEMICOLON:
                                res.append(c_form)
                                self.advance()
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon in call form!"))

                        
                    #-- if we assign a value to it but not declaring it           
                    elif self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL or self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
                        print("initialize the variable")
                        assign, a_error = self.init_var()

                        if a_error:
                            error.extend(a_error)
                            break
                        res.append(assign)
                    #-- if we increment it
                    elif self.current_tok.token == INCRE:
                        self.advance()
                        if self.current_tok.token != SEMICOLON:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon!"))
                        else:
                            res.append(["SUCCESS from unary post increment"])
                            self.advance()
                    #-- if we decrement it
                    elif self.current_tok.token == DECRE:
                        self.advance()
                        if self.current_tok.token != SEMICOLON:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon!"))
                        else:
                            res.append(["SUCCESS from unary post decrement"])
                            self.advance()
                    # -- else no other operation for it
                    else:
                        print('INVALID IDENT OPERATION')
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid identifier operation!"))
                        return [], error

                if self.current_tok.token == INCRE:
                    self.advance()
                    if self.current_tok.token == IDENTIFIER:
                        self.advance()
                        if self.current_tok.token != SEMICOLON:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon!"))
                        else:
                            res.append(["SUCCESS from unary pre increment"])
                            self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid unary statement!"))

                if self.current_tok.token == DECRE:
                    self.advance()
                    if self.current_tok.token == IDENTIFIER:
                        self.advance()
                        if self.current_tok.token != SEMICOLON:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon!"))
                        else:
                            res.append(["SUCCESS from unary pre decrement"])
                            self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid unary statement!"))
                #LOOPS
                if self.current_tok.token in FORCE:
                    print("this is a force statement")
                    force_res, force_error = self.force_stmt()
                    self.advance()

                    if force_error:
                        error.extend(force_error)
                        break
                    else:
                        for fres in force_res:
                            res.append(fres)
                            #self.advance()
                            print("current token from force dec parse: ", self.current_tok)
                    
                    
                if self.current_tok.token in WHIRL:
                    self.advance()
                    w_res, w_error = self.whirl()
                    print("token after whirl:", self.current_tok)
                    if w_error:
                        for err in w_error:
                            error.append(err)
                        return [], error
                    else:
                        #res.append(w_res)
                        self.advance()
                        if self.current_tok.token == CLBRACKET:
                            self.advance()
                            w_result, w_err = self.body()
                            print("w res: ", res)
                            if w_err:
                                print("THERES  AN ERROR INSIDE THE WHIRL SCOPE")
                                for err in w_err:
                                    error.append(err)
                                return [], error
                            else:
                                print("successful whirl!")
                                for w in w_result:
                                    res.append(w)
                                    print("whirl res: ", w_res)
                                #res.append(["SUCCESS from whirl!!"])
                                print("whirl bracket?: ", self.current_tok)
                                if self.current_tok.token != CRBRACKET:
                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket for whirl!"))
                                    return [], error
                                else:
                                    res.append(["SUCCESS from whirl"])
                                    self.advance()
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected scope for whirl!"))
                
                
                if self.current_tok.token == DO:
                    print("there's a do token!")
                    self.advance()
                    do_res, do_err = self.do_whirl()
                    if do_err:
                        for err in do_err:
                            error.append(err)
                        return [], error
                    else:
                        self.advance()
                        res.append(do_res)
                
                if self.current_tok.token in OUTER:
                    print("this is an outer statement")
                    outer_res, outer_error = self.outer_stmt()
                    self.advance()
                    if outer_error:
                        error.extend(outer_error)
                        break
                    res.append(outer_res)

                #CONDITIONAL
                if self.current_tok.token in IF:
                    print("this is an if statement")
                    if_res, if_error = self.if_stmt()
                    self.advance() 

                    if if_error:
                        error.extend(if_error)
                        break
                    else:
                        for fres in if_res:
                            res.append(fres)
                            #self.advance()
                            print("current token from if parse: ", self.current_tok)

                if self.current_tok.token in ELSE:
                    print("this is an else statement")
                    else_res, else_error = self.else_stmt()
                    self.advance()

                    if else_error:
                        error.extend(else_error)
                        break
                    else:
                        for fres in else_res:
                            res.append(fres)
                            print("current token from if parse: ", self.current_tok)
                        self.advance()

                if self.current_tok.token in ELSEIF:
                    print("this is an elif statement")
                    elif_res, elif_error = self.elif_stmt()
                    self.advance()

                    if elif_error:
                        error.extend(elif_error)
                        break
                    else:
                        for fres in elif_res:
                            res.append(fres)
                            print("current token from elseif parse: ", self.current_tok)
                        self.advance()

                #INPUT OUTPUT
                if self.current_tok.token in INNER:
                    print("this is an inner statement")
                    res, error = self.inner_stmt()
                    self.advance()

                        
                # VAR DECLARATION            
                if self.current_tok.token in VAR: 
                    print("this is a var token")
                    var, var_error = self.var_dec()
                    if var_error:
                        error.extend(var_error)
                        break
                    #res.append(var)
                    #self.advance()
                    print("current token from var dec parse: ", self.current_tok)
                    
                    if self.current_tok.token != SEMICOLON:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon from var dec body!"))
                    else:
                        self.advance()
                        res.append(["SUCCESS from variable declaration!"])
                
                
                if self.current_tok.token in FORM:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "You can't declare a function within a function!"))
                    break
                
                if self.current_tok.token == SATURN:
                    self.advance()
                    if self.current_tok.token != INTEL and self.current_tok.token != IDENTIFIER and self.current_tok.token != TRUE and self.current_tok.token != FALSE and self.current_tok.token != STRING:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid return value!"))
                        break
                    else:
                        self.advance()
                        if self.current_tok.token != SEMICOLON:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon!"))
                        else:
                            res.append(["SUCCESS! from saturn"])
                            self.advance()
                        
                if self.current_tok.token == LANDING:
                    self.advance()
                    if self.current_tok.token == SEMICOLON:
                        self.landing = True
                        return res, error
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Semicolon expected for 'landing'!"))

                if self.current_tok.token == CRBRACKET:
                    break

                if self.current_tok.token == EOF:
                    # error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "INVALID MAIN SCOPE"))
                    break
            
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please follow proper syntax!"))
                break


        return res, error
    
    # * checks if the current token's a valid statement in body
    def is_statement(self):
        if self.current_tok.token == S_COMET or self.current_tok.token == NEWLINE or self.current_tok.token in INTEL or self.current_tok.token == IDENTIFIER or self.current_tok.token in FORCE or self.current_tok.token in WHIRL or self.current_tok.token in WHIRL or self.current_tok.token in OUTER or self.current_tok.token in IF or self.current_tok.token in ELSE or self.current_tok.token in ELSEIF or self.current_tok.token in INNER or self.current_tok.token in VAR or self.current_tok.token in SATURN or self.current_tok.token in FORM or self.current_tok.token in CRBRACKET or self.current_tok.token in EOF or self.current_tok.token == DO or self.current_tok.token == WHIRL or self.current_tok.token == INCRE or self.current_tok.token == DECRE  or self.current_tok.token == COMMENT or self.current_tok.token == M_OPEN_COMET or self.current_tok.token == M_END_COMET or self.current_tok.token ==LANDING:
            return True
        else:
            return False

    #* initialize a variable
    def init_var(self):
        
        res = []
        error = []
        
        if self.current_tok.token == EQUAL or self.current_tok.token == PLUS_EQUAL:
            print("in init var")
            # -- pag equal lang pwede string
            # * DONE
            self.advance()
            assign, err = self.assign_val()
            print("assign: ", err)
            if err:
                #error.append(err)
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Please check your initialization!"))

                
            else:
                print("init var: ",self.current_tok )
                if self.current_tok.token != SEMICOLON:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon! from init var"))
                else:
                    res.append("SUCCESS! from assign")
                    self.advance()
        elif self.current_tok.token == MINUS_EQUAL or self.current_tok.token == MUL_EQUAL or self.current_tok.token == DIV_EQUAL:
            #-- use assign val pero bawal dapat sa string
            #* DONE
            assign, err = self.assign_val2()
            if err:
                error.append(err)
                
            else:
                print("init var: ",self.current_tok )
                if self.current_tok.token != SEMICOLON:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon! from init var"))
                else:
                    res.append("SUCCESS! from assign")
                    self.advance()
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid initialization! from initialize variable"))
        return res, error
    
    #*declare a variable
    def var_dec(self):
        res = []
        error = []
        # -- token when entering this function is 'var'
        self.advance()

        # -- if the user doesnt type an identiifier after 'var'
        if self.current_tok.token != IDENTIFIER:
            print("bro put an identifier!")
            print("current tok: ", self.current_tok.token)
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "PLS GIVE ME AN IDENTIFIER "))
        else:
            print("u good")
            self.advance()
            if self.current_tok.token == EQUAL or self.current_tok.token == COMMA:
                if self.current_tok.token == EQUAL:
                    print("value after equal: ", self.current_tok)
                    # -- USED SELF ASSIGN VAL 1
                    self.advance()
                    assign,err = self.assign_val()
                    if err:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid initialization!"))
                        
                    else:
                        #self.advance()
                        print("CURRENT TOKEN FROM VAR DEC INIT: ", self.current_tok)
                        if self.current_tok.token == COMMA:
                            print("comma after init!")
                            comma, c_error = self.var_dec()
                            print('FROM  VAR  DEC CURRENT TOKEN: ', self.current_tok)
                            
                            if c_error:
                                for err in c_error:
                                    error.append(err)
                            else:
                                for c in comma:
                                    res.append(c)
                    
                elif self.current_tok.token == COMMA:
                    print("there's a comma here")
                    comma, c_error = self.var_dec()
                    print('FROM  VAR  DEC CURRENT TOKEN: ', self.current_tok)
                    
                    if c_error:
                        for err in c_error:
                            error.append(err)
                    else:
                        for c in comma:
                            res.append(c)
            # else:
            #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid initialization!"))

                #res.append("SUCCESS! from variable declaration")
    

        return res, error
    
    #* assign a value of a variable
    def assign_val(self):
        res=[]
        error =[]
        #print ("VALUE ASSIGNED FROM  ASSIGN_VAL")
        #self.advance()
        if self.current_tok.token == STRING:
            print("string here")
            self.advance()
            print("operator", self.current_tok)
            while self.current_tok.token in PLUS:
                print("IN THE STRING LOOP for concatenation")
                self.advance()
                if self.current_tok.token == STRING or self.current_tok.token == IDENTIFIER:
                    self.advance()
                else:
                    #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier or string!"))

            return res, error
        if self.current_tok.token == INTEL or self.current_tok.token == GRAVITY or self.current_tok.token == IDENTIFIER:
            
            if self.current_tok.token == INTEL or self.current_tok.token == GRAVITY:
                print("found a number in assign val 2")
                self.advance()
                check, err = self.num_loop()
                if err:
                    print("FOUND AN ERROR IN NUM LOOP")
                    #return False
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM NUM LOOP!"))
                    return res, error

                else:
                    print("checked")
                    #self.advance()
                    print("after checked: ", self.current_tok)
                    res.append(["okay yung num loop!"])
                
                
                
            elif self.current_tok.token == IDENTIFIER:
                print("first value in assign val is an identifier")
                self.advance()
                if self.current_tok.token == LPAREN:
                    print("we assigned a function call to a variable")
                    c_form, call_form_error = self.call_form()
                    print("token after call form in assign val: ", self.current_tok.token)
                    #self.advance()
                    print('call form result in assign val:', c_form)
                    if call_form_error:
                        print("ERROR IN VALL FORM")
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM call form!"))
                        
                    else:
                        print("no error after function call: ", self.current_tok)
                        self.advance()
                        #print("found operator after function call")
                        if self.current_tok.token in (MUL, DIV, PLUS, MINUS, MODULUS):
                            # -- USED SELF.ASSIGN_VAL()
                            self.advance()
                            check, err = self.assign_val2()
                            if  err:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid assign val!"))

                            else:
                                res.append("Success form ident assign!")
                        return res, error
                else:
                    print('FIRST OPERAND IS AN IDENTIFIER')
                    num, err = self.num_loop()
                    if err:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
                    else:
                        res.append("Success form ident assign!")

        elif self.current_tok.token == LPAREN:
            print("PARENTHESIS IN ASSIGN")
            self.advance()
            check, err = self.assign_val2()
            #self.advance()
                
            if err:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
                

            else:
                if self.current_tok.token == RPAREN:
                    print("found closing")
                    self.advance()
                    
                    if self.current_tok.token in (PLUS, MINUS, DIV, MUL):
                        print("found operator  after paren")
                        self.advance()
                        num, err = self.assign_val2()
                        if  err:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid assign val!"))

                        else:
                            res.append("Success form ident assign!")

                    return res, error
                    
                        
                    #return True
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "No closing paren!"))
        elif self.current_tok.token == TRUE:
            self.advance()
            return res, error
        elif self.current_tok.token == FALSE:
            self.advance()
            return res, error
        
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
    
        return res, error
        
    
    def assign_val2(self):
        res = []
        error = []

        print("im in assign val 2: ", self.current_tok)
        
        if self.current_tok.token == INTEL or self.current_tok.token == GRAVITY or self.current_tok.token == IDENTIFIER:
            
            if self.current_tok.token == INTEL or self.current_tok.token == GRAVITY:
                print("found a number in assign val 2")
                self.advance()
                check, err = self.num_loop()
                if err:
                    print("FOUND AN ERROR IN NUM LOOP")
                    #return False
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM NUM LOOP!"))
                    return res, error

                else:
                    print("checked")
                    #self.advance()
                    print("after checked: ", self.current_tok)
                    res.append(["okay yung num loop!"])
                
                
                
            elif self.current_tok.token == IDENTIFIER:
                print("first value in assign val is an identifier")
                self.advance()
                if self.current_tok.token == LPAREN:
                    print("we assigned a function call to a variable")
                    c_form, call_form_error = self.call_form()
                    print("token after call form in assign val: ", self.current_tok.token)
                    #self.advance()
                    print('call form result in assign val:', c_form)
                    if call_form_error:
                        print("ERROR IN VALL FORM")
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM call form!"))
                        
                    else:
                        self.advance()
                        print("FOUND FORM CALL OPERAND HERE")
                        if self.current_tok.token in (MUL, DIV, PLUS, MINUS, MODULUS):
                            # -- USED SELF.ASSIGN_VAL()

                            check, err = self.assign_val2()
                            if  err:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid assign val!"))

                            else:
                                res.append("Success form ident assign!")
                        return res, error
                else:
                    print('FIRST OPERAND IS AN IDENTIFIER')
                    num, err = self.num_loop()
                    if err:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
                    else:
                        res.append("Success form ident assign!")

        elif self.current_tok.token == LPAREN:
            print("PARENTHESIS IN ASSIGN")
            self.advance()
            check, err = self.assign_val2()
            #self.advance()
                
            if err:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
                

            else:
                if self.current_tok.token == RPAREN:
                    print("found closing")
                    self.advance()
                    
                    if self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
                        print("found operator  after paren")
                        self.advance()
                        num, err = self.assign_val2()
                        if  err:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid assign val!"))

                        else:
                            res.append("Success form ident assign!")

                    return res, error
                    
                        
                    #return True
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "No closing paren!"))
        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM assign val2!"))
    
        return res, error
        
    def num_loop(self):
        res = []
        error = []
        ops = "-/*%"
        print("current tok in num loop: ", self.current_tok)
        while self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
            self.advance()
            if self.current_tok.token in (INTEL, GRAVITY, IDENTIFIER):
                self.advance()
            elif self.current_tok.token == LPAREN:
                self.advance()
                num = self.assign_val2()
                if num:
                    if self.current_tok.token == RPAREN:
                        print("found closing")
                        self.advance()
                        
                        if self.current_tok.token in (PLUS, MINUS, DIV, MUL, MODULUS):
                            print("found operator  after paren: ",  self.current_tok)
                            self.advance()
                            num = self.assign_val2()
                            if  num:
                                return res, error
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM ASSIGN VAL!"))

                                #return False
                        return res, error
                        
                            
                        #return True
                    else:
                        #return False
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM NUM LOOP!"))
                else:
                    #return False
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM NUM LOOP!"))
            # elif self.current_tok.token == RPAREN:
            #     print("found rparen")
            #     break
            elif self.current_tok.token == STRING:
                if "-" in ops or "/" in ops or "%" in ops or "*" in ops:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid string operation!"))

                else:
                    self.advance()
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "ERROR FROM NUM LOOP!"))
                return res, error

        
            # else:
            #     return False
        print("end the num lop value: ", self.current_tok)
        return res, error
          

    #* DECLARING A FORM
    def init_form(self):
        res = []
        error = []
        self.advance()
        #print("init form tok:  ", self.current_tok.token)
        if self.current_tok.token == IDENTIFIER:
            print("form name found")
            self.advance()
            if self.current_tok.token == LPAREN:
                print("found left paren")
                self.advance()
                
                if self.current_tok.token == IDENTIFIER:
                    #self.advance()
                    print("current token from form is: ", self.current_tok.token)
                    self.advance()
                    if self.current_tok.token == COMMA:
                        print("you found a comma in the params!")
                        #if comma yung current, find identifier, next, then if comma, next, and repeat
                        c_error = self.comma()
                        if c_error:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                        
                        print("current token after comma: ", self.current_tok.token)
                    if self.current_tok.token != RPAREN:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                        self.advance()
                    else: 
                        #res.append("SUCCESS from form!")
                        self.advance()
                        if self.current_tok.token == CLBRACKET:
                            print("left curly bracket")
                            
                            self.advance()

                            while self.current_tok.token == NEWLINE:
                                self.advance()
                            form_res, form_error = self.body()
                            print("form res: ", res)
                            if form_error:
                                print("THERES  AN ERROR INSIDE THE FUNCTION SCOPE")
                                for err in form_error:
                                    error.append(err)
                                return [], error
                            else:
                                print("successful form!")
                                for f_res in form_res:
                                    res.extend(f_res)
                                    print("f res: ", f_res)
                                
                            
                            print("CURRENT TOK FROM FORM: ", self.current_tok)
                            if self.current_tok.token != CRBRACKET:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets in form!"))
                                
                            else:
                                res.append("SUCCESS from form!")
                                self.advance()
                                
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Form definition missing!"))
                            self.advance()
                elif self.current_tok.token == RPAREN:
                    self.advance()
                    if self.current_tok.token == CLBRACKET:
                        print("left curly bracket")
                        
                        self.advance()

                        while self.current_tok.token == NEWLINE:
                            self.advance()
                        form_res, form_error = self.body()
                        print("form res: ", form_res)
                        if form_error:
                            print("THERES  AN ERROR INSIDE THE FUNCTION SCOPE")
                            for err in form_error:
                                error.append(err)
                            return [], error
                        else:
                            print("successful form!")
                            for f_res in form_res:
                                res.extend(f_res)
                                print("f res: ", f_res)
                                
                            
                            print("CURRENT TOK FROM FORM: ", self.current_tok)
                            if self.current_tok.token != CRBRACKET:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly brackets!"))
                                
                            else:
                                res.append("SUCCESS from form!")
                                self.advance()
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Form definition missing!"))
                        self.advance()
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parameter id!"))
                    self.advance()
            #form add(a, b)
            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected parentheses for parameters!"))
                return res, error
        else:
            print("FORM TOK: ", self.current_tok)
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected form identifier!"))
            return res, error

        
        return res, error
    
    #* CALLING A FORM
    def call_form(self):
        res = []
        error = []
        
        self.advance()
        print("CURRENT TOKEN AFTER LPAREN IN CALL FORM: ", self.current_tok)
        if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEL or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or self.current_tok.token == GRAVITY:
        
            print("current token from callform is: ", self.current_tok.token)
            self.advance()
            if self.current_tok.token == COMMA:
                print("you found a comma in the function call!")
                #if comma yung current, find identifier, next, then if comma, next, and repeat
                a_error = self.arguments()
                print("current token after comma: ", self.current_tok.token)
                if a_error:
                    print("THERES AN ERROR IN THE FUNCTION ARGS")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected literal after comma!"))
                
                else:
                    print("NO ERROR IN THE FUNCTION ARGS")
                    if self.current_tok.token != RPAREN:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                        self.advance()
                    else: 
                        #res.append("SUCCESS from form!")

                        # self.advance()

                        # print("current token from no error function call: ", self.current_tok.token)
                        # if self.current_tok.token != SEMICOLON:
                        #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon from call form!"))
                        
                        # else:
                            
                        res.append(["SUCCESS from function call!"])
                            
            elif self.current_tok.token == RPAREN:
                print("found no arguments in function call")
                # self.advance()
                # if self.current_tok.token != SEMICOLON:
                #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon! from call form"))
            
                # else: 
                res.append(["SUCCESS from function call!"])
                    

            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid function call!"))




        elif self.current_tok.token == RPAREN:
            print("found no arguments in function call")
            #self.advance()
            # if self.current_tok.token != SEMICOLON:
            #     error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon! from call form"))
        
            # else: 
            res.append(["SUCCESS from function call!"])
                

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid function call!"))

        print("RES FROM CALL FROM FUNCTION: ", res)
        return res, error
    
    def arguments (self):
        error = False
        while self.current_tok.token  == COMMA:
            self.advance()
            if self.current_tok.token == IDENTIFIER or self.current_tok.token == INTEL or self.current_tok.token == STRING or self.current_tok.token == TRUE or self.current_tok.token == FALSE or GRAVITY:
                self.advance()
            else:
                #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                error = True
        return error

    def comma(self):
        error = False
        while self.current_tok.token  == COMMA:
            self.advance()
            if self.current_tok.token == IDENTIFIER:
                self.advance()
            else:
                #error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after comma!"))
                error = True
        return error
    
    #*LOOPING STATEMENTS
    def force_stmt(self):
        res = []
        error = []
        self.advance()
        if self.current_tok.token != LPAREN:
            print("no lparen")
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax!"))
        else: 
            self.advance()
            if self.current_tok.token != VAR:
                print("no var")
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Missing var!"))
            else:
                self.advance()
                if self.current_tok.token != IDENTIFIER:
                    print("no ident")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier!"))
                    
                else: 
                    self.advance()
                    if self.current_tok.token != EQUAL:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid initialization!"))
                    else:
                        self.advance()    
                        if self.current_tok.token != INTEL:
                            print("not an intel")
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Value of Identifier is not valid"))
                        else: 
                            self.advance()
                            if self.current_tok.token != SEMICOLON:
                                print("no semicolon")
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon!"))
                            else:
                                self.advance()
                                if self.current_tok.token != IDENTIFIER:
                                    print("no ident")
                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier!"))
                                else: 
                                    self.advance()
                                    if self.current_tok.token not in (E_EQUAL, NOT_EQUAL, LESS_THAN, LESS_THAN_EQUAL, GREATER_THAN_EQUAL):
                                        print("no condition")
                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Condition!"))
                                    else:
                                        self.advance()
                                        if self.current_tok.token != INTEL:
                                            print("not an intel")
                                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Value of Identifier is not valid"))
                                        else: 
                                            self.advance()
                                            if self.current_tok.token != SEMICOLON:
                                                print("no semicolon")
                                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon!"))
                                            else:
                                                self.advance()
                                                if self.current_tok.token not in (INCRE, DECRE) and self.current_tok.token == IDENTIFIER:
                                                    self.advance()
                                                    if self.current_tok.token not in (INCRE, DECRE):
                                                        print("no unary op")
                                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid operation!"))
                                                    else:
                                                        self.advance()
                                                        if self.current_tok.token != RPAREN:
                                                            print("no rparen")
                                                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                                                        else:
                                                            #res.append("SUCCESS!")

                                                            self.advance()

                                                            if self.current_tok.token != CLBRACKET:
                                                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Force scope!"))
                                                                return [], error
                                                            else:
                                                                self.advance()
                                                                force_res, force_error = self.body()
                                                                print("force res: ", res)
                                                                if force_error:
                                                                    print("THERES  AN ERROR INSIDE THE FORCE SCOPE")
                                                                    for err in force_error:
                                                                        error.append(err)
                                                                    return [], error
                                                                else:
                                                                    print("successful form!")
                                                                    for f_res in force_res:
                                                                        res.append(f_res)
                                                                        print("f res: ", f_res)
                                                                    res.append(["SUCCESS from force"])
                                                                    

                                                                    if self.current_tok.token != CRBRACKET:
                                                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                                                                        return [], error
                                                                    
                                                                    
                                                    
                                                elif self.current_tok.token in (INCRE, DECRE) and self.current_tok.token != IDENTIFIER:
                                                    self.advance()
                                                    if self.current_tok.token != IDENTIFIER:
                                                        print("no ident")
                                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier!"))
                                                    else:
                                                        self.advance()
                                                        if self.current_tok.token != RPAREN:
                                                            print("no rparen")
                                                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))
                                                        else:
                                                            #res.append("SUCCESS!")

                                                            self.advance()

                                                            if self.current_tok.token != CLBRACKET:
                                                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Force scope!"))
                                                                return [], error
                                                            else:
                                                                self.advance()
                                                                force_res, force_error = self.body()
                                                                print("force res: ", res)
                                                                if force_error:
                                                                    print("THERES  AN ERROR INSIDE THE FORCE SCOPE")
                                                                    for err in force_error:
                                                                        error.append(err)
                                                                    return [], error
                                                                else:
                                                                    print("successful form!")
                                                                    for f_res in force_res:
                                                                        res.append(f_res)
                                                                        print("f res: ", f_res)
                                                                    res.append(["SUCCESS from force"])
                                                                    

                                                                    if self.current_tok.token != CRBRACKET:
                                                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                                                                        return [], error
                                                else:
                                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Syntax Error!"))
                                                    #next is yung new line, curly brackerts and stamements
        return res, error
    
    def do_whirl(self):
        res = []
        error = []

        if self.current_tok.token == CLBRACKET:
            self.advance()
            do_res, do_error = self.body()
            print("do res: ", res)
            if do_error:
                print("THERES  AN ERROR INSIDE THE DO SCOPE")
                for err in do_error:
                    error.append(err)
                return [], error
            else:
                print("successful do!")
                for d_res in do_res:
                    res.extend([d_res])
                print("do res: ", do_res)
                
                print("token  after  success do: ", self.current_tok)

                if self.current_tok.token == CRBRACKET:
                    #return [], error
                    self.advance()
                    if self.current_tok.token == WHIRL:
                        self.advance()
                        #TODO connect whirl here
                        w_res, w_error = self.whirl()
                        print("token after whirl:", self.current_tok)
                        if w_error:
                            for err in w_error:
                                error.append(err)
                            return [], error
                        else:
                            self.advance()
                            print("token after whirl in do whirl: ", self.current_tok)
                            if self.current_tok.token == SEMICOLON:
                                res.append(["SUCCESS from do whirl"])
                            else:
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected semicolon in do whirl!"))
                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected whirl condition!"))

                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                
        return res, error

    def whirl(self):
        res = []
        error = []
        print("first token in whirl: ", self.current_tok)
        
        if self.current_tok.token == LPAREN:
            self.advance()
            if self.current_tok.token == IDENTIFIER:
                self.advance()
                if self.current_tok.token == E_EQUAL or self.current_tok.token == LESS_THAN or self.current_tok.token == GREATER_THAN or self.current_tok.token == GREATER_THAN_EQUAL or self.current_tok.token == LESS_THAN_EQUAL or self.current_tok.token == NOT_EQUAL:
                    self.advance()
                    if self.current_tok.token == INTEL or self.current_tok.token == GRAVITY or self.current_tok.token == IDENTIFIER:
                        self.advance()
                        if self.current_tok.token == RPAREN:
                            res.append('SUCCESS from whirl!')
                        else:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing parenthesis!"))

                    else:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Condition!"))
                        
                else:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected relational operator!"))

            else:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier for whirl!"))

        else:
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected condition for whirl!"))

        return res, error
    
    #* INPUT OUTPUT STATEMENTS
    def inner_stmt(self):
        res = []
        error = []
        self.advance()

        # Check if the next token is the inner delimiter ">>"
        if self.current_tok.token != ">>":
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax, expected '>>'"))
        else:
            self.advance()
            # Check if the next token is an identifier
            if self.current_tok.token != IDENTIFIER:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier"))
                self.advance()
                return [], error
            else:
                self.advance()
        # Check if the next token is a semicolon
                if self.current_tok.token != SEMICOLON:
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Semicolon"))

                else:
                    res.append(["SUCCESS from inner!"])

        return res, error
    
    def outer_stmt(self):
        res = []
        error = []
        self.advance()
        if self.current_tok.token != OUT:
            print("no <<")
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '<<' symbol!"))
        else: 
            self.advance()
            if self.current_tok.token != STRING and self.current_tok.token != IDENTIFIER and self.current_tok.token != INTEL and self.current_tok.token != GRAVITY:
                print("no string")
                print("current tok from outer: ", self.current_tok.token)
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected literal or identifier!"))
                self.advance()
            else: 
                self.advance()
                if self.current_tok.token != SEMICOLON:
                    print("no semicolon")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Missing Semicolon!"))
                else:
                    res.append(["SUCCESS from outer"])
        
        return res, error
    
    #*CONDITIONAL
    #FUNC FOR IF, ELSE, ELSEIF
    def if_stmt(self):
        res = []
        error = []
        self.advance()
        if self.current_tok.token != LPAREN:
            print("no lparen")
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax!"))
        else: 
            self.advance()
            if self.current_tok.token != IDENTIFIER:
                print("no ident after left paren")
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier!"))
            else: 
                self.advance()
                if self.current_tok.token not in (E_EQUAL, NOT_EQUAL, LESS_THAN, LESS_THAN_EQUAL, GREATER_THAN_EQUAL, GREATER_THAN):
                    print("no condition")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Condition!"))
                else:
                    self.advance()
                    #-- USED ASSIGN VAL PERO DAPAT BAWAL STRING
                    assign = self.assign_val()
                    assign == True   
                    if self.current_tok.token != RPAREN:
                        print("no rparen")
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax!"))
                    else:
                        self.advance()
                        if self.current_tok.token != CLBRACKET:
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected If Scope!"))
                        else:
                            self.advance()
                            if_res, if_error = self.body()
                            print("if res: ", res)
                            if if_error:
                                print("THERES  AN ERROR INSIDE THE IF SCOPE")
                                for err in if_error:
                                    error.append(err)
                                return [], error
                            else:
                                print("successful form!")
                                for f_res in if_res:
                                    res.append(f_res)
                                    print("f res: ", f_res)
                                res.append(["SUCCESS from if"])
                                self.if_stmt_encountered = True

                                if self.current_tok.token != CRBRACKET:
                                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                                    return [], error
        return res, error
    
    def elif_stmt(self):
        res = []
        error = []
        if self.if_stmt_encountered is not True:
            print("this is the error")
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "elif without preceding if statement!"))
            return res, error
        else: 
            self.advance()
            if self.current_tok.token != LPAREN:
                print("no lparen")
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax!"))
            else: 
                self.advance()
                if self.current_tok.token != IDENTIFIER:
                    print("no ident after left paren")
                    error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier!"))
                else: 
                    self.advance()
                    if self.current_tok.token not in (E_EQUAL, NOT_EQUAL, LESS_THAN, LESS_THAN_EQUAL, GREATER_THAN_EQUAL, GREATER_THAN):
                        print("no condition")
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Condition!"))
                    else:
                        self.advance()
                        #-- used assign val pero bawal dapat string
                        assign = self.assign_val()
                        assign == True   
                        if self.current_tok.token != RPAREN:
                            print("no rparen")
                            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Invalid Syntax!"))
                        else:
                            self.advance()
                            if self.current_tok.token != CLBRACKET:
                                
                                # print("no semicolon")
                                # print("current tok in if: ", self.current_tok.token)
                                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected elif Scope!"))
                            else:
                                self.advance()
                                elif_res, elif_error = self.body()
                                print("if res: ", res)
                                if elif_error:
                                    print("THERES  AN ERROR INSIDE THE IF SCOPE")
                                    for err in elif_error:
                                        error.append(err)
                                    return [], error
                                else:
                                    print("successful elif!")
                                    for f_res in elif_res:
                                        res.append(f_res)
                                        print("f res: ", f_res)
                                    res.append(["SUCCESS from elif"])
                                    self.if_stmt_encountered = True
                                    

                                    if self.current_tok.token != CRBRACKET:
                                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                                        return [], error
                                
                    #next is yung new line, curly brackerts and stamements
        return res, error
    
    def else_stmt(self):
        res = []
        error = []
        if self.if_stmt_encountered is not True:
            print("this is the error")
            error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "else without preceding if or elseif statement!"))
            return res, error
        else: 
            self.advance()
            if self.current_tok.token != CLBRACKET:
                error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected else Scope!"))
            else:
                self.advance()
                else_res, else_error = self.body()
                print("if res: ", res)
                if else_error:
                    print("THERES  AN ERROR INSIDE THE IF SCOPE")
                    for err in else_error:
                        error.append(err)
                    return [], error
                else:
                    print("successful else!")
                    for f_res in else_res:
                        res.append(f_res)
                        print("f res: ", f_res)
                    res.append(["SUCCESS from else"])
                    

                    if self.current_tok.token != CRBRACKET:
                        error.append(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected closing curly bracket!"))
                        return [], error
                                
                    #next is yung new line, curly brackerts and stamements
        return res, error


#?PARSE RESULT ARE HERE
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        
        # if tok.token in STRING:
        #     return res.success(tok.value)
        
        # if tok.token in IDENTIFIER:
        #     return res.success(tok.token)
        
        if tok.token in (PLUS, MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        if tok.token in (INTEL, GRAVITY):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        elif tok.token == LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.token == RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))
        #return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float"))
    
    def term(self):
        return self.bin_op(self.factor, (MUL, DIV))
    
        #really this means:
        '''
        def bin_op(self, func, ops):
            left = factor()

            while self.current_tok in ops: # ops instead of (MUL, DIV)
                op_tok = self.current_tok
                right = factor()
                left = BinOpNode(left, op_tok, right)

            return left
            
        '''

    def expr(self):
        return self.bin_op(self.term, (PLUS, MINUS))
    
        #really this means:
        '''
        def bin_op(self, func, ops):
            left = term()

            while self.current_tok in ops: #ops instead of (PLUS, MINUS)
                op_tok = self.current_tok
                right = term()
                left = BinOpNode(left, op_tok, right)

            return left
            
        '''
   
    #func is rule (expr or term)
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func()) #instead of self.factor() or self.term()
        if res.error:
            return res

        while self.current_tok.token in ops: #instead of (MUL, DIV)
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func()) #instead of self.factor() or self.term()
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
    
       
  

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    for item in tokens:
        if isinstance(item, list):
            tokens.remove(item)
    #return tokens, error
    # if error:
    #     print("Lexical Error!")
        
    parser = Parser(tokens)
    result, parseError = parser.parse()
    
    print("parseError: ", parseError)
    return result, parseError