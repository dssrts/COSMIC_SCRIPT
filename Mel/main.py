import lexer

while True:
    text = input('cosmic script > ')
    print("markcys")
    result = lexer.run(text)
    
    for item in result:
        print(item)