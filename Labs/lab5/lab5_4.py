#Sort tuple and if any argument not 'int' back to unsorted tuple
def f(x):
    for z in x:
        try:
            c = int(z)
            if c != z:
                return(x)
        except:
            return(x)
    z = list(x)
    z.sort()
    return tuple(z)
kort1 = (1, 9, 5, 2, 3)
print(f'Entered tuple:{kort1}')
print(f'Tuple after sorting with options: {f(kort1)}')