import itertools

def maxmin_areas(points):
    triangles= list(itertools.combinations(points, 3))
    squares = [getSquare(x) for x in triangles if getSquare(x)!=0]
    return (max(squares), min(squares))

def getSquare(triangle):
    return (abs(triangle[0][0]*(triangle[1][1]-triangle[2][1])+triangle[1][0]*(triangle[2][1]-triangle[0][1])+triangle[2][0]*(triangle[0][1]-triangle[1][1]))/2)

print(maxmin_areas([(-5, 4), (4, -2), (5, 5), (2, 2)]))