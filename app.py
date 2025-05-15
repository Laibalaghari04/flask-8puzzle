from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

# Preset boards by difficulty
boards = {
    "low": [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ],
    "medium": [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ],
    "high": [
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ]
}

goal = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 0))

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def find_zero(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

def swap(board, pos1, pos2):
    new_board = [list(row) for row in board]
    x1, y1 = pos1
    x2, y2 = pos2
    new_board[x1][y1], new_board[x2][y2] = new_board[x2][y2], new_board[x1][y1]
    return board_to_tuple(new_board)

def get_neighbors(board):
    x, y = find_zero(board)
    neighbors = []
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            neighbors.append(swap(board, (x,y), (nx,ny)))
    return neighbors

def solve_puzzle(start_board):
    start = board_to_tuple(start_board)
    if start == goal:
        return 0, [start]

    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return len(path)-1, path
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return -1, []

@app.route('/', methods=['GET', 'POST'])
def index():
    moves_count = None
    solution_steps = None
    selected_board = None

    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        selected_board = boards.get(difficulty)
        moves_count, solution_path = solve_puzzle(selected_board)
        # Format the solution path nicely for the template
        solution_steps = ['\n'.join(' '.join(str(num) for num in row) for row in step) for step in solution_path]

    return render_template('index.html', 
                           moves=moves_count,
                           solution=solution_steps,
                           board=selected_board)

if __name__ == '__main__':
    app.run(debug=True)
