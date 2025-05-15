GOAL_STATE = (0, 1, 2, 3, 4, 5, 6, 7, 8)
MOVES = {'left': -1, 'right': 1, 'up': -3, 'down': 3}

class Node:
    def __init__(self, state, parent=None, action=None, cost=0, f_score=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.f_score = f_score

    def __lt__(self, other):
        return self.f_score < other.f_score

def heuristic(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_pos = GOAL_STATE.index(state[i])
            distance += abs(goal_pos // 3 - i // 3) + abs(goal_pos % 3 - i % 3)
    return distance

def get_neighbors(node):
    neighbors = []
    zero_index = node.state.index(0)
    for move, direction in MOVES.items():
        new_index = zero_index + direction
        if 0 <= new_index < 9:
            if (move == 'left' and zero_index % 3 == 0) or (move == 'right' and zero_index % 3 == 2):
                continue
            new_state = list(node.state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(Node(tuple(new_state), node, move))
    return neighbors

def recursive_best_first_search(node, f_limit):
    if node.state == GOAL_STATE:
        return node, 0

    successors = []
    for child in get_neighbors(node):
        child.cost = node.cost + 1
        child.f_score = max(child.cost + heuristic(child.state), node.f_score)
        successors.append(child)

    if not successors:
        return None, float('inf')

    while True:
        successors.sort(key=lambda x: x.f_score)
        best = successors[0]
        if best.f_score > f_limit:
            return None, best.f_score
        alternative = successors[1].f_score if len(successors) > 1 else float('inf')
        result, best.f_score = recursive_best_first_search(best, min(f_limit, alternative))
        if result:
            return result, best.f_score

def solve_puzzle(initial_state):
    root = Node(initial_state, None, None, 0, heuristic(initial_state))
    solution_node, _ = recursive_best_first_search(root, float('inf'))
    if not solution_node:
        return None
    path = []
    node = solution_node
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    return list(reversed(path))

def is_solvable(state):
    inv_count = 0
    tiles = [tile for tile in state if tile != 0]
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inv_count += 1
    return inv_count % 2 == 0