def calcu(a, b):
    if a // 10000 >= 16:
        k1 = 5
    else:
        k1 = 0.3 * (a // 10000)
    if b in range(1, 4):
        k2 = 3
    elif b in range(4, 7):
        k2 = 5
    elif b > 6:
        k2 = 2
    ks = k1 + k2
    income = 0
    while y != b:
        c += a * (ks / 100)
        y += 1
        a += c
    return a, b, income, k1, k2
try:
    a, b = map(int, input('Enter your deposit and length in integer(value years): ').split())
    if a < 30000:
        print('Minimal deposit 30k(30000)')
        exit()
    calcu(a, b)
    print(f"""
    coefficient 1 - {k1}
    coefficient 2 - {k2}
    income - {c}
    """)
except ValueError:
    print('Not allowed any other symbols except integer numbers')
