# -*- coding: cp1251 -*-
# Словарь
tr = {
    'Jupiter': 'юпитер',
    'Pluto':'плутон',
    'Mars': 'марс',
    'Sun': 'солнце',
    'Moon': 'луна',
    'Saturn': 'сатурн',
    'Venus':'венера',
    'Earth':'земля',
    'Mercury':'меркурий',
    'Neptune':'нептун',
    'Uranus':'уран'
}
u = input('Напишите название планеты с маленькой буквы: ')
rev_tr = {value: key for key, value in tr.items()}
if u in rev_tr:
    print(f'По английски это - {rev_tr[u]}')
else:
    print('Не найдено')