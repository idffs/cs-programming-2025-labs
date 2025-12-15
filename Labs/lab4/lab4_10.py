list1 = [4, 6, 8, 9, 10]
list2 = [2, 3, 5, 7]
try:
    user = input('Type any number: ')
    if '.' in user or ',' in user:
        print('Error: allowed only integer')
        exit()
    user = int(user)
    if user == 1 or user == 0:
        print(f'{user} - not simple or composite number')
    elif user < 0:
        print('Negative number can\'t be simple or composite number')
    else:
        b = 2
        a = int(user ** 0.5)
        if user in list1:
            print(f'{user} - composite number')
        elif user in list2:
            print(f'{user} - simple number')
        elif user > 10:
            while user % b != 0 and b <= a:
                    b += 1
            if user % b == 0:
                print(f'{user} - composite number')
            else:
                print(f'{user} - simple number')
except ValueError:
    print('Error: not numeric value')