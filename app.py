from flask import Flask, render_template, request, redirect, url_for
import copy

app = Flask(__name__)

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def get_neighbors(state):
    neighbors = []
    x, y = next((i, j) for i, row in enumerate(state) for j, val in enumerate(row) if val == 0)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors

def is_goal(state):
    return state == GOAL_STATE

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            board_input = request.form['board'].replace('\r', '').split('\n')
            board = [list(map(int, row.strip().split())) for row in board_input]
            if len(board) != 3 or any(len(row) != 3 for row in board):
                raise ValueError
            return render_template('index.html', board=board, message="Board loaded.")
        except Exception:
            return render_template('index.html', message="Invalid input. Please enter 3x3 integers.")
    return render_template('index.html', board=None)

if __name__ == '__main__':
    app.run(debug=True)
