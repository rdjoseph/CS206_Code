import numpy
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

        # Our initial solution is a 3 by 2 matrix of random floating point values
        self.weights = numpy.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Start_Simulation(self, directOrGUI):
        """ Launch asynchronous process to evaluate solution """
        self.Create_Robot()
        self.Create_World()
        self.Create_Brain()
        print("Evaluating solution ID " + str(self.myID))
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        """ Wait for fitness process to end, read its fitness from filesystem, store in self.fitness """
        fitnessFile = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFile):
            time.sleep(0.001)

        with open(fitnessFile, "r") as file:
            self.fitness = float(file.read())

        os.system("rm " + fitnessFile)
    
    def Mutate(self):
        r = random.randint(0, 2)
        c = random.randint(0, 1)
        self.weights[r, c] = random.random() * 2 - 1

    def Create_Robot(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[self.length,  self.width,  self.height])
        # BackLeg absolute position: [0.5, 0, 0.5]
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg",  type="revolute",  position=[1,  0,  1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[self.length,  self.width,  self.height])

        # Note: Joints & Links are relative to their upstream joints/links. You might think, ah, so Torso_FrontLeg is relative to Torso_BackLeg. No, you fool. There is no upstream joint of Torso_FrontLeg because joint/link relationships are like a tree, ie (torso (joint "torso_backleg" backleg) (joint "torso_frontleg" frontleg)). So we define torso_frontleg as an absolute position, and frontleg is relative to that.
        # Torso_FrontLeg joint absolute position [2,0,1]
        # FrontLeg absolute position [2.5,0,0.5]
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[2, 0, 1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[self.length, self.width, self.height])
        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[5, 5, 0.5],
                          size=[self.length, self.width, self.height])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        # Sensors
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        # Set up synapses with weights
        # As an aside, I am using literal lists over range() to prevent tripping on the [inclusive,exclusive) arguments and accidentally miscounting. It's uglier but less error prone for small ranges
        for currRow in range(numSensorNeurons):
            for currCol in range(numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currRow,
                                     targetNeuronName=(currCol + 3),
                                     weight=self.weights[currRow][currCol])

        pyrosim.End()
