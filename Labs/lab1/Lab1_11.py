numbers = input('Write 3 numbers through comma: ')
a,b,c = map(int, numbers.split(','))
Task = (a + c) // b
print(f"Результат вычисления: {Task}")
