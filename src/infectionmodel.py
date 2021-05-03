import numpy as np
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .agent import MyAgent, State


# Model for infection spread
class InfectionModel(Model):
    def __init__(self, population=10, width=10, height=10, ptrans=0.5,
                 death_rate=0.02, recovery_days=21,
                 recovery_sd=7):

        self.agents = population
        self.recovery_days = recovery_days
        self.recovery_sd = recovery_sd
        self.ptrans = ptrans
        self.death_rate = death_rate
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.dead_agents = []

        # Create agents
        for i in range(self.agents):
            new_agent = MyAgent(i, self)
            self.schedule.add(new_agent)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(new_agent, (x, y))

            # Make some agents infected at start
            infected = np.random.choice([0, 1], p=[0.98, 0.02])
            if infected == 1:
                new_agent.state = State.INFECTED
                new_agent.recovery_time = self.get_recovery_time()

        self.datacollector = DataCollector(
            agent_reporters={"State": "state"})

    def get_recovery_time(self):
        return int(self.random.normalvariate(self.recovery_days, self.recovery_sd))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
