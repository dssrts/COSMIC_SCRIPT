import lexer

while True:
    text = input('cosmic script > ')
    result = lexer.run(text)
    
    for item in result:
        print(item)