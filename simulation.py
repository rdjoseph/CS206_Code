import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data
import time as t
import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        if directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def Run(self):
        """ Run the simulation """
        for i in range(c.iterations):
            if self.directOrGUI == "GUI":
                t.sleep(c.timepause)
            p.stepSimulation()
            self.robot.Act(i)
            self.robot.Think()
            self.robot.Sense(i)

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
