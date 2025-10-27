try:
    user = int(input('Type dog year old: '))
    if user < 1:
        print('Error: Need more than 1')
    elif user > 22:
        print('Error: Too much')
    else:
        if user <3:
            print(f'In human year old: {user * 10.5}')
        else:
            print(f'In human year old: {21 + (user - 2) * 4}')
except ValueError:
    print('Error: Not number')