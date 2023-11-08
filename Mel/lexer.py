
all_num = '0123456789'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
underscore = "_"
space_delim = " "
arithmetic_operator = "+-*/%"
lineEnd_delim = " ;"
symbols = ""

#errors
error = []

#TOKENS

#reserved words
TAKEOFF = 'takeoff' #Start
LANDING = 'landing' #End
#data types
INTEL = 'intel'
GRAVITY = 'gravity'
STAR = 'star'
BANG = 'bang'
VOID = 'void'
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
BREAK = 'break'
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
LQ_MARK = '“'
RQ_MARK = '”'
S_COMET = '/*'
M_OPEN_COMET = '//*'
M_END_COMET =  '*//'
SEMICOLON = ';'
COLON = ':'


#literals

IDENTIFIER = 'IDENTI'
COMMA = 'COMMA'
SPACE = 'SPACE'



class Token:
    def __init__(self, token, value=None):
        self.token = token
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.value}: {self.token}'
        return f'{self.type}'


#LEXER

class Lexer:
    def __init__(self, text):
        
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        # current char is the current pos if the pos is less than the length of the text
        self.current_char = self.text[self.pos] if self.pos <= len(self.text)-1 else None

    def make_tokens(self):
        tokens = []
        errors = []
        string = ""

        while self.current_char is not None:
            if self.current_char in '\t':
                tokens.append(Token(N_TAB, "\\t"))
                self.advance()
            elif self.current_char in ' ':
                tokens.append(Token(SPACE, "\" \""))
                self.advance()
            elif self.current_char in all_letters:
                result = self.make_word()
                if isinstance(result, list):  # check if make_word returned errors
                    errors.extend(result)
                    #break  # exit the loop if there are errors
                else:
                    tokens.append(result)
            elif self.current_char in all_num:
                result = self.make_number()
                if isinstance(result, list):  # check if make_number returned errors
                    errors.extend(result)
                    #break  # exit the loop if there are errors
                else:
                    tokens.append(result)
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=)
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(E_EQUAL, "==")) #for == symbol
                    self.advance()
                else:
                    tokens.append(Token(EQUAL, "="))
                    self.advance()
            elif self.current_char == '<': #relational operator
                self.advance()        
                if self.current_char == '=':
                    tokens.append(Token(LESS_THAN_EQUAL, "<=")) #for == symbol
                    self.advance()
                else:
                    tokens.append(Token(LESS_THAN, "<"))
                    self.advance()    
            elif self.current_char == '>': 
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(GREATER_THAN_EQUAL, ">=")) #for == symbol
                    self.advance()
                else:
                    tokens.append(Token(GREATER_THAN, ">"))
                    self.advance()    
            elif self.current_char == '+': #mathematical operator (+, -, *, /, %)
                self.advance()
                if self.current_char == '=': #for += symbol
                    tokens.append(Token(PLUS_EQUAL, "+="))
                    self.advance()
                elif self.current_char == '+': #for ++ incre
                    tokens.append(Token(INCRE, "++"))
                    self.advance()
                else:
                    tokens.append(Token(PLUS, "+"))
                    self.advance()
            elif self.current_char == '-': 
                self.advance()
                if self.current_char == '=': #for -=symbol
                    tokens.append(Token(MINUS_EQUAL, "-="))
                    self.advance()
                elif self.current_char == '-': #for -- decre
                    tokens.append(Token(DECRE, "--"))
                    self.advance()
                else:
                    tokens.append(Token(MINUS, "-"))
                    self.advance()
            elif self.current_char == '*': 
                self.advance()
                if self.current_char == '=': #for *= symbol
                    tokens.append(Token(MUL_EQUAL, "*=")) #for *// ending comet
                    self.advance()
                else:
                    tokens.append(Token(MUL, "*"))
                    self.advance()
            elif self.current_char == '/': 
                self.advance()
                if self.current_char == '=': #for /= symbol
                    tokens.append(Token(DIV_EQUAL, "/="))
                    self.advance()
                elif self.current_char == '/': #for 
                    self.advance()
                    if self.current_char == "*":
                        tokens.append(Token(M_OPEN_COMET, "//*"))
                        self.advance()# for multi comment
                elif self.current_char == "*":
                    tokens.append(Token(S_COMET, "/*"))# for single comet
                    self.advance()
                else:
                    tokens.append(Token(DIV, "/"))
                    self.advance()
            elif self.current_char == '%':
                tokens.append(Token(MODULUS, "%"))
                self.advance()
            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(NOT_EQUAL, "!=")) #for != symbol
                    self.advance()
                else:
                    tokens.append(Token(NOT_OP, "!"))
                    self.advance()
            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token(AND_OP, "&&"))
                    self.advance()
                else:
                    tokens.append(Token(AND_OP, "&"))
            elif self.current_char == '|': #return error
                self.advance()   
                if self.current_char == '|':
                    tokens.append(Token(OR_OP, "||"))
                    self.advance()
                else:
                    tokens.append(Token(OR_OP, "|"))
            elif self.current_char == '(': #other operator
                tokens.append(Token(LPAREN, "("))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN, ")"))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(SLBRACKET, "["))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(SRBRACKET, "]"))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(CLBRACKET, "{"))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(CLBRACKET, "}"))
                self.advance()
            elif self.current_char == '#': #return error
                self.advance()
                if self.current_char == '#':
                    tokens.append(Token(SHARP, "##"))
                    self.advance()
                else:
                    tokens.append(Token(SHARP, "#"))
            
            elif self.current_char == "\"":
                tokens.append(Token(QMARK, "\'"))
            
            elif self.current_char == ',':
                tokens.append(Token(COMMA, ","))
                self.advance()
            elif self.current_char == ";":
                tokens.append(Token(SEMICOLON, ";"))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(COLON, ":"))
                self.advance()

        if errors:
            return [], errors
        else:
            return tokens, None       

    def make_number(self):
        dec_count = 0
        num_count = 0
        num_str = ''
        dot_count = 0
        errors = []

        while self.current_char is not None and self.current_char in all_num + '.':
            if num_count > 9:
                errors.append(f"You've reached the intel limit!")
                break
            if self.current_char == '.':
                if dot_count == 1: 
                    errors.append(f"Invalid character '{self.current_char}' in number.")
                    break
                dot_count += 1
                num_str += '.'
                
            else:
                if '.' in num_str:
                    dec_count += 1
                    num_count -= 1
                if dec_count > 4:
                    errors.append(f"You've reached the gravity limit!")
                    break
                num_count += 1
                num_str += self.current_char
            self.advance()
        
        # check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            errors.append("Identifiers cannot start with a number!")

        if errors:
            return errors
        elif dot_count == 0:
            return Token(INTEL, int(num_str))
        else:
            return Token(GRAVITY, float(num_str))
        
    #takes in the input character by character then translates them into words then tokens
    def make_word(self):
        ident = ""
        errors = []
        
        while self.current_char != None and self.current_char in alphanum:
            if self.current_char == "b":
                ident += self.current_char
                self.advance()
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "g":
                            ident += self.current_char
                            self.advance()
                            # catch if bang lang yung tinype ng user
                            if self.current_char == None:
                                return Token(BANG, ident)
                            #delimiter ng bang defined in space_delim
                            if self.current_char not in space_delim:
                                while self.current_char in alphanum and self.current_char not in space_delim:
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == None:
                                        return Token(IDENTIFIER, ident)
                                ###test
                            else:
                                return Token(BANG, ident)
                           
                elif self.current_char == "l":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "s":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "t":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == None:
                                    return Token(BLAST, ident)
                            #arith ops
                            if self.current_char not in lineEnd_delim:
                                while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == None:
                                        return Token(IDENTIFIER, ident)
                                
                            else:
                                return Token(BLAST, ident)
            if self.current_char == "d": #do
                ident += self.current_char
                self.advance()
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    return Token(DO, "do")
                
            if self.current_char == "e": #else, else if, entity
                ident += self.current_char
                self.advance()
                if self.current_char == "l":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "s":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == " ":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "i":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "f":
                                        ident += self.current_char
                                        self.advance()
                                        return Token(ELSEIF, "elseif")
                            else:
                                return Token(ELSE, "else")
                elif self.current_char == "n":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "t":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "y":
                                    ident += self.current_char
                                    self.advance()
                                    return Token(ENTITY, "entity")
            if self.current_char == "i": #if, inner, intel
                ident += self.current_char
                self.advance()
                if self.current_char == "f":
                    ident += self.current_char
                    self.advance()
                    return Token(IF, "if")
                elif self.current_char == "n":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                return Token(INNER, "inner")
                    elif self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "l":
                                ident += self.current_char
                                self.advance()
                                return Token(INTEL, "intel")            
            if self.current_char == "f": #false, force, form
                ident += self.current_char
                self.advance()
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "l":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "s":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                    return Token(FALSE, "false")
                elif self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "c":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                return Token(FORCE, "force")
                        elif self.current_char == "m":
                            ident += self.current_char
                            self.advance()
                            return Token(FORM, "form")
            if self.current_char == "g": #gravity
                ident += self.current_char
                self.advance()
                if self.current_char == "r":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "v":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "i":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "t":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "y":
                                        ident += self.current_char
                                        self.advance()
                    return Token(GRAVITY, "gravity")  
            if self.current_char == "l": #landing, launch
                ident += self.current_char
                self.advance()
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "n":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "i":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "n":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "g":
                                        ident += self.current_char
                                        self.advance()
                                        return Token(LANDING, "landing")  
                    elif self.current_char == "u":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "n":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "c":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "h":
                                    ident += self.current_char
                                    self.advance()
                                    return Token(LAUNCH, "launch")
            if self.current_char == "o": #outer
                ident += self.current_char
                self.advance()
                if self.current_char == "u":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                return Token(OUTER, "outer")
            if self.current_char == "s": #saturn, shift, star
                ident += self.current_char
                self.advance()
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "u":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "n":
                                    ident += self.current_char
                                    self.advance()
                                    return Token(SATURN, "saturn")
                elif self.current_char == "h":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "i":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "f":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "t":
                                    ident += self.current_char
                                    self.advance()
                                    return Token(SHIFT, "shift")
                elif self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "a":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                return Token(STAR, "star")
            if self.current_char == "t": #takeoff, trace, true
                ident += self.current_char
                self.advance()
                if self.current_char == "a":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "k":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "o":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "f":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "f":
                                        ident += self.current_char
                                        self.advance()
                                        return Token(TAKEOFF, "takeoff")
                elif self.current_char == "r":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "a":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "c":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "e":
                                    ident += self.current_char
                                    self.advance()
                                    return Token(TRACE, "trace") 
                        elif self.current_char == "u":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()         
                                return Token(TRUE, "true")  
            if self.current_char == "u": #universe
                ident += self.current_char
                self.advance()
                if self.current_char == "n":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "v":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()
                                if self.current_char == "r":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "s":
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == "e":
                                            ident += self.current_char
                                            self.advance()
                                            return Token(UNIVERSE, "universe")    
            if self.current_char == "v": #void
                ident += self.current_char
                self.advance()
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "d":
                            ident += self.current_char
                            self.advance()
                            return Token(VOID, "void")   
            if self.current_char == "w": #whirl
                ident += self.current_char
                self.advance()
                if self.current_char == "h":
                    ident += self.current_char
                    self.advance()
                    if self.current_char == "i":
                        ident += self.current_char
                        self.advance()
                        if self.current_char == "r":
                            ident += self.current_char
                            self.advance()
                            if self.current_char == "l":
                                ident += self.current_char
                                self.advance()
                                return Token(WHIRL, "whirl")
            else:
                if self.current_char == None:
                    break
                if self.current_char.isdigit() == True:
                    ident += str(self.current_char)
                    self.advance()
                else:
                    ident += self.current_char
                    self.advance()
        
        for item in ident:
            if item not in alphanum:
                errors.append("Identifiers cannot contain special symbols!")
                break

        if errors:
            return errors

        return Token(IDENTIFIER, ident)
            
            

    def make_symbol(self):
        symbol = ""

        while self.current_char != None and self.current_char in alphanum:
            pass
        
       
  

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error
