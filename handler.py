from queue import PriorityQueue

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    matrixes = []
    i = 0
    while i < len(lines):
        # Read first line of metadata
        data = [int(matrixData) for matrixData in lines[i].strip().split()]

        if len(data) == 1:
            break
        
        rows = data[0]

        # Read the matrix
        matriz = [[int(lineaMatriz) for lineaMatriz in line.strip().split()] for line in lines[i+1:i+1+rows]]
        # Append the metadata and matrix to the list
        matrixes.append((data, matriz))

        # Move to the next matrix
        i += rows + 1

    return matrixes

def biggestDimensions(matrixes):
    max_rows = 0
    max_cols = 0

    for data, matriz in matrixes:
        rows = data[0]
        cols = data[1]

        if rows > max_rows:
            max_rows = rows
        if cols > max_cols:
            max_cols = cols

    return max_rows, max_cols
    
def depthFirstSearch(matrix, start, goal):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False]*cols for _ in range(rows)]
    stack = [(start, [start])]
    shortest = None

    while stack:
        (cell, path) = stack.pop()
        (x, y) = cell
        if cell == goal:
            if shortest is None or len(path) < len(shortest):
                shortest = path
        else:
            for dx, dy in [(matrix[x][y], 0), (0, matrix[x][y]), (-matrix[x][y], 0), (0, -matrix[x][y])]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny]:
                    visited[nx][ny] = True
                    stack.append(((nx, ny), path + [(nx, ny)]))

    return shortest

def uniformCostSearch(matrix, start, goal):
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    pq = PriorityQueue()
    pq.put((0, start, [start]))  # Cost from start to start is 0, and the path is just the start

    while not pq.empty():
        cost, current, path = pq.get()
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path  # Return the path to reach the goal

        x, y = current
        jump_distance = matrix[x][y]
        for dx, dy in [(jump_distance, 0), (0, jump_distance), (-jump_distance, 0), (0, -jump_distance)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) not in visited:
                    new_path = path + [(nx, ny)]
                    pq.put((cost + 1, (nx, ny), new_path))  # Update the path with the new cell

    return None  # Goal is not reachable

