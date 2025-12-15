try:
    user = input('Type a year(example, 2025): ')
    if '.' in user or ',' in user:
        print('Error: Type a year without float \"."')
        exit()
    if int(user) < 0:
        print('Error: Year can\'t be negative')
        exit()
    user = int(user)
    if user % 4 == 0 and user % 100 != 0 or user % 400 == 0:
        print(f'{user} is leap year ')
    else:
        print(f'{user} isn\'t leap year')
except ValueError:
    print('Error: Type a year in valid integer')