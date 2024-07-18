class Node:
    def __init__(self, x, y, k=None, start=None, start_distance=0.0, robot=None, end=None, end_distance=0.0, obstacle=None, repulsion_factor=0.0):
        self.x = x
        self.y = y
        self.k = k
        self.start = start
        self.start_distance = start_distance
        self.robot = robot
        self.end = end
        self.end_distance = end_distance
        self.obstacle = obstacle
        self.repulsion_factor = repulsion_factor

    def __getitem__(self, key):
        if key == 'x':
            return self.x
        elif key == 'y':
            return self.y
        elif key == 'k':
            return self.k
        elif key == 'start':
            return self.start
        elif key == 'start_distance':
            return self.start_distance
        elif key == 'robot':
            return self.robot
        elif key == 'end':
            return self.end
        elif key == 'end_distance':
            return self.end_distance
        elif key == 'obstacle':
            return self.obstacle
        elif key == 'repulsion_factor':
            return self.repulsion_factor

    def __setitem__(self, key, value):
        if key == 'x':
            self.x = value
        elif key == 'y':
            self.y = value
        elif key == 'k':
            self.k = value
        elif key == 'start':
            self.start = value
        elif key == 'start_distance':
            self.start_distance = value
        elif key == 'robot':
            self.robot = value
        elif key == 'end':
            self.end = value
        elif key == 'end_distance':
            self.end_distance = value
        elif key == 'obstacle':
            self.obstacle = value
        elif key == 'repulsion_factor':
            self.repulsion_factor = value
