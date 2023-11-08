import lexer

while True:
    text = input('cosmic script > ')
    print("markcys")
    print("v2")
    result = lexer.run(text)
    
    for item in result:
        print(item)