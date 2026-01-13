def matrixsum(n, mat1, mat2):
    res = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(mat1[i][j] + mat2[i][j])
        res.append(row)
    return res  

def matmade(n):
    matrix = []
    for l in range(n):
        try:
            row = list(map(int, input().split()))
            if len(row) != n:
                print('Row has incorrect number of elements')
                exit()
            matrix.append(row)
        except ValueError:
            print('Matrix allow only integers')
            return None
    return matrix

def matprint(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

try:
    n = int(input('Enter matrix size nxn(n > 2): '))
    if n < 3:
        print('Matrix can\'t be less than 3x3')
        exit()

    print('Enter Matrix 1, elements that n rows with integers separated by space')
    matrix1 = matmade(n)
    if matrix1 == None:
        exit()

    print('Enter Matrix 2, elements that n rows with integers separated by space')
    matrix2 = matmade(n)
    if matrix2 == None:
        exit()

    result  = matrixsum(n, matrix1, matrix2)

    print("Result matrix:")
    matprint(result)

except ValueError:
    print('Invalid input: allow only integer')
    exit()