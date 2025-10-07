w = input('Write any word: ')
s = ''
for i in range(1, len(w)+1):
    s = w[len(w)] + f'{i}'
    print(s)