from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
worldID = sys.argv [3]

simulation = SIMULATION(directOrGUI, solutionID, worldID)
simulation.Run()
simulation.Get_Fitness()
