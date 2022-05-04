import numpy
import statistics as stat
import random
import os
import time
import sys
import pyrosim.pyrosim as pyrosim
from constants import numSensorNeurons, numMotorNeurons, numHiddenNeurons


class SOLUTION():
    def __init__(self, id):
        self.myID = id
        # Our initial solution is a matrix of random floating point values
        # self.weights = numpy.random.rand(numSensorNeurons, numMotorNeurons)
        # self.weights = self.weights * 2 - 1  # Normalize
        self.final_position = []
        self.sensors_to_hidden = numpy.random.rand(numHiddenNeurons, numSensorNeurons) * 2 - 1
        self.hidden_to_motors = numpy.random.rand(numHiddenNeurons, numMotorNeurons) * 2 - 1

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
            vals = file.read().split(",")
            A_touched_block = bool(int(vals[0]))
            A_x_position = float(vals[1])
            A_y_position = float(vals[2])

        with open(fitnessBFile, "r") as file:
            vals = file.read().split(",")
            B_touched_block = bool(int(vals[0]))
            B_x_position = float(vals[1])
            B_y_position = float(vals[2])

        dA = -1 * (A_y_position - 2.5)  # Diff btwn robo & block in World A, only rewarding negative movement
        dB = B_y_position + 2.5         # Diff btwn robo & block in World B, only rewarding postive movement

        # self.fitness = (dA + dB) / max(1, (A_touches + B_touches))

        if A_touched_block and B_touched_block:
            self.fitness = 2 + dA + dB
        elif A_touched_block:
            self.fitness = 1 + dA + (dB / 100)
        elif B_touched_block:
            self.fitness = 1 + dB + (dA / 100)
        else:
            self.fitness = (dA + dB) / 100

        self.final_position = [(A_x_position, A_y_position),
                               (B_x_position, B_y_position)]


        # print(f"{self.myID} aggr fit: {self.fitness}; touch A? {A_touched_block}; touch B? {B_touched_block}")
        os.system("rm " + fitnessAFile)
        os.system("rm " + fitnessBFile)

    def Mutate(self):
        # random.randint(a,b) is inclusive of b, unlike most Python things
        # We'll mutate only one synapse weight at once
        sth_or_htm = random.randint(0, 1)
        if sth_or_htm: # Pick one of the sensor-to-hidden-neuron weights to modify 
            r = random.randint(0, numHiddenNeurons - 1)
            c = random.randint(0, numSensorNeurons - 1)
            self.sensors_to_hidden[r, c] = random.random() * 2 - 1
        else:          # Pick one of the hidden-to-motor-neuron weights
            r = random.randint(0, numHiddenNeurons - 1)
            c = random.randint(0, numMotorNeurons - 1)
            self.hidden_to_motors[r, c] = random.random() * 2 - 1

    def Create_Brain(self, filename):
        """ Creates a neural network, stored in filename """
        pyrosim.Start_NeuralNetwork(filename)
        # Sensors
        links = ["Torso", "BackLeg", "FrontLeg", "LeftLeg", "RightLeg", "FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
        joints = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "FrontLeg_FrontLowerLeg", "BackLeg_BackLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]
        
        for idx, link in enumerate(links):
            pyrosim.Send_Sensor_Neuron(name=idx, linkName=link)

        for idx in range(numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=(idx + numSensorNeurons))
            
        for idx, joint in enumerate(joints):
            pyrosim.Send_Motor_Neuron(name=(idx + numHiddenNeurons + numSensorNeurons),
                                      jointName=joint)

        # Wire synapses from sensors to the hidden layer
        for sidx in range(numSensorNeurons):
            for hidx in range(numHiddenNeurons):
                # Wire from sensor neuron to hidden neuron 
                pyrosim.Send_Synapse(sourceNeuronName=sidx,
                                     targetNeuronName=(hidx + numSensorNeurons),
                                     weight=self.sensors_to_hidden[hidx][sidx])

        for hidx in range(numHiddenNeurons):
            for midx in range(numMotorNeurons):
                # Wire from hidden neuron to motor neuron 
                pyrosim.Send_Synapse(sourceNeuronName=(hidx + numSensorNeurons),
                                     targetNeuronName=(midx + numHiddenNeurons + numSensorNeurons),
                                     weight=self.hidden_to_motors[hidx][midx])

        pyrosim.End()
