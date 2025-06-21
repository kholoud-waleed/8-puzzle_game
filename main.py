import time
import tkinter as tk
from config import *
from tkinter import messagebox, ttk
from game_algos import breadth_first_search, depth_first_search, iterative_deepening_search, a_star_search


# Input parser
def parse_input(input_str):
    try:
        numbers = list(map(int, input_str.strip().split()))
        if len(numbers) == 9 and set(numbers) == set(range(9)):
            return tuple(numbers)
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numbers 0-8 exactly once, separated by spaces.")
        return None

# Show initial grid
def show_sequence():
    input_str = entry.get()
    initial_state = parse_input(input_str)
    if initial_state:
        for i, num in enumerate(initial_state):
            buttons[i]["text"] = "" if num == 0 else str(num)

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

# Animate solution
def animate_solution(path):
    for move in path:
        root.update()
        time.sleep(0.5)
        blank_index = next(i for i, btn in enumerate(buttons) if btn["text"] == "")
        target_index = blank_index + directions[move]
        if 0 <= target_index < 9:
            buttons[blank_index]["text"], buttons[target_index]["text"] = buttons[target_index]["text"], buttons[blank_index]["text"]

# Solve button handler
def solve_puzzle():
    initial_state = parse_input(entry.get())
    if not initial_state:
        return

    algorithm = algorithm_choice.get()
    solution = None
    result = None

    if algorithm == "BFS":
        solution = breadth_first_search(initial_state)
    elif algorithm == "DFS":
        solution = depth_first_search(initial_state)
    elif algorithm == "IDS":
        result = iterative_deepening_search(initial_state, goal_state)
        if result:
            solution = result["path_to_goal"], result["cost_of_path"], result["nodes_expanded"]
    elif algorithm == "A*":
        selected_heuristic = heuristic_choice.get()
        result = a_star_search(initial_state, heuristic=selected_heuristic)
        if result:
            solution = result["path_to_goal"], result["cost_of_path"], result["nodes_expanded"]
    else:
        messagebox.showerror("Selection Error", "Please select a valid algorithm.")
        return

    if solution:
        path, cost, nodes_expanded = solution
        animate_solution(path)

        result_window = tk.Toplevel(root)
        result_window.title("Solution Report")

        tk.Label(result_window, text="Path to goal: " + " -> ".join(path)).pack()
        tk.Label(result_window, text="Cost of path: " + str(cost)).pack()
        tk.Label(result_window, text="Total moves: " + str(len(path))).pack()
        tk.Label(result_window, text="Nodes expanded: " + str(nodes_expanded)).pack()
        if result:
            tk.Label(result_window, text="Time taken: {:.4f} seconds".format(result["time_taken"])).pack()
    else:
        messagebox.showinfo("Result", "No solution found or depth limit exceeded.")

# Show/hide heuristic dropdown based on algorithm
def update_heuristic_visibility(event):
    if algorithm_choice.get() == "A*":
        heuristic_label.grid()
        heuristic_choice.grid()
    else:
        heuristic_label.grid_remove()
        heuristic_choice.grid_remove()

# GUI setup
root = tk.Tk()
root.title("8-Puzzle Solver")

buttons = []
for i in range(9):
    button = tk.Button(root, text="", width=5, height=2, font=("Arial", 18))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

entry_label = tk.Label(root, text="Enter initial state (e.g., '1 2 5 3 4 0 6 7 8'):")
entry_label.grid(row=3, column=0, columnspan=3)
entry = tk.Entry(root, width=20)
entry.grid(row=4, column=0, columnspan=3)

show_button = tk.Button(root, text="Show Sequence", command=show_sequence)
show_button.grid(row=5, column=0, columnspan=3)

algorithm_label = tk.Label(root, text="Select Algorithm:")
algorithm_label.grid(row=6, column=0, columnspan=3)
algorithm_choice = ttk.Combobox(root, values=["BFS", "DFS", "IDS", "A*"])
algorithm_choice.grid(row=7, column=0, columnspan=3)
algorithm_choice.current(0)
algorithm_choice.bind("<<ComboboxSelected>>", update_heuristic_visibility)

heuristic_label = tk.Label(root, text="Select Heuristic (for A*):")
heuristic_label.grid(row=8, column=0, columnspan=3)
heuristic_choice = ttk.Combobox(root, values=["Manhattan", "Euclidean"])
heuristic_choice.grid(row=9, column=0, columnspan=3)
heuristic_choice.current(0)

# Hide heuristic selection initially
heuristic_label.grid_remove()
heuristic_choice.grid_remove()

solve_button = tk.Button(root, text="Solve", command=solve_puzzle)
solve_button.grid(row=10, column=0, columnspan=3)

root.mainloop()
