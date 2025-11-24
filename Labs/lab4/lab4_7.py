try:
    user = input('Type any 3 numbers separating by space:')
    q, w, e = map(int, user.split()) 
    if q < w and q < e:
        print(q)
    elif w < q and w < e:
        print(w)
    else:
        print(e)
except ValueError:
            print('Error: You need to type any 3 numbers with given conditions')