#Change 3 to 30 in list
list1 = []
for i in range(1, 11):
    list1.append(i)
print(list1)
l = len(list1)
for i in range(l):
    if list1[i] == 3 in list1:
        list1[i] = 30
print(list1)