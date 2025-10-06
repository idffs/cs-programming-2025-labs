input_number = input('Число от 1 до 9: ')
int(input_number)
if input_number == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9:
    for i in range(1, 10):
        a = (f'{input_number} * {i} = {int(input_number) * i}')
        print(a)
else:
    print('Неверно заданное число')