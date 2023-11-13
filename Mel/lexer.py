
all_num = '0123456789'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
special_chars = "$:?@\^`~"
ident_special_chars = "$:?@\^\"`~#"

space_delim = " "
arithmetic_operator = "+-*/%"
lineEnd_delim = " ;"
symbols = ""
ident_delim = ",+-*/%><!=&|)"
equal_delim = alphanum + "({"

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
STRING = 'string'
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
S_COMET = '/*'
M_OPEN_COMET = '//*'
M_END_COMET =  '*//'
SEMICOLON = ';'
COLON = ':'
UNDERSCORE = "_"
NEWLINE= "\\n"
IN = ">>"
OUT = "<<"

#literals

IDENTIFIER = 'IDENTI'
COMMA = ','
SPACE = "space"



class Token:
    def __init__(self, token, value=None):
        self.token = token
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.value}: {self.token}'
        return f'{self.token}'


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
            if self.current_char in special_chars:
                errors.extend([f"Invalid symbol: {self.current_char}"])
                self.advance()
            elif self.current_char in '\t':
                tokens.append(Token(N_TAB, "\\t"))
                self.advance()
            elif self.current_char  == '\n':
                tokens.append(Token(NEWLINE, "\\n"))
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
                result, error = self.make_number()
                if error:
                    errors.extend(error)
                    #break  # exit the loop if there are errors
                else:
                    tokens.append(result)
                    
            elif self.current_char == '=': #assignment operator (=, +=, -=, *=, /=, ==)
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(E_EQUAL, "==")) #for == symbol
                    
                    if self.current_char == None:
                        tokens.append(Token(E_EQUAL, "=="))
                    elif self.current_char not in (alphanum + equal_delim + space_delim):
                        self.advance()
                        errors.extend([f"Invalid delimiter for ' == '. Cause: ' {self.current_char} '"])
                        
                    
                else:
                    
                    if self.current_char == None:
                        errors.extend([f"Invalid delimiter for ' = '. Cause : ' {self.current_char} '"])
                    elif self.current_char not in (alphanum + equal_delim + space_delim ):
                        tokens.append(Token(EQUAL, "="))
                        errors.extend([f"Invalid delimiter for ' = '. Cause : ' {self.current_char} '"])
                        self.advance()
                    else:
                        tokens.append(Token(EQUAL, "="))
                        
                    
                    
            elif self.current_char == '<': #relational operator
                self.advance()        
                if self.current_char == '=':
                    tokens.append(Token(LESS_THAN_EQUAL, "<=")) #for == symbol
                    self.advance()
                elif self.current_char == '<':
                    tokens.append(Token(OUT, "<<"))
                    self.advance()
                else:
                    tokens.append(Token(LESS_THAN, "<"))
                    
                  
            elif self.current_char == '>': 
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(GREATER_THAN_EQUAL, ">=")) #for == symbol
                    self.advance()
                elif self.current_char == '>':
                    tokens.append(Token(IN, ">>"))
                    self.advance()
                else:
                    tokens.append(Token(GREATER_THAN, ">"))
                    
                
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
                    
            elif self.current_char == '-': 
                self.advance()
                if self.current_char == '=': #for -=symbol
                    tokens.append(Token(MINUS_EQUAL, "-="))
                    self.advance()
                elif self.current_char == '-': #for -- decre
                    tokens.append(Token(DECRE, "--"))
                    self.advance()
                elif self.current_char in all_num:
                    result, error = self.make_number()
                    result = Token(result.token, result.value * -1)
                    tokens.append(result)
                else:
                    tokens.append(Token(MINUS, "-"))
                
            elif self.current_char == '*': 
                self.advance()
                if self.current_char == '=': #for *= symbol
                    tokens.append(Token(MUL_EQUAL, "*=")) #for *// ending comet
                    self.advance()

                elif self.current_char == "/":
                    self.advance()
                    if self.current_char == "/":
                        tokens.append(Token(M_END_COMET, "*//"))
                        self.advance()
                    else:
                        errors.extend(["Missing ending slash for multi line comment!"])
                else:
                    tokens.append(Token(MUL, "*"))
                
            elif self.current_char == '/': 
                self.advance()
                if self.current_char == '=': #for /= symbol
                    tokens.append(Token(DIV_EQUAL, "/="))
                    self.advance()
                    if self.current_char not in (alphanum + equal_delim + space_delim):
                        errors.append(f"Invalid delimiter for /=. Cause:{self.current_char}")
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
                
            elif self.current_char == '%':
                tokens.append(Token(MODULUS, "%"))
                self.advance()
                if self.current_char not in (alphanum + equal_delim + space_delim):
                    errors.append(f"Invalid delimiter for %. Cause:{self.current_char}")
            elif self.current_char == '!': #logical operators (!, &&, ||)
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(NOT_EQUAL, "!=")) #for != symbol
                    self.advance()
                else:
                    tokens.append(Token(NOT_OP, "!"))
                    
            elif self.current_char == '&': #return error
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token(AND_OP, "&&"))
                    self.advance()
                else:
                    errors.extend([f"Please enter a valid symbol! User typed: & .Did you mean && ?"])
            elif self.current_char == '|': #return error
                self.advance()
                if self.current_char == '|':
                    tokens.append(Token(OR_OP, "||"))
                    self.advance()
                else:
                    errors.extend(["Please enter a valid symbol!"])
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
                    errors.extend(["Please enter a valid symbol! Did you mean ## ?"])
            elif self.current_char == "\"":
                result = self.make_string()
                if isinstance(result, list):  # check if make_word returned errors
                    errors.extend(result)
                    #break  # exit the loop if there are errors
                else:
                    tokens.append(result)
                    self.advance()
                    if self.current_char not in ("+", " ", ",", None):
                        errors.append("Invalid delimiter for string!")
            elif self.current_char == ',':
                tokens.append(Token(COMMA, ","))
                self.advance()
            elif self.current_char == ";":
                tokens.append(Token(SEMICOLON, ";"))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(COLON, ":"))
                self.advance()


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
            '''
            if num_count > 9:
                reached_limit_intel = True
            '''
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
                
                num_count += 1
                num_str += self.current_char
            self.advance()
        
        # check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            while self.current_char is not None and self.current_char.isalpha():
                num_str += self.current_char
                #added this advance para maskip nya yung identifier if ever
                self.advance()
            errors.append(f"Identifiers cannot start with a number! Cause: {num_str}")    
            if errors:
                return [], errors
               
            

        if num_count > 9:
            errors.append(f"You've reached the intel limit! Intel limit: 9 digits. Entered: {num_count} numbers. Cause: {num_str}")
            if dot_count == 0:
                #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
                return Token(INTEL, int(num_str)), errors
            else:
                return Token(GRAVITY, float(num_str)), errors
        if dec_count > 4:
            errors.append(f"You've reached the gravity limit! Gravity decimal limit: 4 digits. Entered: {dec_count} numbers. Cause: {num_str}")
            if dot_count == 0:
                #balik naalng yung token intel or gravity if need makita yung tokens ket may errors
                return Token(INTEL, int(num_str)), errors
            else:
                return Token(GRAVITY, float(num_str)), errors
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

        
        while self.current_char != None :
            
            if self.current_char == "b":
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
                        if self.current_char == "g":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            # catch if bang lang yung tinype ng user (for demo purposes)
                            if self.current_char == None:
                                return Token(BANG, ident)
                            
                            #delimiter ng bang defined in space_delim
                            if self.current_char not in space_delim: 
                                while self.current_char in alphanum and self.current_char not in space_delim:
                                    ident_count += 1
                                    if ident_count > 10:
                                        errors.extend(["Exceeded identifier limit!"])
                                        return errors
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == None:
                                        return Token(IDENTIFIER, ident)
                            else:
                                return Token(BANG, ident)
                           
                elif self.current_char == "l":
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(BLAST, "blast")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(BLAST, "blast")
                
            if self.current_char == "d": #do
                ident += self.current_char
                self.advance()
                ident_count += 1
                if self.current_char == "o":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    # catch if blast lang yung tinype ng user (for demo purposes)
                    if self.current_char == None:
                        return Token(DO, "do")
                
                    #delimiter ng bang defined in space_delim
                    if self.current_char not in space_delim: 
                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                            ident_count += 1
                            if ident_count > 10:
                                errors.extend(["Exceeded identifier limit!"])
                                return errors
                            ident += self.current_char
                            self.advance()
                            if self.current_char == None:
                                return Token(IDENTIFIER, ident)
                    else:
                        return Token(DO, "do")
                
                
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
                            if self.current_char == " ":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                            else:
                                return Token(ELSE, "else")
                            if self.current_char == "i":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                if self.current_char == "f":
                                    ident += self.current_char
                                    self.advance()
                                    ident_count += 1
                                    return Token(ELSEIF, "elseif")
                        else:
                            return Token(ELSE, "else")
                elif self.current_char == "n":
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
                                    # catch if blast lang yung tinype ng user (for demo purposes)
                                    if self.current_char == None:
                                        return Token(ENTITY, "entity")
                                
                                    #delimiter ng bang defined in space_delim
                                    if self.current_char not in space_delim: 
                                        ident += self.current_char
                                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                            ident_count += 1
                                            if ident_count > 10:
                                                errors.extend(["Exceeded identifier limit!"])
                                                return errors
                                            self.advance()
                                            if self.current_char == None:
                                                return Token(IDENTIFIER, ident)
                                    else:
                                        return Token(ENTITY, "entity")
                
            if self.current_char == "i": #if, inner, intel
                ident += self.current_char
                self.advance()
                ident_count += 1 
                if self.current_char == "f":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    return Token(IF, "if")
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(INNER, "inner")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(INNER, "inner")
                    elif self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "e":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "l":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(INTEL, "INTEL")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(INTEL, "intel")
                        
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(FALSE, "false")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(FALSE, "false")
                    
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(FORCE, "force")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(FORCE, "force")
                        elif self.current_char == "m":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            # catch if blast lang yung tinype ng user (for demo purposes)
                            if self.current_char == None:
                                return Token(FORM, "form")
                        
                            #delimiter ng bang defined in space_delim
                            if self.current_char not in space_delim: 
                                while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                    ident_count += 1
                                    if ident_count > 10:
                                        errors.extend(["Exceeded identifier limit!"])
                                        return errors
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == None:
                                        return Token(IDENTIFIER, ident)
                            else:
                                return Token(FORM, "form")
                
            if self.current_char == "g": #gravity
                ident += self.current_char
                self.advance()
                ident_count += 1 
                if self.current_char == "r":
                    ident += self.current_char
                    self.advance()
                    ident_count += 1
                    if self.current_char == "a":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "v":
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
                                        # catch if blast lang yung tinype ng user (for demo purposes)
                                        if self.current_char == None:
                                            return Token(GRAVITY, "gravity")
                                    
                                        #delimiter ng bang defined in space_delim
                                        if self.current_char not in space_delim: 
                                            while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                                ident_count += 1
                                                if ident_count > 10:
                                                    errors.extend(["Exceeded identifier limit!"])
                                                    return errors
                                                ident += self.current_char
                                                self.advance()
                                                if self.current_char == None:
                                                    return Token(IDENTIFIER, ident)
                                        else:
                                            return Token(GRAVITY, "gravity")
                                
                
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
                                        # catch if blast lang yung tinype ng user (for demo purposes)
                                        if self.current_char == None:
                                            return Token(LANDING, "landing")
                                    
                                        #delimiter ng bang defined in space_delim
                                        if self.current_char not in space_delim: 
                                            while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                                ident_count += 1
                                                if ident_count > 10:
                                                    errors.extend(["Exceeded identifier limit!"])
                                                    return errors
                                                ident += self.current_char
                                                self.advance()
                                                if self.current_char == None:
                                                    return Token(IDENTIFIER, ident)
                                        else:
                                            return Token(LANDING, "landing")
                    elif self.current_char == "u":
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
                                    # catch if blast lang yung tinype ng user (for demo purposes)
                                    if self.current_char == None:
                                        return Token(LAUNCH, "launch")
                                
                                    #delimiter ng bang defined in space_delim
                                    if self.current_char not in space_delim: 
                                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                            ident_count += 1
                                            if ident_count > 10:
                                                errors.extend(["Exceeded identifier limit!"])
                                                return errors
                                            ident += self.current_char
                                            self.advance()
                                            if self.current_char == None:
                                                return Token(IDENTIFIER, ident)
                                    else:
                                        return Token(LAUNCH, "launch")
                
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(OUTER, "outer")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(OUTER, "outer")
                
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
                                    # catch if blast lang yung tinype ng user (for demo purposes)
                                    if self.current_char == None:
                                        return Token(SATURN, "saturn")
                                
                                    #delimiter ng bang defined in space_delim
                                    if self.current_char not in space_delim: 
                                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                            ident_count += 1
                                            if ident_count > 10:
                                                errors.extend(["Exceeded identifier limit!"])
                                                return errors
                                            ident += self.current_char
                                            self.advance()
                                            if self.current_char == None:
                                                return Token(IDENTIFIER, ident)
                                    else:
                                        return Token(SATURN, "saturn")
                
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
                                    # catch if blast lang yung tinype ng user (for demo purposes)
                                    if self.current_char == None:
                                        return Token(SHIFT, "shift")
                                
                                    #delimiter ng bang defined in space_delim
                                    if self.current_char not in space_delim: 
                                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                            ident_count += 1
                                            if ident_count > 10:
                                                errors.extend(["Exceeded identifier limit!"])
                                                return errors
                                            ident += self.current_char
                                            self.advance()
                                            if self.current_char == None:
                                                return Token(IDENTIFIER, ident)
                                    else:
                                        return Token(SHIFT, "shift")

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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(SKIP, "skip")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(SKIP, "skip")
                
                elif self.current_char == "t":
                        ident += self.current_char
                        self.advance()
                        ident_count += 1
                        if self.current_char == "a":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "r":
                                ident += self.current_char
                                self.advance()
                                ident_count += 1
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(STAR, "star")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(STAR, "star")
                
                
            
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
                                        # catch if blast lang yung tinype ng user (for demo purposes)
                                        if self.current_char == None:
                                            return Token(TAKEOFF, "takeoff")
                                    
                                        #delimiter ng bang defined in space_delim
                                        if self.current_char not in space_delim: 
                                            while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                                ident_count += 1
                                                if ident_count > 10:
                                                    errors.extend(["Exceeded identifier limit!"])
                                                    return errors
                                                ident += self.current_char
                                                self.advance()
                                                if self.current_char == None:
                                                    return Token(IDENTIFIER, ident)
                                        else:
                                            return Token(TAKEOFF, "takeoff")
                    
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
                                    # catch if blast lang yung tinype ng user (for demo purposes)
                                    if self.current_char == None:
                                        return Token(TRACE, "trace")
                                
                                    #delimiter ng bang defined in space_delim
                                    if self.current_char not in space_delim: 
                                        while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                            ident_count += 1
                                            if ident_count > 10:
                                                errors.extend(["Exceeded identifier limit!"])
                                                return errors
                                            ident += self.current_char
                                            self.advance()
                                            if self.current_char == None:
                                                return Token(IDENTIFIER, ident)
                                    else:
                                        return Token(TRACE, "trace")
                        elif self.current_char == "u":
                            ident += self.current_char
                            self.advance()
                            ident_count += 1
                            if self.current_char == "e":
                                ident += self.current_char
                                self.advance()     
                                ident_count += 1    
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(TRUE, "true")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        if ident_count > 10:
                                            errors.extend(["Exceeded identifier limit!"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                    return Token(TRUE, "true") 
                
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
                                            # catch if blast lang yung tinype ng user (for demo purposes)
                                            if self.current_char == None:
                                                return Token(UNIVERSE, "universe")
                                        
                                            #delimiter ng bang defined in space_delim
                                            if self.current_char not in space_delim: 
                                                while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                                    ident_count += 1
                                                    if ident_count > 10:
                                                        errors.extend(["Exceeded identifier limit!"])
                                                        return errors
                                                    ident += self.current_char
                                                    self.advance()
                                                    if self.current_char == None:
                                                        return Token(IDENTIFIER, ident)
                                            else:
                                                return Token(UNIVERSE, "universe") 
                
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
                            # catch if blast lang yung tinype ng user (for demo purposes)
                            if self.current_char == None:
                                return Token(VOID, "void")
                        
                            #delimiter ng bang defined in space_delim
                            if self.current_char not in space_delim: 
                                while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                    ident_count += 1
                                    if ident_count > 10:
                                        errors.extend(["Exceeded identifier limit!"])
                                        return errors
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == None:
                                        return Token(IDENTIFIER, ident)
                            else:
                                return Token(VOID, "void")
                  
                            
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
                                # catch if blast lang yung tinype ng user (for demo purposes)
                                if self.current_char == None:
                                    return Token(WHIRL, "whirl")
                            
                                #delimiter ng bang defined in space_delim
                                if self.current_char not in space_delim: 
                                    while self.current_char in alphanum and self.current_char not in lineEnd_delim:
                                        ident_count += 1
                                        print(ident_count)
                                        if ident_count > 10:
                                            errors.extend([f"Exceeded identifier limit! Characters entered: {ident_count}"])
                                            return errors
                                        ident += self.current_char
                                        self.advance()
                                        if self.current_char == None:
                                            return Token(IDENTIFIER, ident)
                                else:
                                   return Token(WHIRL, "whirl")
                else:
                    ident_count += 1
                    if ident_count > 10:
                        errors.extend([f"Exceeded identifier limit! Characters entered: {ident_count}"])
                        return errors
                       
            
            else:
                
                if self.current_char == None:
                    break
                if self.current_char == " ":
                    break
                if self.current_char in lineEnd_delim:
                    break
                if self.current_char in ident_delim:
                    break    
                if self.current_char in arithmetic_operator:
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
                        return errors
                
             
        if ident_count > 10:
            errors.extend([f"Exceeded identifier limit! Limit: 10 characters. Characters entered: {ident_count}. Cause: {ident}"])           

        
        if errors:
            return errors
        #print(ident_count)
        # pwede return Token(IDENTIFIER, ident), errors dito basta dalawa den yung value sa nag call (ex: result, error = cat.make_word)
        return Token(IDENTIFIER, ident)
            
        
    def make_string(self):
        string = ""
        errors = []
        self.advance()
        while self.current_char != "\"" and self.current_char != None :
            
            string += self.current_char
            self.advance()
        if self.current_char == "\"":
            return Token(STRING, f"\"{string}\"")
    
        elif self.current_char == None:
            errors.append("Expected closing quotation mark!")

        if errors:
            return errors
        
        
       
  

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    
    return tokens, error