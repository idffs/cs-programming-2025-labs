user = input('Type number to know will divisible by 6 or not: ')
q = len(str(user))
w = 0
for i in range(q):
    w += int(user[i])
if int(user[-1]) % 2 == 0 and w % 3 == 0:
    print('It would divisible by 6')
else:
    print('This number wont divisible by 6')