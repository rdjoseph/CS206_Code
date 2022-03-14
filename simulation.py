import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data
import time as t
import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        """ Run the simulation """
        for i in range(c.iterations):
            t.sleep(0.001)
            p.stepSimulation()
            self.robot.Act(i)
            self.robot.Think()
            self.robot.Sense(i)

        exit()

    def Get_Fitness(self):
        pass 

    def __del__(self):
        p.disconnect()
