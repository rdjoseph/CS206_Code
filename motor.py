import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = np.pi / 4
        self.frequency = 20
        self.phaseOffset = 0

        if self.jointName == "Torso_BackLeg":
            print(self.jointName, "is oscillating at frequency", 80)
            self.frequency = 80

        self.motorValues = [(self.amplitude * np.sin(self.frequency * x + self.phaseOffset)) for x in np.linspace(0, (2 * np.pi), 1000)]

    def Set_Value(self, robot, timestep):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot, jointName=self.jointName, controlMode=p.POSITION_CONTROL, targetPosition=self.motorValues[timestep], maxForce=25)

    def Save_Values(self):
        with open('data/motorValues.npy', 'wb') as f:
            np.save(f, self.motorValues)
