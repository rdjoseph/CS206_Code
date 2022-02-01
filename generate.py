import pyrosim.pyrosim as pyrosim
# Pos read [x,y,z] according to source code
# Size read [length,width,height] according to online docs of urdf format

length = 1
width = 1 
height = 1

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Link0",pos=[0,0,0.5],size=[length,width,height])
    pyrosim.Send_Cube(name="Link1",pos=[0.5,0,0.5],size=[length,width,height])
    # Absolute pos of link2 (second leg): [2,0,0.5]
    pyrosim.Send_Cube(name="Link2",pos=[0.5,0,-0.5],size=[length,width,height])
    pyrosim.Send_Joint(name = "Link0_Link1", parent = "Link0",child = "Link1",type="revolute",position = [0.5,0,1])
    # Absolute joint pos: [1.5,0,1]
    pyrosim.Send_Joint(name = "Link1_Link2", parent = "Link1",child = "Link2",type="revolute",position = [1,0,0])
    pyrosim.End() 

def Create_World(): 
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box",pos=[5,5,0.5],size=[length,width,height])

    pyrosim.End()


def main():
    Create_World()
    Create_Robot()

main()
