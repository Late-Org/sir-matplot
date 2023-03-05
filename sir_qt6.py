import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QPen
import numpy as np

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
    def __init__(self, num_agents, width, height, initial_infected, radius):
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.initial_infected = initial_infected
        self.radius = radius
       
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
            print(len(neighbors), " neighbors of ", infected, " are ", str(neighbors))
            for neighbor in neighbors:
                if neighbor.state == 'S':
                    if np.random.random() < 0.6:
                        neighbor.change_state('I')
                        self.susceptible.remove(neighbor)
                        new_infected.append(neighbor)
            if np.random.random() < 0.9:
                infected.change_state('R')
                self.infected.remove(infected)
                new_recovered.append(infected)
            elif np.random.random() < 0.3: # death
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
                if moving_agent.x > 800: moving_agent.x = 800
                if moving_agent.x < 0: moving_agent.x = 0
                # vertical move
                movey = np.random.randint(-1 * movement, movement)
                moving_agent.y = moving_agent.y + movey
                if moving_agent.y > 800: moving_agent.y = 800
                if moving_agent.y < 0: moving_agent.y = 0

    def plot(self, qp):
        colors = {'S':QColor(0,0,255), 'I':QColor(255,0,0), 'R':QColor(0,255,0), 'D':QColor(0,0,0)}
        for agent in self.agents:
            brush = colors[agent.state]
            qp.setBrush(brush)
            qp.drawEllipse(agent.x, agent.y, 10, 10)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Epidemic Simulation'
        self.width = int(800)
        self.height = int(800)
        self.num_agents = 500
        self.initial_infected = 150
        self.radius = 15
        self.infection_propability = 0.8
        self.movement = 5
        self.world = World(self.num_agents, self.width, self.height, self.initial_infected, self.radius)
        self.timer = self.startTimer(500)

    def paintEvent(self, event):
        qp = QPainter(self)
        self.world.plot(qp)

    def timerEvent(self, event):
        self.world.update()
        self.world.move_agents(self.movement)
        self.update()


if __name__ == '__main__':
    title = 'Epidemic Simulation'
    width = 800
    height = 800
    # num_agents = 500
    # initial_infected = 5
    # radius = 15
    # infection_propability = 0.8
    # movement = 5

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(0, 0, width, height)
    window.setWindowTitle(title)
    window.show()
    sys.exit(app.exec())