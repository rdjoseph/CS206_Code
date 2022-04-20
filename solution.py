import numpy
import statistics as stat
import random
import os
import time
import sys
import pyrosim.pyrosim as pyrosim
from constants import numSensorNeurons, numMotorNeurons


class SOLUTION():
    def __init__(self, id):
        self.myID = id
        
        # Our initial solution is a matrix of random floating point values
        self.weights = numpy.random.rand(numSensorNeurons, numMotorNeurons)
        self.weights = self.weights * 2 - 1  # Normalize

    def Set_ID(self, id):
        self.myID = id

    def Start_Simulation(self, directOrGUI):
        """ Launch asynchronous process to evaluate solution """
        self.Create_Brain("brain" + str(self.myID) + "A.nndf")
        self.Create_Brain("brain" + str(self.myID) + "B.nndf")
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " A 2&>1 &")
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " B 2&>1 &")

    def Display_Best(self):
        self.Create_Brain("brain" + str(self.myID) + "A.nndf")
        self.Create_Brain("brain" + str(self.myID) + "B.nndf")
        print("Displaying world A...")
        os.system("python simulate.py GUI " + str(self.myID) + " A")
        time.sleep(1)
        
        print("Displaying world B...")
        os.system("python simulate.py GUI " + str(self.myID) + " B")

    def Wait_For_Simulation_To_End(self):
        """ Wait for fitness process to end, read its fitness from filesystem, store in self.fitness """
        fitnessAFile = "fitness" + str(self.myID) + "A.txt"
        fitnessBFile = "fitness" + str(self.myID) + "B.txt"
        while (not os.path.exists(fitnessAFile)) or (not os.path.exists(fitnessBFile)):
            time.sleep(0.001)

        with open(fitnessAFile, "r") as file:
            fitnessA = float(file.read())

        with open(fitnessBFile, "r") as file:
            fitnessB = float(file.read())

        # We want to reward negative movement in World A, and positive movement in World B 
        self.fitness = (-1 * fitnessA) + fitnessB

        # Tried this to penalize large differences between results, ie robot just stops after hitting obstacle in
        # one world. Did not yield great results
        # self.fitness = (-1 * fitnessA) + fitnessB / max(abs(abs(fitnessA) - abs(fitnessB)), 1)


        # self.fitness = stat.mean([(-1 * fitnessA), fitnessB])
        print("ID: " + str(self.myID) + " aggregate fitness: " + str(self.fitness))

        os.system("rm " + fitnessAFile)
        os.system("rm " + fitnessBFile)

    def Mutate(self):
        r = random.randint(0, numSensorNeurons)
        c = random.randint(0, numMotorNeurons)
        self.weights[r, c] = random.random() * 2 - 1

    def Create_Brain(self, filename):
        """ Creates a neural network, stored in filename """ 
        pyrosim.Start_NeuralNetwork(filename)
        # Sensors
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLowerLeg")
        
        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=9, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=12, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=13, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightLeg_RightLowerLeg")
        
        # Set up synapses with weights
        for currRow in range(numSensorNeurons):
            for currCol in range(numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currRow,
                                     targetNeuronName=(currCol + numSensorNeurons),
                                     weight=self.weights[currRow][currCol])

        pyrosim.End()
