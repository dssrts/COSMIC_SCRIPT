import lexer

while True:
    text = input('cosmic script > ')
    #kaya dalawa kasi dalawa nirererturn ng make_tokens()
    result, error = lexer.run('<stdin>', text)
    print("this is the main branch")
    
    for item in result:
        print(item)
    for err in error:
        print(err)
    '''
    if error:
        for err in error:
            print(err)
    '''