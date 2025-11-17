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
The stone breaks the scissors''')
item = ('stone', 'scissors', 'paper', 'lizard', 'spock')
rules = {
    'stone': ['scissors', 'lizard'],
    'scissors': ['paper', 'lizard'],
    'paper': ['stone', 'spock'],
    'lizard': ['spock', 'paper'],
    'spock': ['stone', 'scissors']
}
try:
    print('''
    1 - Stone
    2 - Scissors
    3 - Paper
    4 - Lizard
    5 - Spock
    ''')
    u= int(input('Enter number: '))
    us = item[u-1]
    if 1 <= u <= 5:
        print(f'Selected: {us}')
    else:
        exit(print('Out of options'))
except ValueError:
    exit(print('Not number'))
pc = random.choice(item)
print(f'{us} vs {pc}')
if us == pc:
    print('Draw!')
elif pc in rules[us]:
    print('User wins!')
else:
    print('PC wins!')