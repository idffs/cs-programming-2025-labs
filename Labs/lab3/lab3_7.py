w = input('Type any word: ')
s = ''
l = len(w)
e = 1
for i in range(0, l):
    s += f'{w[i]}' + f'{e}'
    e += 1
print(s)