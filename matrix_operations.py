

def rotate(Matrix, giro=1):
    '''Matrix is an list of n list (nxn)
       giro=1 anti-clock anti-clock. giro=-1 clock rotation

       returns: a matrix rotated 90 or -90 degrees. Or
                a matrix of None if giro !=1 or !=-1'''
    length = len(Matrix)  # For Reference, if len = 3 then length = 2
    rotated = [[None]*length for rows in range(length)]

    for i in range(length):
        for j in range(length):
            if giro == 1:  # giro antihorario
                rotated[length-1-j][i] = Matrix[i][j]
            elif giro == -1:  # giro horario
                rotated[j][length-1-i] = Matrix[i][j]
    return rotated


def show(matrix):
    "Prints the matrix "
    print('MATRIX:')
    for row in matrix:
        for column in row:
            print(column, end=' ')
        print()


def center(matrix):
    '''Returns a 2x2 or 1x1 matrix that is the center of the in matrix'''
    length = len(matrix)
    if length in [1, 2]:
        return matrix.copy()
    mitad = length//2
    center = [[]]
    # topleftt = (mitad-1, mitad-1)
    # topright = (mitad-1, mitad)
    # botleftt = (mitad, mitad-1)
    # botright = (mitad, mitad)
    if length % 2 == 0:
        # Center will be:
        # [[topleftt,topright],
        #  [botleftt, botright]]
        center.append([])
        for i in [mitad-1, mitad]:
            for j in [mitad-1, mitad]:
                center[i-mitad+1].append(matrix[i][j])
    else:
        center[0].append(matrix[mitad][mitad])
    return center


def obtusecenter(matrix):
    '''returns an (n-1)x(n-1) matrix, such as is the centered of input matrix'''
    lg = len(matrix)
    if lg <= 2:
        return matrix.copy()
    center = [[None]*(lg-2) for row in range(lg-2)]
    for i in range(1, lg-1):
        for j in range(1, lg-1):
            center[i-1][j-1] = matrix[i][j]
    return center


def ringlist(matrix, punto=(0, 0)):
    '''return a list of ring'''
    ring = []
    lng = len(matrix)
    if lng == 1:
        ring.append(matrix[0][0])
        return ring
    limx, limy = lng-1, lng-1
    j, i = punto
    dir = 1      # 1->positivo; -1->negativo
    sentido = True  # True->horizontal; False->vertical
    while (j, i) != punto or len(ring) == 0:
        ring.append(matrix[i][j])
        if sentido:
            j += dir
        else:
            i += dir
        if (j, i) == (limx, punto[1]) or (j, i) == (limx, limy) or\
                (j, i) == (punto[0], limy):
            sentido = not sentido
        if (j, i) == (limx, limy) or (j, i) == punto:
            dir *= -1
    return ring


def RINGSSS(matrix):
    t = matrix.copy()
    print(ringlist(t))
    while len(t) not in [1, 2]:
        t = obtusecenter(t)
        print(ringlist(t))


t = [[1, 2, 3, 4, 5],
     [6, 7, 8, 9, 10],
     [11, 12, 13, 14, 15],
     [16, 17, 18, 19, 20],
     [21, 22, 23, 24, 25]]
RINGSSS(t)
