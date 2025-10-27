user = input('Type your password: ')
l = int(len(user))
list1 = []
f1 = 'No lowercase letter'
f11 = False
f2 = 'No uppercase letter'
f22 = False
f3= 'No number'
f33 = False
f4 = 'No special symbol'
f44 = False
p = 'Password aint strong. List of disadvantages:'
if l >= 8:
    for i in range(l):
        list1.append(int(ord(user[i])))
    for list1 in  list1:
        if 97 <= list1 <= 122:
                f11 = True
        elif 65 <= list1 <= 90:
            f22 = True
        elif 48 <= list1 <= 57:
            f33 = True
        elif 20 <= list1 <= 47 or  58 <= list1 <= 64:
            f44 = True
    if f11 == f22 == f33 == f44 == True:
        exit('Password is strong enough')
    else:
        print(p)
        if f11 == False: 
            print(f1)
        if f22 == False:
            print(f2)
        if f33 == False:
            print(f3)
        if f44 == False:
            print(f4)
else:
    print('Password need at least 8 symbols')