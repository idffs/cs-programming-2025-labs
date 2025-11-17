user = int(input('Type number of month: '))
if user == 12 or user == 1 or user == 2:
    print('Its Winter')
elif user == 3 or user == 4 or user == 5:
    print('Its Sprint')
elif user == 6 or user == 7 or user == 8:
    print('Its Summer')
elif user == 9 or user == 10 or user == 11:
    print('Its Autumn')
else:
    print('Not exist month')