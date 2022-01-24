import pybullet as p 
import time as t 

physicsClient = p.connect(p.GUI)

for i in range(1000):
    print("Counter: ", i)
    t.sleep(1)
    p.stepSimulation()

p.disconnect()
