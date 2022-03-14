import pyrosim.pyrosim as pyrosim
import numpy as np


class SENSOR:
    def __init__(self, name):
        self.linkName = name
        self.values = np.zeros(1000)

    def Get_Value(self, timestep):
        self.values[timestep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        with open('data/sensorValues.npy', 'wb') as f:
            np.save(f, self.values)
