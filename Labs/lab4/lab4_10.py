list1 = [4, 6, 8, 9, 10]
try:
    user = int(input('Type any number: '))
    b = 2
    c = 0
    a = int(user ** 0.5)
    if user == 1:
        exit('1 - not simple or composite number')
    elif user == 0:
        print('0 - not simple or composite number')
    elif user < 0:
        print('Negative number cant be simple or composite number')
    else:
        if user > 10:
            while user % b != 0 and b <= a:
                    b += 1
            if user % b == 0:
                exit(f'{user} - composite number')
            else:
                exit(f'{user} - simple number')        
        elif user in list1:
            exit(f'{user} - composite number')
        else:
            exit(f'{user} - simple number')
           

        if c == 0:
            print(f'{user} - simple number')
        else:
            print(f'{user} - composite number')
except ValueError:
    print('Error: not number')