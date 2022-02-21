import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp
# with open('data/backLegSensorValues.npy','rb') as f:
#     backLegSensorValues = np.load(f)
# with open('data/frontLegSensorValues.npy','rb') as f:
#     frontLegSensorValues = np.load(f)
# pp.plot(backLegSensorValues,linewidth=2,label="backLegSensorValues")
# pp.plot(frontLegSensorValues,linewidth=2,label="frontLegSensorValues")

with open('data/FrontLegTargetData.npy', 'rb') as f:
    frontLeg = np.load(f)
with open('data/BackLegTargetData.npy', 'rb') as f:
    backLeg = np.load(f)

pp.plot(frontLeg, linewidth=2, label="Front Leg")
pp.plot(backLeg, linewidth=2, label="Back Leg")

pp.legend()

pp.show()  # not without dinner first, si
