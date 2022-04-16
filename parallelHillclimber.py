""" A parallel hill climber, using system parallelism """
import os
import solution
import copy
from constants import numberOfGenerations, populationSize


class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        # Because the worlds & robot body are only constructed once, I moved them to PHC. No sense writing the same files to disk 100 times per evolutionary session
        self.Create_Robot()
        self.Create_World()
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Print(self):
        print("Generational Fitness: ")
        for k, v in self.parents.items():
            print(str(k) + ") ", end='')
            print("Parent: " + str(self.parents[k].fitness), end='')
            print("; Child: " + str(self.children[k].fitness))
        print("")

    def Spawn(self):
        self.children = {}
        for k, v in self.parents.items():
            self.children[k] = copy.deepcopy(v)
            self.children[k].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Evaluate(self, solutions):
        for sol in solutions.values():
            sol.Start_Simulation("DIRECT")

        for sol in solutions.values():
            sol.Wait_For_Simulation_To_End()

    def Select(self):
        """ Compares children to parents, replacing when children have larger fitness values """
        for k, v in self.parents.items():
            if self.parents[k].fitness < self.children[k].fitness:
                self.parents[k] = self.children[k]

    def Show_Best(self):
        bestSol = min(list(self.parents.values()), key=lambda x: x.fitness)
        print("\n Best solution: ")
        print(bestSol.weights)
        bestSol.Display_Best()
        bestSol.Start_Simulation("GUI")

    # Note: Joints & Links are relative to their upstream joints/links. You might think, ah, so Torso_FrontLeg is relative to Torso_BackLeg. No, you fool. There is no upstream joint of Torso_FrontLeg because joint/link relationships are like a tree, ie (torso (joint "torso_backleg" backleg) (joint "torso_frontleg" frontleg)). So we define torso_frontleg as an absolute position, and frontleg is relative to that.
    # Torso_FrontLeg joint absolute position [2,0,1]
    # FrontLeg absolute position [2.5,0,0.5]
    def Create_Robot(self):
        """ Creates a quadraped robot, stored in body.urdf """
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[self.length,  self.width,  self.height])

        # Upper Legs 
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg",  type="revolute",  position=[0, -0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])

        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, 0.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1.0, 0.2])

        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1.0, 0.2, 0.2])

        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1.0, 0.2, 0.2])

        # Lower Legs
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        
        pyrosim.End()

    def Create_World(self):
        """ Constructs two world files, WorldA.sdf & WorldB.sdf, each with a block placed (respectively) 5 blocks ahead/behind of [0,0,0] on the y axis """
        pyrosim.Start_SDF("worldA.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[0, 5, 0.5],
                          size=[self.length, self.width, self.height])

        pyrosim.End()
        
        pyrosim.Start_SDF("worldB.sdf")
        pyrosim.Send_Cube(name="Box",
                          pos=[0, -5, 0.5],
                          size=[self.length, self.width, self.height])

        pyrosim.End()
