try:
    user = int(input('Type your buy cost: '))

    if user < 0:
        print('Buy cost can\'t be negative')
    elif 0 <= user < 1000:
        print('Your discount: 0%')
        print(f'Price is {user}')
    elif user >= 1000 and user < 5000:
        print('Your discount: 5%')
        print(f'Price is {user * 0.95}')
    elif user >= 5000 and user <10000:
        print(f'Your discount: 10%')
        print(f'Price is {user * 0.9}')
    elif user >= 10000:
        print('Your discount: 15%')
        print(f'Price is {user * 0.85}')
except ValueError:
    print('Allowed is numeric value, any other will be considered an error')