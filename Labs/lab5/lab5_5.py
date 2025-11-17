#Find max and min price of fruits(in task was anything from shop)
dict1 = {'Bananas': 3, 'Apples': 3, 'Qiwi': 5, 'Cabbage': 2, 'Carrot': 3}
ly = min(dict1, key=dict1.get)
re = max(dict1, key=dict1.get)
print(f'{re} - have max price, {ly} - have min price')