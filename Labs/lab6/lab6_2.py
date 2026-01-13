print('Minimal deposit 30k(30000)')
def calcu(a, b):
    if a // 10000 > 16:
        k1 = 5
    else:
        k1 = 0.3 * (a // 10000)
    if 1 <= b <= 3:
        k2 = 3
    elif 4 <= b <= 6:
        k2 = 5
    elif b > 6:
        k2 = 2
    ks = k1 + k2
    c = 0
    y = 0
    ksf = ks / 100
    a = a
    while y != b:
        c += a * ksf
        y += 1
        a += c
    c = round(c)
    return {
        'cof1': k1, 
        'cof2': k2,
        'income':c
    }
try:
    a, b = map(int, input('Enter your deposit and length in integer(value years): ').split())
    if a < 30000:
        print('Less than minimal deposit')
        exit()
    elif b < 1:
        print('Deposit lenght can\'t be less 1 year')
        exit()
    res = calcu(a, b)
    print(f"""
    coefficient 1 - {res['cof1']}
    coefficient 2 - {res['cof2']}
    income - {res['income']}
    """)
except ValueError:
    print('Not allowed any other symbols except integers')
