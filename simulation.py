import pyrosim.pyrosim as pyrosim
import pybullet as p
import pybullet_data
import time as t
import numpy as np
import constants as c
from robot import ROBOT
from world import WORLD


class SIMULATION:
    def __init__(self, directOrGUI, solutionID, worldID):
        self.solutionID = solutionID
        self.worldID = worldID
        self.directOrGUI = directOrGUI
        if directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD(worldID)
        # We write each neural net solution file out twice, ie solution42B.nndf
        # So we give the robot its corresponding worldID
        self.robot = ROBOT(solutionID, worldID)

    def Run(self):
        """ Run the simulation """
        for i in range(c.iterations):
            if self.directOrGUI == "GUI":
                t.sleep(c.timepause)
            p.stepSimulation()
            self.robot.Act(i)
            self.robot.Think()
            self.robot.Sense(i)

        # TODO REMOVE: This is a temporary hack because of how Josh's multiprocessing works
        # To get the footprint data out for our footprint graph
        if self.directOrGUI == "GUI":
            footsteps = np.array([self.robot.sensors['FrontLowerLeg'],
                                  self.robot.sensors['BackLowerLeg'],
                                  self.robot.sensors['LeftLowerLeg'],
                                  self.robot.sensors['RightLowerLeg']]
            np.save(f"footsteps{self.solutionID}{self.worldID}.npy", footsteps)

        if self.directOrGUI == "GUI":
            print("\nFinal neuron values of " + self.solutionID + " in world " + self.worldID)
            self.robot.nn.Print()

    def Get_Fitness(self):
        return self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()
