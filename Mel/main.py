import lexer

while True:
    text = input('cosmic script > ')
    print("pano ba nag pull req!!!!")
    result = lexer.run(text)
    
    for item in result:
        print(item)