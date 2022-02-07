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

    
    # pyrosim.Send_Cube(name="Link0",pos=[0,0,0.5],size=[length,width,height])
    # pyrosim.Send_Cube(name="Link1",pos=[0.5,0,0.5],size=[length,width,height])
    # # Absolute pos of link2 (second leg): [2,0,0.5]
    # pyrosim.Send_Cube(name="Link2",pos=[0.5,0,-0.5],size=[length,width,height])
    # pyrosim.Send_Joint(name = "Link0_Link1", parent = "Link0",child = "Link1",type="revolute",position = [0.5,0,1])
    # Absolute joint pos: [1.5,0,1]
    # pyrosim.Send_Joint(name = "Link1_Link2", parent = "Link1",child = "Link2",type="revolute",position = [1,0,0])
    pyrosim.End() 

def Create_World(): 
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box",pos=[5,5,0.5],size=[length,width,height])

    pyrosim.End()


def main():
    Create_World()
    Create_Robot()

main()
