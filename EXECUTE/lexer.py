
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
GALAXY = 'galaxy'
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
#negative operator
NEG_OP = '~'
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
#TILDE = "~"

#literals

IDENTIFIER = 'IDENTI'
COMMA = ','
SPACE = "space"
EOF = 'EOF'
COMMENT = "COMMENT"

class Error:
    def __init__ (self,pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self. details = details

    def __repr__(self): 
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    #the lexer comes across a character it doesn't support
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character ', details)

class DelimiterError(Error):
    def __init__(self,pos_start, pos_end, details, char):
        super().__init__(pos_start, pos_end, f"Invalid Delimiter for '{char}'", "Cause -> " + str(details))

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance (self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Token:
    def __init__(self, token, value=None):
        self.token = token
        self.value = value
    
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
            if self.current_char in '\t':
                tokens.append(Token(N_TAB, "\\t"))
                self.advance()
            elif self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n"))
                self.advance()
            elif self.current_char in ' ':
                tokens.append(Token(SPACE, "\" \""))
                self.advance()
            elif self.current_char in all_letters:
                result, error = self.make_word()
                
                errors.extend(error)
                tokens.append(result)
                    
            elif self.current_char in all_num:
                result, error = self.make_number()
                
                errors.extend(error)
                
                
                if self.current_char == None or self.current_char == EOF:
                    errors.extend([f"Invalid delimiter for {result.value}. Cause: ' {self.current_char} '. "])
                else:
                    tokens.append(result)
                    
                    
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=, ==)
                self.advance()
                if self.current_char == '=':
                    
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected:  \' \', ;, ' \"\', (, [, or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
                        continue
                    if self.current_char not in (delim1 + '['):
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '. Expected:  \' \', ;, ' \"\', (, [, or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
                        continue
                    tokens.append(Token(E_EQUAL, "==")) #for == symbol
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', or ( "])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' = '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', or ( "])
                        continue
                    tokens.append(Token(EQUAL, "=")) #for == symbol
                        
            elif self.current_char == '~':
                self.advance()
                if self.current_char in all_num:
                    result, error = self.make_number()
                    result = Token(result.token, "~" + str(result.value))
                    tokens.append(result)  
                else:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '. Expected:  123456789"])
                    
                    
            elif self.current_char == '<': #relational operator
                self.advance()        
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' <= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    tokens.append(Token(LESS_THAN_EQUAL, "<=")) #for == symbol
                elif self.current_char == '<':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' << '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', or ( "])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' << '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', or ( "])
                        continue
                    tokens.append(Token(OUT, "<<"))
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    if self.current_char not in (delim2 + space_delim + alphanum):
                        errors.extend([f"Invalid delimiter for ' < '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    tokens.append(Token(LESS_THAN, "<"))
                    
                  
            elif self.current_char == '>': 
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' >= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, or ( "])
                        continue
                    tokens.append(Token(GREATER_THAN_EQUAL, ">="))
                elif self.current_char == '>':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' >> '. Cause: ' {self.current_char} '. Expected: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ or  \' \' "])
                        continue
                    if self.current_char not in all_letters+space_delim:
                        errors.extend([f"Invalid delimiter for ' >> '. Cause: ' {self.current_char} '. Expected: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ or  \' \' "])
                        continue
                    tokens.append(Token(IN, ">>"))
                    
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '. Expected: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ( or  \' \' "])
                        continue
                    if self.current_char not in alphanum + '(' + space_delim:
                        errors.extend([f"Invalid delimiter for ' > '. Cause: ' {self.current_char} '. Expected: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ( or  \' \' "])
                        continue
                    tokens.append(Token(GREATER_THAN, ">"))
                    
                
            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', (, or ["])
                        continue
                    if self.current_char not in (delim1 + '['):
                        errors.extend([f"Invalid delimiter for ' += '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\', (, or ["])
                        continue
                    tokens.append(Token(PLUS_EQUAL, "+=")) #for == symbol
                    
                elif self.current_char == '+': #for ++ incre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for '++'. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ) "])
                        continue
                    if self.current_char not in (lineEnd_delim + alphanum + ')'):
                        errors.extend([f"Invalid delimiter for '++'. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ) "])
                        continue
                    tokens.append(Token(INCRE, "++")) #for == symbol
                else:
    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' + ' ! Cause: {self.current_char}. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                        
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' + ' ! Cause: {self.current_char}. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                        
                    tokens.append(Token(PLUS, "+")) #for == symbol
                    
                        
                    
            elif self.current_char == '-': 
                self.advance()
                if self.current_char == '=': #for -=symbol
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ( "])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' -= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ( "])
                        continue
                    tokens.append(Token(MINUS_EQUAL, "-=")) 
                elif self.current_char == '-': #for -- decre
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ) "])
                        continue
                    if self.current_char not in (lineEnd_delim + alphanum + ')'):
                        errors.extend([f"Invalid delimiter for ' -- '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ) "])
                        continue
                    tokens.append(Token(DECRE, "--")) 
                
                else:
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' - '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ( "])
                        continue
                    tokens.append(Token(MINUS, "-")) 
                
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
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' *= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ( "])
                        continue
                    tokens.append(Token(MUL_EQUAL, "*=")) 
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' * '. Cause: ' {self.current_char} ' Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ( "])
                        continue
                    tokens.append(Token(MUL, "*"))    
                        
                
                
            elif self.current_char == '/': 
                self.advance()
                if self.current_char == '=': #for /= symbol
                    
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' /= '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    tokens.append(Token(DIV_EQUAL, "/="))
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
                        
                        #tokens.append(Token(COMMENT, f"{comment}"))# for single comet
                elif self.current_char == "*":
                    tokens.append(Token(S_COMET, "/*"))# for single comet
                    #self.advance()
                    comment = ""
                    while self.current_char != "\n":
                        self.advance()
                        comment += self.current_char
                        print("CURRENT CHAR IN TOKEN: ", self.current_char)
                    tokens.append(Token(COMMENT, f"{comment}"))# for single comet

                    
                
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        errors.extend([f"Invalid delimiter for ' / '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
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
                    #errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '%')])
                    errors.extend([f"Invalid delimiter for ' % '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])

                    
                    continue
                tokens.append(Token(MODULUS, "%"))
                
            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                pos_start = self.pos.copy()
                if self.current_char == '=':  
                    self.advance()
                    pos_start = self.pos.copy()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected:  \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])
                        continue
                    if self.current_char not in delim2:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!=' )])
                        errors.extend([f"Invalid delimiter for ' != '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or ("])

                        continue
                    tokens.append(Token(NOT_EQUAL, "!=")) #for != symbol
                else:
                    if self.current_char == None:
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                    if self.current_char not in delim1 + '(':
                        # errors.extend([DelimiterError(pos_start, self.pos, self.current_char, '!')])
                        errors.extend([f"Invalid delimiter for ' ! '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                    tokens.append(Token(NOT_OP, "!"))
                    
            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' & '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' & '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
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
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                    if self.current_char not in delim1:
                        errors.extend([f"Invalid delimiter for ' || '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or ("])
                        continue
                    tokens.append(Token(OR_OP, "||"))
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
                    
            elif self.current_char == '(': #other operator
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or )"])
                    continue
                if self.current_char not in delim1 + ')' + alphanum + '!':
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ' \"\' or )"])
                    continue
                tokens.append(Token(LPAREN, "("))
            elif self.current_char == ')':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: +-*/%, ><==!<=>=!=, \' \', 'closing bracket', ;, \' \', newline or ) "])
                    continue
                if self.current_char not in closing_delim + '{' + ';' + space_delim + '\n' + ')' + ',':
                    errors.extend([f"Invalid delimiter for ' ( '. Cause: ' {self.current_char} '. Expected: +-*/%, ><==!<=>=!=, \' \', 'closing bracket', ;, \' \', newline or ) "])
                    continue
                tokens.append(Token(RPAREN, ")"))
            elif self.current_char == '[':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ] "])
                    continue
                if self.current_char not in delim0 + space_delim + ']' + " \" ":
                    errors.extend([f"Invalid delimiter for ' [ '. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, ] "])
                    continue
                tokens.append(Token(SLBRACKET, "["))
            elif self.current_char == ']':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: ; "])
                    continue
                if self.current_char not in lineEnd_delim + ',':
                    errors.extend([f"Invalid delimiter for ' ] '. Cause: ' {self.current_char} '. Expected: ; "])
                    continue
                tokens.append(Token(SRBRACKET, "]"))
            elif self.current_char == '{':
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or newline "])
                    continue
                if self.current_char not in delim3:
                    errors.extend([f"Invalid delimiter for 'opening curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or newline "])
                    continue
                tokens.append(Token(CLBRACKET, "{"))
            elif self.current_char == '}':
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(CRBRACKET, "}"))
                    continue
                if self.current_char not in delim3:
                    errors.extend([f"Invalid delimiter for 'closing curly bracket'. Cause: ' {self.current_char} '. Expected: \' \', abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or newline "])
                    continue
                tokens.append(Token(CRBRACKET, "}"))
            
            elif self.current_char == "\"":
                string, error = self.make_string()
                tokens.append(Token(STRING, f"{string}"))
                self.advance()
                # if self.current_char == None:
                #     errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '"])
                #     continue
                # if self.current_char not in lineEnd_delim+'),' + delim0:
                #     errors.extend([f"Invalid delimiter for ' \" '. Cause: ' {self.current_char} '"])
                #     continue
                # tokens.append(Token(Q_MARK, "\""))
                
                errors.extend(error)
                # ! BAWAL DAPAT YUGN SINGLE QUOTATION
            # elif self.current_char == '\'':
            #     self.advance()
            #     if self.current_char == None:
            #         errors.extend([f"Invalid delimiter for ' \' '. Cause: ' {self.current_char} '. Expected: ; or ),"])
            #         continue
            #     if self.current_char not in lineEnd_delim+'),':
            #         errors.extend([f"Invalid delimiter for ' \' '. Cause: ' {self.current_char} '. Expected: ; or ),"])
            #         continue
            #     tokens.append(Token(SQ_MARK, "\'"))
            elif self.current_char == ',':
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: \' \' or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Invalid delimiter for ' , '. Cause: ' {self.current_char} '. Expected: \' \' or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
                    continue
                tokens.append(Token(COMMA, ","))
            elif self.current_char == ";":
                
                self.advance()
                if self.current_char == None:
                    tokens.append(Token(SEMICOLON, ";"))
                    continue
                if self.current_char not in newline_delim + space_delim + '}' + alphanum + "-+":
                    errors.extend([f"Invalid delimiter for ' ; '. Cause: ' {self.current_char} '. Expected: newline, \' \', closing bracket, abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 or -+"])
                    continue
                tokens.append(Token(SEMICOLON, ";"))
            elif self.current_char == ":":
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' : '. Cause: ' {self.current_char} '. Expected: newline"])
                    continue
                if self.current_char not in newline_delim:
                    errors.extend([f"Invalid delimiter for ' : '. Cause: ' {self.current_char} '. Expected: newline"])
                    continue
                #TODO FIX DELIMITER
                tokens.append(Token(COLON, ":"))
            elif self.current_char == "~":
                
                self.advance()
                if self.current_char == None:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '. Expected: \' \' or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
                    continue
                if self.current_char not in delim0:
                    errors.extend([f"Invalid delimiter for ' ~ '. Cause: ' {self.current_char} '. Expected: \' \' or abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "])
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
        tokens.append(Token(EOF, "EOF"))
        return tokens, errors       

    def make_number(self):
        dec_count = 0
        num_count = 0
        num_str = ''
        dot_count = 0
        errors = []
        #not used ata to
        reached_limit_intel = False
        

        while self.current_char is not None and self.current_char in all_num + '.':
           
                    
            if self.current_char == '.':
                if dot_count == 1: 
                    errors.append(f"Invalid character '{self.current_char}' in number. Decimal point already found!")
                    break 
                dot_count += 1 
                num_str += '.'
                
            else:
                if '.' in num_str: 
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
            # if dot_count == 0:
            #     #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
            #     return Token(INTEL, int(num_str)), errors
            # else:
            #     return Token(GRAVITY, float(num_str)), errors
        
        if dot_count == 0:
            #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
            return Token(INTEL, int(num_str)), errors
        else:
            return Token(GRAVITY, float(num_str)), errors
       
        
    #takes in the input character by character then translates them into words then tokens
    def make_word(self):
        
        ident = ""  
        ident_count = 0
        errors = []
        
        while self.current_char != None:
            
            if self.current_char == "b":
                
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
                        if self.current_char == "s":
                            
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "t":
                                
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for blast! Cause: {self.current_char}. Expected: newline '])
                                    return [], errors
                                if self.current_char not in lineEnd_delim:
                                    errors.extend([f'Invalid delimiter for blast! Cause: {self.current_char}. Expected: newline '])
                                    return [], errors

                                return Token(BLAST, "blast"), errors
                            else:
                                print("not blast: ", self.current_char)
                                #self.advance()
                                ident_res = self.make_ident(ident)
                                ident += ident_res
                                return Token(IDENTIFIER, ident), errors
                        else:
                            print("not blast: ", self.current_char)
                            #self.advance()
                            ident_res = self.make_ident(ident)
                            ident += ident_res
                            return Token(IDENTIFIER, ident), errors
                    else:
                        print("not blast: ", self.current_char)
                        #self.advance()
                        ident_res = self.make_ident(ident)
                        ident += ident_res
                        return Token(IDENTIFIER, ident), errors
                else:
                    print("not blast: ", self.current_char)
                    #self.advance()
                    ident_res = self.make_ident(ident)
                    ident += ident_res
                    return Token(IDENTIFIER, ident), errors
                            
                                
                
            elif self.current_char == "d": #do
                ident += self.current_char
                self.advance()
                print("ident: ", ident)
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    
                    if self.current_char == None:
                        errors.extend([f'Invalid delimiter for do! Cause: {self.current_char}. Expected: opening bracket or newline'])
                        return [], errors
                    if self.current_char not in block_delim:
                        errors.extend([f'Invalid delimiter for do! Cause: {self.current_char}. Expected: opening bracket or newline'])
                        return [], errors
                    return Token(DO, "do"), errors
                else:
                    print("not do: ", self.current_char)
                    #self.advance()
                    ident_res = self.make_ident(ident)
                    ident += ident_res
                    return Token(IDENTIFIER, ident), errors
                
                
            elif self.current_char == "e": #else, else if, entity
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
                                        errors.extend([f'Invalid delimiter for elseif! Cause: {self.current_char} Expected: opening bracket, newline or ( '])
                                        return [], errors
                                    if self.current_char not in block_delim + "(":
                                        errors.extend([f'Invalid delimiter for elseif! Cause: {self.current_char} Expected: opening bracket, newline or ( '])
                                        return [], errors
                                    return Token(ELSEIF, "elseif"), errors
                            else:
                                if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for else! Cause: {self.current_char}. Expected: opening bracket or newline'])
                                    return [], errors
                                if self.current_char not in block_delim:
                                    errors.extend([f'Invalid delimiter for else! Cause: {self.current_char}. Expected: opening bracket or newline'])
                                    return [], errors
                                return Token(ELSE, "else"),errors
                                    
                
            elif self.current_char == "i": #if, inner, intel
                ident += self.current_char
                self.advance()
                ident_count += 1 
                if self.current_char == "f":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == None:
                        errors.extend([f'Invalid delimiter for if! Cause: {self.current_char}. Expected: ( '])
                        return [], errors
                    if self.current_char not in loop_delim:
                        errors.extend([f'Invalid delimiter for if! Cause: {self.current_char}. Expected: ( '])
                        return [], errors
                    return Token(IF, "if"), errors
                
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
                                    errors.extend([f'Invalid delimiter for inner! Cause: {self.current_char}. Expected: >> '])
                                    return [], errors
                                if self.current_char not in inner_delim:
                                    errors.extend([f'Invalid delimiter for inner! Cause: {self.current_char}. Expected: >> '])
                                    return [], errors
                                return Token(INNER, "inner"), errors
                        
            elif self.current_char == "f": #false, force, form
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
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
                                    return [], errors
                                if self.current_char not in bool_delim + ',':
                                    errors.extend([f'Invalid delimiter for false! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
                                    return [], errors
                                return Token(FALSE, "false"), errors
                            
                            
                    
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
                                    errors.extend([f'Invalid delimiter for force! Cause: {self.current_char}. Expected: ('])
                                    return [], errors
                                if self.current_char not in loop_delim:
                                    errors.extend([f'Invalid delimiter for force! Cause: {self.current_char}. Expected: ('])
                                    return [], errors
                                return Token(FORCE, "force"), errors
                            

                        elif self.current_char == "m":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == None:
                                    errors.extend([f'Invalid delimiter for form! Cause: {self.current_char}. Expected: \' \''])
                                    return [], errors
                            if self.current_char not in space_delim:
                                errors.extend([f'Invalid delimiter for form! Cause: {self.current_char}. Expected: \' \''])
                                return [], errors
                            return Token(FORM, "form"), errors
                        
            elif self.current_char == "g": #galaxy
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
                                        errors.extend([f'Invalid delimiter for galaxy! Cause: {self.current_char}. Expected: \' \' '])
                                        return [], errors
                                    if self.current_char not in "( " + space_delim:
                                        errors.extend([f'Invalid delimiter for galaxy! Cause: {self.current_char}. Expected: \' (\' '])
                                        return [], errors
                                    return Token(GALAXY, "galaxy"), errors                     
                
            elif self.current_char == "l": #landing, launch
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
                                            errors.extend([f'Invalid delimiter for landing! Cause: {self.current_char}. Expected: ; '])
                                            return [], errors
                                        if self.current_char not in lineEnd_delim:
                                            errors.extend([f'Invalid delimiter for landing! Cause: {self.current_char}. Expected: ; '])
                                            return [], errors
                                        return Token(LANDING, "landing"), errors
                                    
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
                                        errors.extend([f'Invalid delimiter for launch! Cause: {self.current_char}. Expected: \' \' '])
                                        return [], errors
                                    if self.current_char not in space_delim:
                                        errors.extend([f'Invalid delimiter for launch! Cause: {self.current_char}. Expected: \' \' '])
                                        return [], errors
                                    return Token(LAUNCH, "launch"), errors
                                    
                
            elif self.current_char == "o": #outer
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
                                    errors.extend([f'Invalid delimiter for outer! Cause: {self.current_char}. Expected: << '])
                                    return [], errors
                                if self.current_char not in outer_delim:
                                    errors.extend([f'Invalid delimiter for outer! Cause: {self.current_char}. Expected: << '])
                                    return [], errors
                                return Token(OUTER, "outer"), errors
                
            elif self.current_char == "s": #saturn, shift, skip, star
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
                                        errors.extend([f'Invalid delimiter for saturn! Cause: {self.current_char}. Expected: ;'])                                        
                                        return [], errors
                                    if self.current_char not in lineEnd_delim:
                                        errors.extend([f'Invalid delimiter for saturn! Cause: {self.current_char}. Expected: ;'])
                                        return [], errors
                                    return Token(SATURN, "saturn"), errors

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
                                    errors.extend([f'Invalid delimiter for skip! Cause: {self.current_char}. Expected: ;'])
                                    return [], errors
                                if self.current_char not in lineEnd_delim:
                                    errors.extend([f'Invalid delimiter for skip! Cause: {self.current_char}. Expected: ;'])
                                    return [], errors
                                return Token(SKIP, "skip"), errors
            
            elif self.current_char == "t": #takeoff, trace, true
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
                                            errors.extend([f'Invalid delimiter for takeoff! Cause: {self.current_char}. Expected: ;'])
                                            return [], errors
                                        if self.current_char not in lineEnd_delim:
                                            errors.extend([f'Invalid delimiter for takeoff! Cause: {self.current_char}. Expected: ;'])
                                            return [], errors
                                        return Token(TAKEOFF, "takeoff"), errors
                                
                elif self.current_char == "r":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "u":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()     
                            ident_count += 1    
                            if self.current_char == None:
                                errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
                                return [], errors
                            if self.current_char not in bool_delim + ',':
                                errors.extend([f'Invalid delimiter for true! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
                                return [], errors
                            return Token(TRUE, "true"), errors
                
            elif self.current_char == "u": #universe
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
                                                errors.extend([f'Invalid delimiter for universe! Cause: {self.current_char}. Expected: \' \' '])
                                                return [], errors
                                            if self.current_char not in space_delim:
                                                errors.extend([f'Invalid delimiter for universe! Cause: {self.current_char}. Expected: \' \' '])
                                                return [], errors
                                            return Token(UNIVERSE, "universe"), errors
                
            elif self.current_char == "v": #void
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
                                errors.extend([f'Invalid delimiter for void! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
                                return [], errors
                            if self.current_char not in bool_delim:
                                errors.extend([f'Invalid delimiter for void! Cause: {self.current_char}. Expected: \' \', ;, newline or ) '])
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
                            errors.extend([f'Invalid delimiter for var! Cause: {self.current_char}. Expected: \' \' '])
                            return [], errors
                        if self.current_char not in space_delim:
                            errors.extend([f'Invalid delimiter for var! Cause: {self.current_char}. Expected: \' \' '])
                            return [], errors
                        return Token(VAR, "var"), errors
                  
                            
            elif self.current_char == "w": #whirl
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
                                    errors.extend([f'Invalid delimiter for whirl! Cause: {self.current_char}. Expected: ('])
                                    return [], errors
                                if self.current_char not in loop_delim:
                                    errors.extend([f'Invalid delimiter for whirl! Cause: {self.current_char}. Expected: ('])
                                    return [], errors
                                return Token(WHIRL, "whirl"), errors
            
            ident_res = self.make_ident(ident)
            ident += ident_res
            for item in ident:
                if item in ident_special_chars:
                    error.extend([f"Identifiers cannot have special characters! Cause: {item}"])
                    return [], error
            return Token(IDENTIFIER, ident), errors
                        
            
            # else:
                
            #     print("non reserve word letter: ", self.current_char)
            #     ident_res = self.make_ident(ident)
            #     ident += ident_res
            #     return Token(IDENTIFIER, ident), errors
        
                        
        
        if self.current_char == None:
            errors.extend([f"Invalid delimiter for {ident}. Cause: ' {self.current_char} '"])
            return [], errors
        
        if errors:
            return [], errors
        else:
            return Token(IDENTIFIER, ident), errors

    def make_ident(self, ident):
        temp = ""
        print("make ident char: ", self.current_char)
        
        while self.current_char not in (lineEnd_delim + ident_delim + CLBRACKET + CRBRACKET + space_delim + '(' + ':' + '\n' + "[]"):
            
            if self.current_char == None:
                break
            if self.current_char in (lineEnd_delim + ident_delim + CLBRACKET + CRBRACKET + space_delim + '(' + ':' + '\n' + "[]"):
                break
            
            
            if self.current_char in "\n":
                break
            
            if self.current_char == UNDERSCORE:
                
                temp += str(self.current_char)
                self.advance()
            if self.current_char.isdigit() == True:
                
                temp += str(self.current_char)
                self.advance()
            else:
                
                temp += self.current_char
                self.advance()

            # for item in ident:
            #     if item in ident_special_chars:
            #         error.extend([f"Identifiers cannot have special characters! Cause: {item}"])
            #         return [], error
         
        return temp
        
    def make_string(self):
        pos_start = self.pos.copy()
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
        
        
       
  

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error
