print('Works with numeric value from 1 to 22')
try:
    user = int(input('Write dog years old: '))
    if user < 1:
        print('Error: Need more than 0')
    elif user > 22:
        print('Error: Too much')
    else:
        if user <3:
            print(f'In human years: {user * 10.5}')
        else:
            print(f'In human years: {21 + (user - 2) * 4}')
except ValueError:
    print('Error: Not numeric value')