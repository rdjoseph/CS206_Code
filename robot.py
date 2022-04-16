import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import pybullet as p
from sensor import SENSOR
from motor import MOTOR
from constants import motorJointRange


class ROBOT:
    def __init__(self, solutionID, worldID):
        self.myID = solutionID
        self.worldID = worldID
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + worldID + ".nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("rm brain" + str(solutionID) + worldID + ".nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, timestep):
        for sensorName, sensor in self.sensors.items():
            sensor.Get_Value(timestep)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = motorJointRange * self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

    def Get_Fitness(self):
        """ Calculates a robot's fitness, post-simulation, as its absolute y coordinate """
        stateOfLinkZero = p.getLinkState(self.robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = abs(positionOfLinkZero[1])  # positionOfLinkZero is a tuple (x,y,z)
        fitnessFile = "tmp" + str(self.myID) + ".txt"
        with open(fitnessFile, "w") as file:
            file.write(str(xCoordinateOfLinkZero))
        os.system("mv " + fitnessFile + " fitness" + str(self.myID) + str(self.worldID) + ".txt")
