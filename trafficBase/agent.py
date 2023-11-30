from mesa import Agent
from queue import PriorityQueue

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.name = "Car"
        self.availability = False
        self.stopped = False
        self.grid_Map = []
        self.destination = []
        self.path = []

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        """possible_steps = [x for x  in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)]
        new_steps = []
        for step in possible_steps:
            try:
                agents = self.model.grid[step[0],step[1]]
                for agent in agents:
                    if agent.availability == True:
                        new_steps.append(step)
                    #if self.pos == step:
                    #    self.stopped = False
            except:
                pass
        #clean_steps = [a for a in possible_steps if a not in new_steps]
        self.model.grid.move_agent(self, self.random.choice(new_steps))"""
        def manhattan_distance(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        def reconstruct_path(came_from, current):
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path
        
        def car_in_next_cell(direction):
            Cars = []
            for agent in self.model.grid.get_cell_list_contents(direction):
                if agent.name == "Car":
                    Cars.append(agent)
            if Cars == []:
                return False
            else:
                return True
                
        def green_light(position):
            Traffic_Light = ''
            for agent in self.model.grid.get_cell_list_contents(position):
                if agent.name == "Traffic Light":
                    Traffic_Light = agent.state
            if Traffic_Light == True:
                return True
            elif Traffic_Light == False:
                return False
            elif Traffic_Light == '':
                return True
                
        
        def not_obstacle(position):
            Obstacles = []
            for agent in self.model.grid.get_cell_list_contents(position):
                if agent.name == "Obstacle":
                    Obstacles.append(agent)
            if Obstacles == []:
                return True
            else:
                return False
        
        def is_in_cross(a, b):
            return a[0] == b[0] or a[1] == b[1]


        def aStar_path(grid, start, goal):
            g_score = {cell:float('inf') for cell in grid}
            f_score = {cell:float('inf') for cell in grid}
            count = 0
            came_from = {}
            open_set = PriorityQueue()
            open_set.put((0, count, start))
            g_score[start] = 0
            f_score[start] = manhattan_distance(start, goal)
            grid_Map_keys = list(grid.keys())

            open_set_hash = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                open_set_hash.remove(current)
                if current == goal:
                    path = []
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.append(start)
                    path.reverse()
                    return path

                neighbors = []
                for d in 'NSEW':
                    if grid[current][d] == True:
                        if d == 'N':
                            neighbors.append((current[0], current[1] + 1))
                            neighbors.append((current[0] + 1, current[1] + 1))
                            neighbors.append((current[0] - 1, current[1] + 1))
                        if d == 'S':
                            neighbors.append((current[0], current[1] - 1))
                            neighbors.append((current[0] + 1, current[1] - 1))
                            neighbors.append((current[0] - 1, current[1] - 1))
                        if d == 'E':
                            neighbors.append((current[0] + 1, current[1]))
                            neighbors.append((current[0] + 1, current[1] + 1))
                            neighbors.append((current[0] + 1, current[1] - 1))
                        if d == 'W':
                            neighbors.append((current[0] - 1, current[1]))
                            neighbors.append((current[0] - 1, current[1] + 1))
                            neighbors.append((current[0] - 1, current[1] - 1))

                clean_neighbors = [a for a in neighbors if a in grid_Map_keys]
                #in_cross_order = sorted(clean_neighbors, key=lambda x: is_in_cross(x, goal))

                for neighbor in clean_neighbors:
                    temp_g_score = g_score[current] + 1
                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        if is_in_cross(neighbor, current):
                            f_score[neighbor] = temp_g_score + manhattan_distance(neighbor, goal) - 1
                        else:
                            f_score[neighbor] = temp_g_score + manhattan_distance(neighbor, goal)
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)

        def force_move(current, grid):
            neighbors = []
            for d in 'NSEW':
                if grid[current][d] == True:
                    if d == 'N':
                        neighbors.append((current[0], current[1] + 1))
                        neighbors.append((current[0] + 1, current[1] + 1))
                        neighbors.append((current[0] - 1, current[1] + 1))
                    if d == 'S':
                        neighbors.append((current[0], current[1] - 1))
                        neighbors.append((current[0] + 1, current[1] - 1))
                        neighbors.append((current[0] - 1, current[1] - 1))
                    if d == 'E':
                        neighbors.append((current[0] + 1, current[1]))
                        neighbors.append((current[0] + 1, current[1] + 1))
                        neighbors.append((current[0] + 1, current[1] - 1))
                    if d == 'W':
                        neighbors.append((current[0] - 1, current[1]))
                        neighbors.append((current[0] - 1, current[1] + 1))
                        neighbors.append((current[0] - 1, current[1] - 1))
            for neighbor in neighbors:
                if car_in_next_cell(neighbor) == False:
                    if green_light(neighbor) == True and neighbor in self.grid_Map:
                        self.model.grid.move_agent(self, neighbor)
                        break

        new_moves = aStar_path(self.grid_Map, self.pos, self.destination)
        try:
            if new_moves != None:
                if car_in_next_cell(new_moves[1]) == False:
                    if green_light(self.pos) == True and not_obstacle(new_moves[1]) == True and new_moves[1] in self.grid_Map:
                        self.model.grid.move_agent(self, new_moves[1])
                        self.path = new_moves[2:]
                else:
                    pass
                    #print('FORCED Disabled: No local proactivity')
                    force_move(self.pos, self.grid_Map)
            else:
                pass
                print('No path found to: ', self.destination)
                #print('FORCED Disabled: No local proactivity')
                force_move(self.pos, self.grid_Map)
        except:
            pass

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.num_agents -= 1
            self.model.destroyed_cars += 1
            return
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.last_state = "Green"
        self.name = "Traffic Light"
        self.availability = True
        self.timeToChange = timeToChange
    
    def changeColor(self):
        def is_cross_adjacent(a, b):
            return a[0] == b[0] or a[1] == b[1]

        radial_cells = [x for x in self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=3)]
        neighboring_traffic_lights = []

        for agent in radial_cells:
            if agent.name == "Traffic Light" and not is_cross_adjacent(self.pos, agent.pos):
                neighboring_traffic_lights.append(agent.state)


        if self.state == False:
            if neighboring_traffic_lights.count(True) <= 2:
                self.state = not self.state
        elif self.state == True:
            if neighboring_traffic_lights.count(False) <= 2:
                self.state = not self.state

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Destination"
        self.availability = True

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.name = "Obstacle"
        self.availability = False

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = {}
        self.name = "Road"
        self.availability = True

    def step(self):
        pass
