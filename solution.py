import numpy
import statistics as stat
import random
import os
import time
import pyrosim.pyrosim as pyrosim
from constants import numSensorNeurons, numMotorNeurons


class SOLUTION():
    def __init__(self, id):
        self.myID = id
        self.length = 1
        self.width = 1
        self.height = 1

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
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " A 2&>1")
        print("Displaying world B...")
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " B 2&>1")

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

        self.fitness = stat.mean([fitnessA, fitnessB])

        os.system("rm " + fitnessAFile)
        os.system("rm " + fitnessBFile)
    
    def Mutate(self):
        r = random.randint(0, 2)
        c = random.randint(0, 1)
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
        # As an aside, I am using literal lists over range() to prevent tripping on the [inclusive,exclusive) arguments and accidentally miscounting. It's uglier but less error prone for small ranges
        for currRow in range(numSensorNeurons): # 4
            for currCol in range(numMotorNeurons): # 3
                pyrosim.Send_Synapse(sourceNeuronName=currRow,
                                     targetNeuronName=(currCol + numSensorNeurons),
                                     weight=self.weights[currRow][currCol])

        pyrosim.End()
