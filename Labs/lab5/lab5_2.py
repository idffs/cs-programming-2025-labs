#Made list with square of numbers
list1 = []
for i in range(1, 6):
    list1.append(i)
l = len(list1)
print(list1)
for i in range(l):
    list1[i] = list1[i] ** 2
print(list1)