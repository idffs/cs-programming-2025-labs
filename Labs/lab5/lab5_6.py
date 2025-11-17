#Get arguments and made a dict where key and value same thing
def trans(a, s):
    slov = {a: s}
    return slov
u = ''
li1 = []
ress = {}
print('Enter data(5 times): ')
while len(li1) != 5:
    u = input()
    li1.append(u)
print(li1)
for i in range(5):
    res = trans(li1[i], li1[i])
    ress.update(res)
print(ress)