import lexer

while True:
    text = input('cosmic script > ')
    #kaya dalawa kasi dalawa nirererturn ng make_tokens()
    result, error = lexer.run('<stdin>', text)
    
    #print(result)

    
    """ for err in error:
        print(error) """
    #THIS IS FOR THE PARSER
    # if error: 
    #     print(error)
    # else: 
    #     print(result)

    #REMOVE THIS FOR THE PARSER KASI IBA NA YUNG ERRORS NG PARSER  
    #THIS IS FOR THE LEXER  
    for item in result:
        print(item)
    for err in error:
        print(err.as_string())
    '''
    if error:
        for err in error:
            print(err)
    '''
    #hello jayson 
    #hiiii