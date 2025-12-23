def calcu(a, b):
    if a // 10000 >= 16:
        k1 = 5
    else:
        k1 = 0.3 * (a // 10000)

    if 1 <= b < 4:
        k2 = 3
    elif 4 <= b < 7:
        k2 = 5
    else: 
        k2 = 2
    
    ks = k1 + k2
    total_income = 0
    current_amount = a
    

    for year in range(b):
        year_income = current_amount * (ks / 100)
        total_income += year_income
        current_amount += year_income  
    
    return a, b, total_income, k1, k2


try:
    a, b = map(int, input('Enter your deposit and length in integer (value years): ').split())
    if a < 30000:
        print('Minimal deposit is 30,000')
    else:
        initial_deposit, years, income, k1, k2 = calcu(a, b)
        print(f"""
        Coefficient 1 - {k1}
        Coefficient 2 - {k2}
        Income - {income:.2f}
        Final amount - {initial_deposit + income:.2f}
        """)
except ValueError:
    print('Only integers are allowed')
