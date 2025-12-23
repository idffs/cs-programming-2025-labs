print('Works with ms, sec, min, h (milliseconds, seconds, minutes, hours)')
ms = 'ms'
sec = 'sec'
m = 'min'
h = 'h'
def trans(a, b, c):
    int(a)
    if b == ms:
        a = a
    elif b == sec:
        a = a * 1000
    elif b == m:
        a = a * 60 * 1000
    elif b == h:
        a = a * 60 * 60 * 1000
    
    if c == ms:
        a = a
    elif c == sec:
        a = a / 1000
    elif c == m:
        a = a / 1000 / 60
    elif c == h:
        a = a / 1000 / 60 / 60
    return a
try:
    a = float(input('Enter Value:'))
    if a < 0:
        print('Time can\'t be negative')
        exit()
    elif a == 0:
        print('0 is the same in any other time')
        exit()
except ValueError:
    print('Invalid Input(Allowed - 15, 13.5, etc. )')
    exit()
try:
    b = str(input('Enter Time Value that into transform:'))
    c = str(input('Enter Time Value that in end transform:'))
except ValueError:
    print('Invalid Input(Allowed - ms, sec, m, h)')
    exit()
print(f"""Entered data:
{a} {b}""")

print(f"""Output data:
{trans(a, b, c):.1f} {c}""")