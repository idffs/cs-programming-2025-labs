input_number = input('Число от 1 до 9: ')
if int(input_number) > 0 and int(input_number) < 10:
    for i in range(1, 11):
        a = (f'{input_number} * {i} = {int(input_number) * i}')
        print(a)
else:
     print('Неверно заданное число')