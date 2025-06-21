import time
import math
import heapq
from collections import deque
from config import *

# Neighbor states
def get_neighbors(state):
    blank_index = state.index(0)
    neighbors = []
    for move, direction in directions.items():
        new_blank_index = blank_index + direction
        if move == 'Left' and blank_index % 3 == 0:
            continue
        if move == 'Right' and blank_index % 3 == 2:
            continue
        if 0 <= new_blank_index < 9:
            new_state = list(state)
            new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
            neighbors.append((tuple(new_state), move))
    return neighbors


# Manhattan heuristic
def manhattan_distance(state):
    distance = 0
    for i, val in enumerate(state):
        if val != 0:
            x1, y1 = i // 3, i % 3
            x2, y2 = goal_positions[val]
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


# Euclidean heuristic
def euclidean_distance(state):
    distance = 0
    for i, val in enumerate(state):
        if val != 0:
            x1, y1 = i // 3, i % 3
            x2, y2 = goal_positions[val]
            distance += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance


def breadth_first_search(initial_state):
    frontier = deque([(initial_state, [], 0)])
    explored = set()
    nodes_expanded = 0
    while frontier:
        state, path, cost = frontier.popleft()
        explored.add(state)
        if state == goal_state:
            return path, cost, nodes_expanded
        for neighbor, move in get_neighbors(state):
            if neighbor not in explored and all(neighbor != f[0] for f in frontier):
                frontier.append((neighbor, path + [move], cost + 1))
        nodes_expanded += 1
    return None


def depth_first_search(initial_state):
    frontier = [(initial_state, [], 0)]
    explored = set()
    nodes_expanded = 0
    while frontier:
        state, path, cost = frontier.pop()
        explored.add(state)
        if state == goal_state:
            return path, cost, nodes_expanded
        if cost < 20:
            for neighbor, move in get_neighbors(state):
                if neighbor not in explored and all(neighbor != f[0] for f in frontier):
                    frontier.append((neighbor, path + [move], cost + 1))
        nodes_expanded += 1
    return None


def iterative_deepening_search(initial_state, goal_state):
    def dfs_limited(state, goal, depth, path, visited):
        if state == goal:
            return path
        if depth == 0:
            return None
        for neighbor, move in get_neighbors(state):
            if neighbor not in visited:
                visited.add(neighbor)
                result = dfs_limited(neighbor, goal, depth - 1, path + [move], visited)
                if result is not None:
                    return result
                visited.remove(neighbor)
        return None
    depth = 0
    start_time = time.time()
    total_expanded = 0
    while True:
        visited = set([initial_state])
        result = dfs_limited(initial_state, goal_state, depth, [], visited)
        total_expanded += len(visited)
        if result is not None:
            return {
                "path_to_goal": result,
                "cost_of_path": len(result),
                "number_of_moves": len(result),
                "nodes_expanded": total_expanded,
                "time_taken": time.time() - start_time
            }
        depth += 1
        if depth > 50:
            break
    return None


# A* Search
def a_star_search(initial_state, heuristic="Manhattan"):
    if heuristic == "Manhattan":
        h_func = manhattan_distance
    elif heuristic == "Euclidean":
        h_func = euclidean_distance
    else:
        raise ValueError("Unsupported heuristic")

    start_time = time.time()
    frontier = []
    heapq.heappush(frontier, (h_func(initial_state), 0, initial_state, []))
    explored = set()
    nodes_expanded = 0

    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        if state == goal_state:
            return {
                "path_to_goal": path,
                "cost_of_path": g,
                "number_of_moves": len(path),
                "nodes_expanded": nodes_expanded,
                "time_taken": time.time() - start_time
            }
        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1
        for neighbor, move in get_neighbors(state):
            if neighbor not in explored:
                new_g = g + 1
                new_f = new_g + h_func(neighbor)
                heapq.heappush(frontier, (new_f, new_g, neighbor, path + [move]))
    return None
