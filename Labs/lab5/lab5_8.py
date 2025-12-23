#Камень-Ножницы-Бумага-Ящерица-Спок
import random
print('''Game: Rock-Scissors-Paper-Lizard-Spock
Rules: 

Scissors cut paper
Paper covers the stone
The stone crushes the lizard
the lizard poisons Spock
Spock breaks the scissors
Scissors decapitate a lizard
The lizard eats paper
Paper sets up Spock
Spock vaporizes the stone
The stone breaks the scissors

To close programm enter "quit"
I will remind it for you every 10 games''')
item = ('stone', 'scissors', 'paper', 'lizard', 'spock')
rules = {
    'stone': ['scissors', 'lizard'],
    'scissors': ['paper', 'lizard'],
    'paper': ['stone', 'spock'],
    'lizard': ['spock', 'paper'],
    'spock': ['stone', 'scissors']
}
game = 0
while True:
    game += 1
    if game % 10 == 0:
        print('''
        
        Remind, to exit enter "quit"
        
        ''')
    try:
        print('''
        1 - Stone
        2 - Scissors
        3 - Paper
        4 - Lizard
        5 - Spock
        ''')
        u= input('Enter number: ')
        if u == 'quit':
            print('Closing game...')
            exit()
        elif '.' in u or ',' in u:
            print('Not use any float')
            exit()
        elif int(u) < 1 or int(u) > 5:
            print('Error: Out of options')
            exit()
        else:
            u = int(u)
            us = item[u-1]
            print(f'Selected: {us}')
    except ValueError:
        print('Error: Not number')
        exit()
    pc = random.choice(item)
    print(f'{us} vs {pc}')
    if us == pc:
        print('Draw!')
    elif pc in rules[us]:
        print('User wins!')
    else:
        print('PC wins!')