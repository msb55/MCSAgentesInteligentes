frontier = []
explored_set = []

actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Node():
    def __init__(self, state, parent=None, energy_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.energy_cost = energy_cost + (parent.energy_cost if parent else 0)
        self.heuristic_cost = heuristic_cost
        self.cost = self.energy_cost + heuristic_cost

    def __str__(self):
        return str(self.state)


def init_search():
    global frontier
    global explored_set

    explored_set = []
    frontier = []


def search(map, agent_position, food_position):
    init_search()
    frontier.append((0, Node(state=agent_position)))

    while True:    
        node = frontier.pop(0)[1]
        explored_set.append(node.state)

        if goal_test(node, food_position):
            return solution(node)

        else:
            expand_node(map, node, food_position)
            if not frontier:
                raise Exception("Solucao nao encontrada")

def heuristic_cost(food_position, current_position):
    return (abs(food_position[0] - current_position[0]) +
            abs(food_position[1] - current_position[1]))

def energy_cost(map, current_position):
    ground_cost = {
               0: 0,
               1: 999,
               2: 5,
               3: 10,
               4: 20
               }
    return ground_cost[map[current_position[0]][current_position[1]]]
    

def goal_test(node, food_position):
    return node.state == food_position

def solution(node):
    solution_path = []
    while node:
            solution_path.insert(0, node.state)
            node = node.parent
    return solution_path

def expand_node(map, node, food_position):
    global frontier
    global explored_set

    for action in actions:
        state = (node.state[0] + action[0], node.state[1] + action[1])
        if check_valid_node(state, map):
            child_node = Node(state, node, energy_cost(map, state), heuristic_cost(food_position, state))
            frontier.append((child_node.cost, child_node))
    frontier = sorted(frontier, key=lambda x: x[0])

def check_valid_node(state, map):
    return (0<=state[0]<len(map) and 
            0<=state[1]<len(map) and 
            state not in explored_set and
            state not in [node[1].state for node in frontier] and
            map[state[0]][state[1]] != 1)
