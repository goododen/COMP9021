# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and determines the size of the largest
# isosceles triangle, consisting of nothing but 1s and whose base can be either
# vertical or horizontal, pointing either left or right or up or down.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def size_of_largest_isosceles_triangle():
    graph = [[0 for m in range(len(grid))] for n in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]:
                graph[i][j] = 1
                if (1 <= i) and (1 <= j < 9):
                    graph[i][j] = min(graph[i-1][j-1], graph[i-1][j], graph[i-1][j+1]) + 1
    u = max(x for matrix in graph for x in matrix)
    
    for j in range(len(grid)):
        for i in range(len(grid)):
            if grid[i][j]:
                graph[i][j] = 1
                if (1 <= j) and (1 <= i < 9):
                    graph[i][j] = min(graph[i-1][j-1], graph[i][j-1], graph[i+1][j-1]) + 1
    l = max(x for matrix in graph for x in matrix)
   
    for i in range(len(grid) - 1, - 1, -1):
        for j in range(len(grid) - 1, - 1, -1):
             if grid[i][j]:
                graph[i][j] = 1
                if (i < 9) and (1 <= j < 9):
                    graph[i][j] = min(graph[i+1][j-1], graph[i+1][j], graph[i+1][j+1]) + 1
    d = max(x for matrix in graph for x in matrix)

    for j in range(len(grid) - 1, -1, -1):
        for i in range(len(grid) - 1, -1, -1):
            if grid[i][j]:
                graph[i][j] = 1
                if (j < 9) and (1 <= i < 9):
                    graph[i][j] = min(graph[i-1][j+1], graph[i][j+1], graph[i+1][j+1]) + 1
    r = max(x for matrix in graph for x in matrix)
	
    return max(u, d, l, r)



try:
    arg_for_seed, density = (abs(int(x)) for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
print('The largest isosceles triangle has a size of',
      size_of_largest_isosceles_triangle()
     )
