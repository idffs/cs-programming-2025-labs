user = int(input('Type dog year old: '))
if user > 0 and user < 3:
    print(f'In human year old: {user * 10.5}')
elif user > 2 and user < 23:
    print(f'In human year old: {21 + (user - 2) * 4}')
else:
    print('Wront type of information')