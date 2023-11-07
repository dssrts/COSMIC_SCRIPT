
all_num = '0123456789'
all_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#errors
error = []

#TOKENS

#types
TT_INT = 'INTEL'
TT_FLOAT = 'GRAVITY'

#operators
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

#reserved words
BANG = 'BANG'
BLAST = 'BLAST'
INTEL = 'INTEL'

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
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        
        while self.current_char != None:
            if self.current_char in '\t':
                self.advance()
            if self.current_char in ' ':
                tokens.append(Token(SPACE))
                self.advance()
            elif self.current_char in all_letters:
                tokens.append(self.make_word())
            elif self.current_char in all_num:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(COMMA))
                self.advance()
        
        return tokens      

    def make_number(self):
        num_str = ''
        dot_count = 0
        
        while self.current_char != None and self.current_char in all_num + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
        
    def make_word(self):
        ident = ""
        
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
                            return Token(BANG, "bang")
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
