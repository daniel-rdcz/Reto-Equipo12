from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):


        self.num_agents = N
        self.running = True

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []

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
                    if col == "v":
                        agent = RoadDown(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    if col == "^":
                        agent = RoadUp(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    
                    if col == ">":
                        agent = RoadRight(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    
                    if col == "<":
                        agent = RoadLeft(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "S":
                        vecinos_tipo = self.grid.get_neighbors((c, self.height - r), moore = True)
                        vecinos_pos = self.grid.get_neighborhood((c, self.height - r), moore = True)
                        vecinos = [(p, f) for p, f in zip(vecinos_pos, vecinos_tipo) if f == isinstance(f, RoadUp) or isinstance(f, RoadDown)]
                        direction = 270.0
                        for v in vecinos:
                            if v[0] == (c, self.height - r + 1) and isinstance(v[1], RoadUp):
                                direction = 270.0
                            elif v[0] == (c, self.height - r + 1) and isinstance(v[1], RoadDown):
                                direction = 90.0
                            elif v[0] == (c, self.height - r - 1) and isinstance(v[1], RoadUp):
                                direction = 270.0
                            elif v[0] == (c, self.height - r - 1) and isinstance(v[1], RoadDown):
                                direction = 90.0
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False, int(dataDictionary[col]), direction)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "s":
                        vecinos_tipo = self.grid.get_neighbors((c, self.height - r - 1), moore = False)
                        vecinos_pos = self.grid.get_neighborhood((c, self.height - r - 1), moore = False)
                        vecinos = [(p, f) for p, f in zip(vecinos_pos, vecinos_tipo) if f == isinstance(f, RoadLeft) or isinstance(f, RoadRight)]
                        direction = 180.0
                        for v in vecinos:
                            if v[0] == (c - 1, self.height - r - 1) and isinstance(v[1], RoadLeft):
                                direction = 180.0
                            elif v[0] == (c + 1, self.height - r - 1) and isinstance(v[1], RoadRight):
                                direction = 0.0
                            elif v[0] == (c - 1, self.height - r - 1) and isinstance(v[1], RoadRight):
                                direction = 0.0
                            elif v[0] == (c + 1, self.height - r - 1) and isinstance(v[1], RoadLeft):
                                direction = 180.0

                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, True, int(dataDictionary[col]), direction)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        for i in range(self.num_agents):
            agent = Car(f"c_{i}", self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (i, 0))

        

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()