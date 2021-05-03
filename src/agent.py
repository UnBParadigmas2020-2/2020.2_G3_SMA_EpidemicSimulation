import enum
import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class State(enum.IntEnum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2
    DECEASED = 3


# An agent in an epidemic model
class MyAgent(Agent):
    def init(self, unique_id, model):
        super().init(unique_id, model)
        self.age = self.random.normalvariate(20, 40)
        self.state = State.SUSCEPTIBLE
        self.infection_time = 0

    # Move the agent
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    # Check infection status
    def status(self):
        if self.state == State.INFECTED:
            drate = self.model.death_rate
            alive = np.random.choice([0, 1], p=[drate, 1-drate])
            t = self.model.schedule.time-self.infection_time
            if alive == 0 and t > self.random.normalvariate(1, 21):
                self.state = State.DECEASED
            if t >= self.model.get_recovery_time():
                self.state = State.RECOVERED

    # Find close contacts and infect
    def contact(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for other in cellmates:
                if self.random.random() > self.model.ptrans:
                    continue
                if self.state is State.INFECTED and other.state is State.SUSCEPTIBLE:
                    other.state = State.INFECTED
                    other.infection_time = self.model.schedule.time

    def step(self):
        self.status()
        self.move()
        self.contact()