
all_num = '0123456789'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
space_delim = " "

#errors
error = []

#TOKENS


#operators
PLUS = '+'
MINUS = '-'
MUL = '*'
DIV = '/'
LPAREN = '('
RPAREN = ')'

#reserved words
TAKEOFF = 'takeoff' #Start
LANDING = 'landing' #End
#Data types
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

#literals
IDENTIFIER = 'IDENTI'
COMMA = 'COMMA'
SPACE = 'SPACE'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
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

        while self.current_char is not None:
            if self.current_char in '\t':
                self.advance()
            elif self.current_char in ' ':
                tokens.append(Token(SPACE, "\" \""))
                self.advance()
            elif self.current_char in all_letters:
                result = self.make_word()
                if isinstance(result, list):  # Check if make_word returned errors
                    errors.extend(result)
                    break  # Exit the loop if there are errors
                else:
                    tokens.append(result)
            elif self.current_char in all_num:
                result = self.make_number()
                if isinstance(result, list):  # Check if make_number returned errors
                    errors.extend(result)
                    break  # Exit the loop if there are errors
                else:
                    tokens.append(result)
            elif self.current_char == '+':
                tokens.append(Token(PLUS, "+"))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS, "-"))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL, "*"))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV, "/"))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN, "("))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN, ")"))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(COMMA, ","))
                self.advance()

        if errors:
            return errors
        else:
            return tokens          

    def make_number(self):
        num_str = ''
        dot_count = 0
        errors = []

        while self.current_char is not None and self.current_char in all_num + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    errors.append(f"Invalid character '{self.current_char}' in number.")
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        # Check if there are letters after the number
        if self.current_char is not None and self.current_char.isalpha():
            errors.append("Identifiers cannot start with a number!")

        if errors:
            return errors
        elif dot_count == 0:
            return Token(INTEL, int(num_str))
        else:
            return Token(GRAVITY, float(num_str))
        
    
    def make_word(self):
        ident = ""
        
        while self.current_char != None and self.current_char in alphanum:
            if self.current_char == "b": #bang blast
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
                                ###test
                            else:
                                return Token(BANG, ident)
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
                                if self.current_char == "i":
                                    ident += self.current_char
                                    self.advance()
                                    if self.current_char == "f":
                                        ident += self.current_char
                                        self.advance()
                                        return Token(ELSEIF, "elseif")
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
            if self.current_char == "i":
                ident += self.current_char
                self.advance()
                if self.current_char == "f":
                    ident += self.current_char
                    self.advance()
                    return Token(IF, "if")
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
                                return Token(BLAST, "blast")
            
            else:
                if self.current_char.isdigit() == True:
                    ident += str(self.current_char)
                    self.advance()
                else:
                    ident += self.current_char
                    self.advance()

        return Token(IDENTIFIER, ident)
            
            #self.advance()

       
  

def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    
    return tokens
