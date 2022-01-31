import pyrosim.pyrosim as pyrosim

length = 1
width = 1 
height = 1

x = 5 
y = 5 
z = 0.5

# Pos read [x,y,z] according to source code
# Size read [length,width,height] according to online docs of urdf format 

pyrosim.Start_SDF("box.sdf")
l = length
w = width
h = height 

for i in range(5): # Col, sets x 
    for j in range(5): # Row, sets y 
        for k in range(10): # Tower, set z 
            pyrosim.Send_Cube(name="Box",pos=[x-i,y-j,z+k],size=[l,w,h])
            l *= 0.9
            w *= 0.9
            h *= 0.9
        l = length
        w = width
        h = height 


pyrosim.End()
