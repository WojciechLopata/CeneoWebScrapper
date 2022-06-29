with open("requirements.txt","r") as file:
    a=''
    for line in file:
        a=a+line+"<br>"
    print(a)