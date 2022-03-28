""" A parallel hill climber, using system parallelism """
import os
import solution
import copy
from constants import numberOfGenerations, populationSize


class PARALLEL_HILL_CLIMBER():
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
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
        print("")
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
        for k, v in self.parents.items():
            if self.parents[k].fitness > self.children[k].fitness:
                self.parents[k] = self.children[k]
        
    def Show_Best(self):
        bestSol = min(list(self.parents.values()), key = lambda x: x.fitness)
        bestSol.Start_Simulation("GUI")
