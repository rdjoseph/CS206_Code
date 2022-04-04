import pybullet as p


class WORLD:
    def __init__(self, worldID):
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world" + worldID + ".sdf")
