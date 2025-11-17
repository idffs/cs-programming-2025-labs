#Made dict where studens and their avg grade, where output is student with best grade
li = [("Anna", [5, 4, 5]), ("Ivan", [3, 4, 4]), ("Maria", [5, 5, 5])]
dic = {}
avg = {}
for stud, grades in li:
    avg = sum(grades) / len(grades)
    dic[stud] = avg
print('Stud with best avg grade: ')
best_stud = ''
best_avg = 0
for stud, avg in dic.items():
    if avg > best_avg:
        best_avg = avg
        best_stud = stud
print(f'{best_stud} -- {best_avg:.2f}')