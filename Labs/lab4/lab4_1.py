try:    
    user = int(input('Type temperature in room(example, 25): '))
    if user >= 20:
        print('Conditioner is off')
    else:
        print('Conditioner is on')
except ValueError:
    print('Error: Not number ')