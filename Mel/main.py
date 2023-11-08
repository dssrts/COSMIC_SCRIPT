import lexer

while True:
    text = input('cosmic script > ')
    print("markcys")
    print("9 40 am")
    result = lexer.run(text)
    
    for item in result:
        print(item)