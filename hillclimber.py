import solution
import copy 
from constants import numberOfGenerations


class HILL_CLIMBER():
    def __init__(self):
        self.parent = solution.SOLUTION()

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Print(self):
        print("Parent: ", self.parent.fitness, "; Child: ", self.child.fitness)

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if (self.parent.fitness > self.child.fitness):
            self.parent = self.child

    def Show_Best(self):
        self.parent.Evaluate("GUI")
