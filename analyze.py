import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp 

with open('data/backLegSensorValues.npy','rb') as f:
    backLegSensorValues = np.load(f)
with open('data/frontLegSensorValues.npy','rb') as f:
    frontLegSensorValues = np.load(f)


pp.plot(backLegSensorValues,linewidth=2,label="backLegSensorValues")
pp.plot(frontLegSensorValues,linewidth=2,label="frontLegSensorValues")

pp.legend()

pp.show() # not without dinner first, sir  


