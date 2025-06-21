# Goal state and directions
goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
directions = {'Up': -3, 'Down': 3, 'Left': -1, 'Right': 1}
goal_positions = {val: (i // 3, i % 3) for i, val in enumerate(goal_state)}
