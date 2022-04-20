import parallelHillclimber

phc = parallelHillclimber.PARALLEL_HILL_CLIMBER()
try:
    phc.Evolve()
    phc.Show_Best()
except KeyboardInterrupt:
    print("Interrupted! Showing best so far: ")
    phc.Show_Best()
