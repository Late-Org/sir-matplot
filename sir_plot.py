import numpy as np
import matplotlib.pyplot as plt
# from scipy.spatial import distance
import time

class Agent:
    def __init__(self, x, y, state, radius):
        self.x = x
        self.y = y
        self.state = state
        self.radius = radius
   
    def __repr__(self):
        return f"({self.x},{self.y})"
       
    def move(self, x, y):
        self.x = x
        self.y = y
   
    def change_state(self, state):
        self.state = state
       
    def distance(self, other_agent):
        xx = (self.x - other_agent.x) ** 2
        yy = (self.y - other_agent.y) ** 2
        dist = np.sqrt( xx + yy )
        # dist2 = distance.euclidean((self.x, self.y), (other_agent.x, other_agent.y))
        # print(xx, " x ", yy, " y ", dist, " - ", dist2)
        return dist
   
class World:
    def __init__(self, num_agents, width, height, initial_infected, radius, infection_prop, recover_prop, death_prop):
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.initial_infected = initial_infected
        self.radius = radius
        self.infection_prop = infection_prop
        self.recover_prop = recover_prop
        self.death_prop = death_prop

       
        self.agents = []
        self.infected = []
        self.susceptible = []
        self.recovered = []
        self.dead = []
       
        for i in range(num_agents):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            state = 'S'
            if i < self.initial_infected:
                state = 'I'
            agent = Agent(x, y, state, self.radius)
            self.agents.append(agent)
            if state == 'S':
                self.susceptible.append(agent)
            elif state == 'I':
                self.infected.append(agent)
            else:
                self.recovered.append(agent)
   
    def get_neighbors(self, agent):
        neighbors = []
        for other_agent in self.agents:
            if other_agent != agent and agent.distance(other_agent) <= agent.radius:
                neighbors.append(other_agent)
        return neighbors
   
    def update(self):
        new_infected = []
        new_recovered = []
        new_dead = []
        for infected in self.infected:
            neighbors = self.get_neighbors(infected)
            for neighbor in neighbors:
                if neighbor.state == 'S':
                    if np.random.random() < self.infection_prop:
                        neighbor.change_state('I')
                        self.susceptible.remove(neighbor)
                        new_infected.append(neighbor)
            if np.random.random() < self.recover_prop:
                infected.change_state('R')
                self.infected.remove(infected)
                new_recovered.append(infected)
            elif np.random.random() < self.death_prop: # death
                infected.change_state('D')
                self.infected.remove(infected)
                new_dead.append(infected)
        self.recovered += new_recovered
        self.infected += new_infected
        self.dead += new_dead

    def move_agents(self, movement):
        for moving_agent in self.agents:
            if moving_agent.state != 'D':
                # horizontal move
                movex = np.random.randint(-1 * movement, movement)
                moving_agent.x = moving_agent.x + movex
                if moving_agent.x > 100: moving_agent.x = 100
                if moving_agent.x < 0: moving_agent.x = 0
                # vertical move
                movey = np.random.randint(-1 * movement, movement)
                moving_agent.y = moving_agent.y + movey
                if moving_agent.y > 100: moving_agent.y = 100
                if moving_agent.y < 0: moving_agent.y = 0
   
    def plot(self):
        fig, ax = plt.subplots()
        xs = [agent.x for agent in self.agents]
        ys = [agent.y for agent in self.agents]
        states = [agent.state for agent in self.agents]
        colors = {'S':'blue', 'I':'red', 'R':'green', 'D':'black'}
        ax.scatter(xs, ys, c=[colors[state] for state in states])
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        # print(fig.get_gid)
        plt.show()

# TODO: 
#  - Move these parameters into User Interface (or input file)

num_agents = 100
initial_infected = 5
radius = 15  # How far infection spread to neighbours
infection_prop = 0.8
recover_prop = 0.7
death_prop = 0.4
width=100
height=100
movement = 5 # how many pixels agent move at max

# Run the application
if __name__ == '__main__':
    # Initiate scene
    world = World(num_agents, width, height, initial_infected, radius, infection_prop, recover_prop, death_prop)
    # Run iteration
    for i in range(10):
        world.update()
        world.plot() # Note you need to close Window manually to get updated view
        world.move_agents(movement)
        a = False