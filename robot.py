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

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = motorJointRange * self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

    def Get_Fitness(self):
        """
        Calculates a robot's fitness, post-simulation, as it's position on the
        y axis of the world
        """
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]
        yPosition = basePosition[1]
        fitnessFile = "tmp" + str(self.myID) + str(self.worldID) + ".txt"
        with open(fitnessFile, "w") as file:
            file.write(str(yPosition))
 
        os.system("mv " + fitnessFile + " fitness" + str(self.myID) + str(self.worldID) + ".txt")
