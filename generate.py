import pyrosim.pyrosim as pyrosim
# Pos read [x,y,z] according to source code
# Size read [length,width,height] according to online docs of urdf format

length = 1
width = 1 
height = 1

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")

    pyrosim.Send_Cube(name="Torso",pos=[1.5,0,1.5],size=[length,width,height])
    # BackLeg absolute position: [0.5,0,0.5]
    pyrosim.Send_Joint(name="Torso_BackLeg",parent="Torso",child="BackLeg", type="revolute", position =[1,0,1])
    pyrosim.Send_Cube(name="BackLeg",pos=[-0.5,0,-0.5],size=[length,width,height])

    # Note: Joints & Links are relative to their upstream joints/links. You might think, ah, so Torso_FrontLeg is relative to Torso_BackLeg. No, you fool. There is no upstream joint of Torso_FrontLeg because joint/link relationships are like a tree, ie (torso (joint "torso_backleg" backleg) (joint "torso_frontleg" frontleg)). So we define torso_frontleg as an absolute position, and frontleg is relative to that. 
    # Torso_FrontLeg joint absolute position [2,0,1]
    # FrontLeg absolute position [2.5,0,0.5]
    pyrosim.Send_Joint(name="Torso_FrontLeg",parent="Torso",child="FrontLeg", type="revolute", position =[2,0,1])
    pyrosim.Send_Cube(name="FrontLeg",pos=[0.5,0,-0.5],size=[length,width,height])
    
    pyrosim.End()
    
def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
    pyrosim.End()


def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box",pos=[5,5,0.5],size=[length,width,height])

    pyrosim.End()


def main():
    Create_World()
    Generate_Brain()
    Create_Robot()


main()
