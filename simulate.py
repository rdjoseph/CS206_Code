import pybullet as p
import pybullet_data
import time as t
import random 
import pyrosim.pyrosim as pyrosim
import numpy as np

pi = np.pi
BackLeg_amplitude = pi/2
BackLeg_frequency = 20
BackLeg_phaseOffset = pi/4

FrontLeg_amplitude = pi/4
FrontLeg_frequency = 20
FrontLeg_phaseOffset = 0

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotID)
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

targetAngles = np.linspace(0, (2 * pi), 10000)
FrontLeg_targetAngles = [(FrontLeg_amplitude * np.sin(FrontLeg_frequency * x + FrontLeg_phaseOffset)) for x in targetAngles]
BackLeg_targetAngles = [(BackLeg_amplitude * np.sin(BackLeg_frequency * x + BackLeg_phaseOffset)) for x in targetAngles]

# with open('data/FrontLegTargetData.npy', 'wb') as f:
#     np.save(f, FrontLeg_targetAngles)
#     
# with open('data/BackLegTargetData.npy', 'wb') as f:
#     np.save(f, BackLeg_targetAngles)
# 
# exit()

for i in range(10000):
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotID, jointName="Torso_BackLeg", controlMode=p.POSITION_CONTROL, targetPosition=BackLeg_targetAngles[i], maxForce=25)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotID, jointName="Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=FrontLeg_targetAngles[i], maxForce=25)
    t.sleep(0.01)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

# with open('data/backLegSensorValues.npy', 'wb') as f:
#   np.save(f, backLegSensorValues)
# with open('data/frontLegSensorValues.npy', 'wb') as f:
#    np.save(f, frontLegSensorValues)


p.disconnect()
