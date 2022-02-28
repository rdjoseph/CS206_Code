import pyrosim.pyrosim as pyrosim
import pybullet as p
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    def __init__(self):
        self.robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

        print(self.sensors)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

        print(self.motors)
            
    def Sense(self, timestep):
        for sensorName, sensor in self.sensors.items():
            sensor.Get_Value(timestep)

    def Act(self, timestep):
        for motorName, motor in self.motors.items():
            motor.Set_Value(self.robot, timestep)

            
