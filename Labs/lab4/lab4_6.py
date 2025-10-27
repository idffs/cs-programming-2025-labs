user = int(input('Type a year: '))
if user % 4 == 0 and user % 100 != 0:
    print(f'{user} is leap year ')
elif user % 400 == 0:
    print(f'{user} is leap year')
else:
    print(f'{user} isnt leap year')