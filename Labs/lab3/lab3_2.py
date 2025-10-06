input_number = input('Число от 1 до 9: ')
int(input_number)
for i in range(1, 10+1):
    a = (f'{input_number} * {i} = {int(input_number) * i}')
    print(a)