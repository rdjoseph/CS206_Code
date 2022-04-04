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

        # Our initial solution is a matrix of random floating point values
        self.weights = numpy.random.rand(numSensorNeurons, numMotorNeurons)
        self.weights = self.weights * 2 - 1  # Normalize

    def Set_ID(self, id):
        self.myID = id

    def Start_Simulation(self, directOrGUI):
        """ Launch asynchronous process to evaluate solution """
        self.Create_Robot()
        self.Create_World()
        self.Create_Brain("brain" + str(self.myID) + "A.nndf")
        self.Create_Brain("brain" + str(self.myID) + "B.nndf")
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " A 2&>1 &")
        os.system("python simulate.py " + directOrGUI + " " + str(self.myID) + " B 2&>1 &")

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


        # Note: Joints & Links are relative to their upstream joints/links. You might think, ah, so Torso_FrontLeg is relative to Torso_BackLeg. No, you fool. There is no upstream joint of Torso_FrontLeg because joint/link relationships are like a tree, ie (torso (joint "torso_backleg" backleg) (joint "torso_frontleg" frontleg)). So we define torso_frontleg as an absolute position, and frontleg is relative to that.
        # Torso_FrontLeg joint absolute position [2,0,1]
        # FrontLeg absolute position [2.5,0,0.5]
    def Create_Robot(self):
        """ Creates a quadraped robot, stored in body.urdf """
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[self.length,  self.width,  self.height])

        # Upper Legs 
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg",  type="revolute",  position=[0, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1.0, 0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1.0, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1.0, 0.2, 0.2])

        # Lower Legs
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pyrosim.End()

    def Create_World(self):
        """ Constructs two world files, WorldA.sdf & WorldB.sdf, each with a block placed (respectively) 5 blocks ahead/behind of [0,0,0] on the y axis """
        pyrosim.Start_SDF("worldA.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[0, 5, 0.5],
                          size=[self.length, self.width, self.height])

        pyrosim.End()
        
        pyrosim.Start_SDF("worldB.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[0, -5, 0.5],
                          size=[self.length, self.width, self.height])

        pyrosim.End()
        

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
