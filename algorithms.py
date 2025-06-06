import heapq
import random

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bfs_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    queue = [start]
    visited = {start}
    steps = [start]
    while queue:
        current = queue.pop(0)
        if current == goal:
            break
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    steps.append(neighbor)
    return steps

def dfs_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    stack = [start]
    visited = {start}
    steps = [start]
    while stack:
        current = stack.pop()
        if current == goal:
            break
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    steps.append(neighbor)
    return steps

def astar_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    came_from = {start: None}
    steps = []
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        steps.append(current)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return steps, path
            
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                    
                tentative_g = g_score[current] + 1
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return steps, []  # No path found

def dijkstra_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    steps = []
    while open_set:
        current = heapq.heappop(open_set)[1]
        steps.append(current)
        if current == goal:
            break
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_set, (tentative_g, neighbor))
    return steps

def beam_search(grid, start, goal, beam_width=3):
    rows = len(grid)
    cols = len(grid[0])
    current_nodes = [start]
    visited = {start}
    steps = [start]
    while current_nodes:
        current_nodes.sort(key=lambda node: heuristic(node, goal))
        current_nodes = current_nodes[:beam_width]
        next_nodes = []
        for current in current_nodes:
            if current == goal:
                steps.append(current)
                return steps
            for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (current[0]+delta[0], current[1]+delta[1])
                if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_nodes.append(neighbor)
                        steps.append(neighbor)
        current_nodes = next_nodes
    return steps

def greedy_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    open_set = [start]
    visited = {start}
    steps = [start]
    while open_set:
        open_set.sort(key=lambda node: heuristic(node, goal))
        current = open_set.pop(0)
        steps.append(current)
        if current == goal:
            break
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    open_set.append(neighbor)
    return steps

def iddfs_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    steps = []
    def dls(current, depth, visited):
        steps.append(current)
        if current == goal:
            return True
        if depth == 0:
            return False
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1 or neighbor in visited:
                    continue
                visited.add(neighbor)
                if dls(neighbor, depth-1, visited):
                    return True
                visited.remove(neighbor)
        return False
    max_depth = rows * cols
    for depth in range(max_depth):
        visited = {start}
        if dls(start, depth, visited):
            break
    return steps

def bidirectional_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    queue_start = [start]
    queue_goal = [goal]
    visited_start = {start}
    visited_goal = {goal}
    steps = [start, goal]
    while queue_start and queue_goal:
        current_start = queue_start.pop(0)
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current_start[0]+delta[0], current_start[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor in visited_start:
                    continue
                visited_start.add(neighbor)
                queue_start.append(neighbor)
                steps.append(neighbor)
                if neighbor in visited_goal:
                    return steps
        current_goal = queue_goal.pop(0)
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current_goal[0]+delta[0], current_goal[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor in visited_goal:
                    continue
                visited_goal.add(neighbor)
                queue_goal.append(neighbor)
                steps.append(neighbor)
                if neighbor in visited_start:
                    return steps
    return steps

def depth_limited_dfs(grid, start, goal, limit=20):
    rows = len(grid)
    cols = len(grid[0])
    steps = []
    def dls(current, depth, visited):
        steps.append(current)
        if current == goal:
            return True
        if depth == 0:
            return False
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1 or neighbor in visited:
                    continue
                visited.add(neighbor)
                if dls(neighbor, depth-1, visited):
                    return True
                visited.remove(neighbor)
        return False
    visited = {start}
    dls(start, limit, visited)
    return steps

def random_walk_search(grid, start, goal, max_steps=1000):
    rows = len(grid)
    cols = len(grid[0])
    current = start
    steps = [current]
    for _ in range(max_steps):
        if current == goal:
            break
        neighbors = []
        for delta in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+delta[0], current[1]+delta[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue
                neighbors.append(neighbor)
        if not neighbors:
            break
        current = random.choice(neighbors)
        steps.append(current)
    return steps

def q_learning_search(grid, start, goal, episodes=5000, learning_rate=0.1, discount_factor=0.95, epsilon=1.0, min_epsilon=0.05, epsilon_decay=0.99, max_steps_per_episode=400, clear_callback=None):
    """
    Advanced Q-Learning for pathfinding with:
    - Distance-based reward
    - Stronger loop/oscillation penalties
    - Faster epsilon decay
    - Early episode termination
    - Visualization callback to clear highlights every 1000 episodes
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Initialize Q-table
    q_table = {}
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 1:  # Only initialize for non-wall cells
                q_table[(i, j)] = {
                    (-1, 0): 0,  # up
                    (1, 0): 0,   # down
                    (0, -1): 0,  # left
                    (0, 1): 0    # right
                }
    
    steps = [start]  # Track exploration steps
    for episode in range(episodes):
        state = start
        visited_in_episode = {start}
        recent_states = []  # For oscillation detection
        for step in range(max_steps_per_episode):
            # Epsilon-greedy action selection
            if random.random() < epsilon:
                action = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            else:
                action = max(q_table[state].items(), key=lambda x: x[1])[0]
            
            next_state = (state[0] + action[0], state[1] + action[1])
            reward = -1  # Default step penalty
            prev_dist = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
            # Check if next state is valid
            if (0 <= next_state[0] < rows and 0 <= next_state[1] < cols):
                if grid[next_state[0]][next_state[1]] == 1:
                    reward = -20  # Strong wall penalty
                    next_state = state  # Stay in place
                elif next_state == goal:
                    reward = 100  # Goal reward
                elif next_state not in visited_in_episode:
                    reward = 2  # Reward for new cell
                else:
                    reward = -20  # Strong penalty for revisiting (loop)
            else:
                reward = -20  # Out of bounds penalty
                next_state = state  # Stay in place
            
            # Distance-based reward
            new_dist = abs(next_state[0] - goal[0]) + abs(next_state[1] - goal[1])
            if new_dist < prev_dist:
                reward += 3  # Getting closer
            elif new_dist > prev_dist:
                reward -= 3  # Getting further
            
            # Dead end check (if not goal or wall)
            if (next_state != goal and grid[next_state[0]][next_state[1]] != 1):
                valid_moves = 0
                for d in [(-1,0), (1,0), (0,-1), (0,1)]:
                    neighbor = (next_state[0]+d[0], next_state[1]+d[1])
                    if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and
                        grid[neighbor[0]][neighbor[1]] != 1 and neighbor != state):
                        valid_moves += 1
                if valid_moves == 0:
                    reward += -30  # Strong dead end penalty
            
            # Oscillation/short loop penalty
            recent_states.append(state)
            if len(recent_states) > 6:
                recent_states.pop(0)
            if recent_states.count(state) > 2:
                reward -= 30  # Strong penalty for oscillation
            
            # Q-learning update
            old_value = q_table[state][action]
            next_max = max(q_table[next_state].values())
            new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
            q_table[state][action] = new_value
            
            state = next_state
            steps.append(state)
            visited_in_episode.add(state)
            if state == goal:
                # Bonus for short path
                reward += 100 * (rows * cols / (step + 1))
                break
        # Decay epsilon faster
        if epsilon > min_epsilon:
            epsilon *= epsilon_decay
            epsilon = max(min_epsilon, epsilon)
        # Clear highlights every 1000 episodes
        if clear_callback and episode > 0 and episode % 1000 == 0:
            clear_callback()
    
    # Extract the final path using the learned Q-values
    path = [start]
    current = start
    visited = {start}
    for _ in range(rows * cols):
        action = max(q_table[current].items(), key=lambda x: x[1])[0]
        next_state = (current[0] + action[0], current[1] + action[1])
        if (0 <= next_state[0] < rows and 0 <= next_state[1] < cols and
            grid[next_state[0]][next_state[1]] != 1 and next_state not in visited):
            current = next_state
            path.append(current)
            visited.add(current)
            if current == goal:
                break
        else:
            break
    if path[-1] != goal:
        path = []  # No valid path found
    return steps, path

ALGORITHMS = {
    "BFS": bfs_search,
    "DFS": dfs_search,
    "A*": astar_search,
    "Dijkstra": dijkstra_search,
    "Beam Search": beam_search,
    "Greedy Best-First": greedy_search,
    "IDDFS": iddfs_search,
    "Bidirectional BFS": bidirectional_search,
    "Depth-Limited DFS": depth_limited_dfs,
    "Random Walk": random_walk_search,
    "Q-Learning": q_learning_search,
}
