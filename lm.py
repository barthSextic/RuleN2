"""
List Manipulation Library
"""


def scale2D(array, c):
    for x in range(len(array)):
        for y in range(len(array[x])):
            array[x][y] *= c
    return array


# scale array by a factor c
"""
take an array and a factor c

[ f g h
  i j k
  l m n ]
>
[ f f g g h h
  f f g g h h
  i i j j k k 
  i i j j k k 
  l l m m n n
  l l m m n n ]
"""


def stretch2D(array, c):
    returnArray = []
    for x in range(len(array)):
        lineBuff = []
        for y in range(len(array[x])):
            for mult in range(c):
                lineBuff.insert(c*y+c, array[x][y])
        for copy in range(c):
            returnArray.insert(c*x+c, lineBuff)
    return returnArray
