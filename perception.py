import grid as g

class Perception:
    def __init__(self, environment):
        self.environment = environment

    def get_obstacles(self, path=None):
        if path is None:
            path = self.environment.robot_path
        for timestep in path:
            self.obstacles = {}
            colliding_obstacles = {obstacle_id: {
                'x': self.environment.obstacles[obstacle_id]['path'][timestep]['x'],
                'y': self.environment.obstacles[obstacle_id]['path'][timestep]['y'],
                'dx': self.environment.obstacles[obstacle_id]['path'][timestep]['dx'],
                'dy': self.environment.obstacles[obstacle_id]['path'][timestep]['dy'],
                'major_axis': self.environment.obstacles[obstacle_id]['major_axis'],
                'minor_axis': self.environment.obstacles[obstacle_id]['minor_axis'],
                } for obstacle_id in self.environment.obstacles if self.environment.obstacles[obstacle_id]['path'][timestep]['x'] == path[timestep]['x'] and self.environment.obstacles[obstacle_id]['path'][timestep]['y'] == path[timestep]['y']
            }
            other_obstacles = {obstacle_id: {
                'x': self.environment.obstacles[obstacle_id]['path'][timestep]['x'],
                'y': self.environment.obstacles[obstacle_id]['path'][timestep]['y'],
                'dx': self.environment.obstacles[obstacle_id]['path'][timestep]['dx'],
                'dy': self.environment.obstacles[obstacle_id]['path'][timestep]['dy'],
                'major_axis': self.environment.obstacles[obstacle_id]['major_axis'],
                'minor_axis': self.environment.obstacles[obstacle_id]['minor_axis'],
                } for obstacle_id in self.environment.obstacles if obstacle_id not in colliding_obstacles
            }
            if len(colliding_obstacles) > 0:
                self.obstacles[timestep] = {'colliding': colliding_obstacles, 'other': other_obstacles}
                break

    def get_occupancy_grid(self):
        occupancy_grid = g.Grid(self.environment.grid_h, self.environment.grid_w)
        occupancy_grid.put_start(self.environment.start_x, self.environment.start_y)
        occupancy_grid.put_end(self.environment.end_x, self.environment.end_y)
        for timestep in self.obstacles:
            for obstacle_id in self.obstacles[timestep]['colliding']:
                obstacle_x = self.obstacles[timestep]['colliding'][obstacle_id]['x']
                obstacle_y = self.obstacles[timestep]['colliding'][obstacle_id]['y']
                obstacle_dx = self.obstacles[timestep]['colliding'][obstacle_id]['dx']
                obstacle_dy = self.obstacles[timestep]['colliding'][obstacle_id]['dy']
                major_axis = self.obstacles[timestep]['colliding'][obstacle_id]['major_axis']
                minor_axis = self.obstacles[timestep]['colliding'][obstacle_id]['minor_axis']
                occupancy_grid.put_obstacle(obstacle_id, obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, major_axis, minor_axis)
            for obstacle_id in self.obstacles[timestep]['other']:
                obstacle_x = self.obstacles[timestep]['other'][obstacle_id]['x']
                obstacle_y = self.obstacles[timestep]['other'][obstacle_id]['y']
                obstacle_dx = self.obstacles[timestep]['other'][obstacle_id]['dx']
                obstacle_dy = self.obstacles[timestep]['other'][obstacle_id]['dy']
                major_axis = self.obstacles[timestep]['other'][obstacle_id]['major_axis']
                minor_axis = self.obstacles[timestep]['other'][obstacle_id]['minor_axis']
                occupancy_grid.put_obstacle(obstacle_id, obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, major_axis, minor_axis)
        occupancy_grid.calculate_distances()
        return occupancy_grid
