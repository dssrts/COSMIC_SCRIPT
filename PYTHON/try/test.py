def res_word(string):
#check if it's an alphabet
    flag = []
    word = list(string)
    #bang and blast
    
    if (word[0]== "b"):
        if word[1] == "a":
            if word[2] == "n":
                if word[3] == "g":
                    flag.append("bang")
                    return "bang!"
        elif word[1] == "l":
            if word[2] == "a":
                if word[3] == "s":
                    if word[4] == "t":
                        flag.append("blast")
                        return "blast!"
        
    else:
        return "Identifier!"

while True:
    word = input("input a word: ")

    print(res_word(word))