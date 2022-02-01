import pybullet as p
import pybullet_data
import time as t 

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotID = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

for i in range(10000):
    t.sleep(0.2)
    p.stepSimulation()

p.disconnect()
