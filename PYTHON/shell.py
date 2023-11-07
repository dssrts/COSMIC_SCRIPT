import basic

start = ""
text = ""
while start != "takeoff":
    print("Remember to start your journey with ""takeoff""!")
    start = input('CS Compiler> ')

print("You may now begin your adventure, traveler!\n")

while True :
    text = input('cosmic script > ')

    if "landing" in text:
        print("Farewell traveler!")
        break
    result, error = basic.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)