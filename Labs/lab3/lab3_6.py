s = input('Type number: ')
s = int(s)
a = 0
b = 1
c = 0
while c <= s:
    print(a)
    a, b = b, a + b
    c += 1

