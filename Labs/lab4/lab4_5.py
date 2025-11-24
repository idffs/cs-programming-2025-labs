print('Use english layout')
user = input('Type your password: ')
l = len(user)
list1 = []
list2 = []
f1 = 'no lowercase character'
f11 = False
f2 = 'no uppercase character'
f22 = False
f3= 'no number'
f33 = False
f4 = 'no special(allowed) character'
f44 = False
p = 'Password aint strong. Theres no:'
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
        if f11 == False: 
            list2.append(f1)
        if f22 == False:
            list2.append(f2)
        if f33 == False:
            list2.append(f3)
        if f44 == False:
            list2.append(f4)
        print(p, ', '.join(list2))
else:
    print('Password need at least 8 characters')
