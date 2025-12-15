try:
    user = input('Type number to know will it divisible by 6 or not: ')
    if int(user) < 0:
        print('Error: Type positive value')
        exit()
    elif int(user) == 0:
        print('0 can\'t be divisible by 6')
        exit()
    q = len(str(user))
    w = 0
    for i in range(q):
        w += int(user[i])
    if int(user[-1]) % 2 == 0 and w % 3 == 0:
        print('It would divisible by 6')
    else:
        print('This number won\'t divisible by 6')
except ValueError:
    print('Error: Needs numeric value')