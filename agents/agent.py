from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv
from random import randint
import enum


class States(enum.IntEnum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    REMOVED = 2


class Person(Agent):
    def __init__(self, agent_id, model):
        super(Person, self).__init__(agent_id)

        self.age = randint(20, 40)
        self.state = States.SUSCEPTIBLE
        self.infection_time = 0