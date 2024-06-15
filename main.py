import bstar as b
import perception as p
import environment as e

GRID_H, GRID_W = 20, 20
START_X, START_Y = 10, 19
END_X, END_Y = 10, 0
OBSTACLES = {
    'a': {'x': 9, 'y': 3, 'dx': 0, 'dy': 0, 'major_axis': [-1, 1], 'minor_axis': [-1, 1]},
    'b': {'x': 1, 'y': 10, 'dx': 1, 'dy': 0, 'major_axis': [-1, 2], 'minor_axis': [-1, 1]},
    'c': {'x': 19, 'y': 19, 'dx': -1, 'dy': -1, 'major_axis': [-1, 2], 'minor_axis': [-1, 1]},
    }
OBSTACLE_PENALTY = 500
MOVEMENT = 'queen'
MAX_SPEED = 4
K_FACTOR = 0.5

environment = e.Environment(GRID_H, GRID_W)
watcher = p.Perception(environment)

environment.set_start(START_X, START_Y)
environment.set_end(END_X, END_Y)
environment.set_obstacles(OBSTACLES)
environment.set_global_path()
environment.plot_environment(pause_time=5.0)

watcher.get_obstacles()
while len(watcher.obstacles) > 0:
    occupancy_grid = watcher.get_occupancy_grid()
    occupancy_grid.plot_grid(pause_time=5.0)
    planner = b.Bstar(occupancy_grid, OBSTACLE_PENALTY)
    path = planner.find_path(MOVEMENT, MAX_SPEED, K_FACTOR)
    print(path)
    occupancy_grid.plot_grid(path, pause_time=10.0, text=False)
    watcher.get_obstacles(path)
environment.set_path(path)
environment.simulate(pause_time=2.0)
