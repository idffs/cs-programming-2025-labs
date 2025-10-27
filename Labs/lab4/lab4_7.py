user = input('Type any 3 number separated by space: ')
q, w, e = map(int, user.split()) 
if q < w and q < e:
    print(q)
elif w < q and w < e:
    print(w)
elif e < q and e < w:
    print(e)