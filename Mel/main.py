import lexer

while True:
    text = input('cosmic script > ')
    result, error = lexer.run(text)
    
    for item in result:
        print(item)
    for err in error:
        print(err)
    '''
    if error:
        for err in error:
            print(err)
    '''