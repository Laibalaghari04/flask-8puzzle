from flask import Flask, render_template, request, jsonify
import random
from solver import solve_puzzle, is_solvable, GOAL_STATE

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["GET"])
def generate():
    while True:
        state = list(GOAL_STATE)
        random.shuffle(state)
        if is_solvable(tuple(state)):
            return jsonify({"state": state})

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json
    state = tuple(data["state"])
    solution = solve_puzzle(state)
    return jsonify({"solution": solution})

if __name__ == "__main__":
    app.run(debug=True)