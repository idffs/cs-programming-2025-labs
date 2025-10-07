w = input('Write any word: ')
s = ''
for i in range(1, len(w)+1):
    s += f'w[i]' + f'{i}'
    print(s)