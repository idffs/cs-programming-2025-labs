try:
    user = int(input('Type a year(example, 2025): '))
    if user % 4 == 0 and user % 100 != 0:
        print(f'{user} is leap year ')
    elif user % 400 == 0:
        print(f'{user} is leap year')
    else:
        print(f'{user} isnt leap year')
except ValueError:
    print('Error: Type a year in numeric value, not a word or smth else')