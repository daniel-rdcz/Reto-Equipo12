from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json, random, os

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []
        self.destinations = []
        self.obstacles = []
        self.grid_Map= {}
        self.locations_wo_cars = []
        self.step_count = 0
        self.car_agents = 0
        self.destroyed_cars = 0
        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<", "*"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        if col == "v":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': True, 'E': False, 'W': False}
                        elif col == "^":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': True, 'S': False, 'E': False, 'W': False}
                        elif col == "<":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': False, 'E': False, 'W': True}
                        elif col == ">":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': False, 'E': True, 'W': False}
                        elif col == "*":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': True, 'S': True, 'E': True, 'W': True}
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    # elif col in ["◊", "∆", "«", "»"]:
                    elif col in ["u", "n", "L", "R"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col in ["n", "L"] else True, int(dataDictionary[col]))
                        if col == "u":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': True, 'E': False, 'W': False}
                        elif col == "n":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': True, 'S': False, 'E': False, 'W': False}
                        elif col == "L":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': False, 'E': False, 'W': True}
                        elif col == "R":
                            self.grid_Map[(c,self.height - r - 1)] = {'N': False, 'S': False, 'E': True, 'W': False}
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        position = [c, self.height - r - 1]
                        self.obstacles.append(position)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid_Map[(c,self.height - r - 1)] = {'N': True, 'S': True, 'E': True, 'W': True}
                        key = (c,self.height - r - 1)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.destinations.append((c, self.height - r - 1))


        self.num_agents = N
        self.running = True

    def step(self):
        def car_not_in_pos(position):
            for agent in self.schedule.agents:
                if agent.name == 'Car' and agent.pos == position:
                    return False
            return True
        def percentage_of_occupied_grid(grid):
            count = 0
            for agent in self.schedule.agents:
                if agent.name == 'Car' and agent.pos == grid:
                    count += 1
            return count/len(grid)*100

        '''Advance the model by one step.'''
        self.schedule.steps
        self.locations_wo_cars = list(self.grid_Map.keys())
        clean_car_grid = [x for x in self.locations_wo_cars if x not in self.destinations]
        self.step_count += 1
        #print(len(clean_car_grid))
        if percentage_of_occupied_grid(clean_car_grid) <= 99:
            if self.step_count % 10 == 0:
                for i in range(20):
                    position = random.choice(clean_car_grid)
                    if car_not_in_pos(position) == True:
                        agent = Car(f"c_{self.step_count}_*{i}", self)
                        agent.grid_Map = self.grid_Map
                        agent.destination = random.choice(self.destinations)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, position)
        print(self.destroyed_cars)
        self.schedule.step()