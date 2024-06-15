import math
import grid as g
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class Environment:
    def __init__(self, grid_h: int, grid_w: int):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.reset_grid()

    def reset_grid(self):
        self.obstacles = {}
        self.robot_path = {}

    def is_inside_grid(self, x, y):
        return -1 < x < self.grid_w and -1 < y < self.grid_h

    def set_start(self, start_x: int, start_y: int):
        if self.is_inside_grid(start_x, start_y):
            self.start_x, self.start_y = start_x, start_y
        else:
            raise ValueError("START CANNOT BE OUTSIDE GRID.")

    def set_end(self, end_x: int, end_y: int):
        if self.is_inside_grid(end_x, end_y):
            self.end_x, self.end_y = end_x, end_y
        else:
            raise ValueError("END CANNOT BE OUTSIDE GRID.")

    def set_obstacles(self, obstacles: dict):
        diagonal = int(math.sqrt(math.pow(self.grid_h, 2) + math.pow(self.grid_w, 2)))
        for obstacle_id in obstacles:
            self.obstacles[obstacle_id] = {
                'x': obstacles[obstacle_id]['x'],
                'y': obstacles[obstacle_id]['y'],
                'dx': obstacles[obstacle_id]['dx'],
                'dy': obstacles[obstacle_id]['dy'],
                'major_axis': obstacles[obstacle_id]['major_axis'],
                'minor_axis': obstacles[obstacle_id]['minor_axis'],
                'path': {timestep: {'x': obstacles[obstacle_id]['x'] + (timestep * obstacles[obstacle_id]['dx']),
                                    'y': obstacles[obstacle_id]['y'] + (timestep * obstacles[obstacle_id]['dy']),
                                    'dx': obstacles[obstacle_id]['dx'],
                                    'dy': obstacles[obstacle_id]['dy'],
                                    'speed': math.sqrt(math.pow(obstacles[obstacle_id]['dx'], 2) + math.pow(obstacles[obstacle_id]['dy'], 2)),
                                    } for timestep in range(diagonal)
                        },
                }

    def get_straight_path(self, start_x: int, start_y: int, end_x: int, end_y: int):
        path = {}
        if start_x == end_x:
            for timestep, y in enumerate(range(start_y, end_y + 1 if start_y < end_y else end_y - 1, 1 if start_y < end_y else -1)):
                path[timestep] = {'x': start_x, 'y': y, 'dx': 0, 'dy': 1 if start_y < end_y else -1, 'speed': 1.0}
        elif start_y == end_y:
            for timestep, x in enumerate(range(start_x, end_x + 1 if start_x < end_x else end_x - 1, 1 if start_x < end_x else -1)):
                path[timestep] = {'x': x, 'y': start_y, 'dx': 1 if start_x < end_x else -1, 'dy': 0, 'speed': 1.0}
        return path

    def set_global_path(self):
        self.robot_path = self.get_straight_path(self.start_x, self.start_y, self.end_x, self.end_y)

    def set_path(self, path):
        self.robot_path = path

    def plot_environment(self, robot_path=None, pause_time=1.0):
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.add_patch(plt.Rectangle((self.start_x, self.start_y), 1, 1, color='green'))
        ax.add_patch(plt.Rectangle((self.end_x, self.end_y), 1, 1, color='red'))
        for obstacle_id in self.obstacles:
            ax.add_patch(plt.Rectangle((self.obstacles[obstacle_id]['x'], self.obstacles[obstacle_id]['y']), 1, 1, color='black'))
            ax.annotate('', (self.obstacles[obstacle_id]['x'] + 0.5, self.obstacles[obstacle_id]['y'] + 0.5), (self.obstacles[obstacle_id]['x'] + 0.5 + self.obstacles[obstacle_id]['dx'], self.obstacles[obstacle_id]['y'] + 0.5 + self.obstacles[obstacle_id]['dy']), arrowprops={'color': 'purple', 'arrowstyle': '<-'})
            ax.plot([self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], [self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], label=f'OBSTACLE {obstacle_id} PATH')
            ax.scatter([self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], [self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], label=f'OBSTACLE {obstacle_id} PATH')
            for timestep in self.obstacles[obstacle_id]['path']:
                ax.text(self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.6, self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.4, f'SPEED={self.obstacles[obstacle_id]["path"][timestep]["speed"]}', horizontalalignment='center', verticalalignment='center', color='black')
        if robot_path is None:
            robot_path = self.robot_path
        ax.plot([robot_path[timestep]['x'] + 0.5 for timestep in robot_path], [robot_path[timestep]['y'] + 0.5 for timestep in robot_path], label=f'ROBOT PATH')
        ax.scatter([robot_path[timestep]['x'] + 0.5 for timestep in robot_path], [robot_path[timestep]['y'] + 0.5 for timestep in robot_path], label=f'ROBOT PATH')
        for timestep in robot_path:
            ax.text(robot_path[timestep]['x'] + 0.6, robot_path[timestep]['y'] + 0.4, f'SPEED={robot_path[timestep]["speed"]}', horizontalalignment='center', verticalalignment='center', color='black')
        ax.legend(loc='best')
        ax.set_xlim(0, self.grid_w)
        ax.set_ylim(0, self.grid_h)
        ax.set_xticks([i for i in range(self.grid_w + 1)])
        ax.set_yticks([i for i in range(self.grid_h + 1)])
        ax.tick_params(axis='both')
        # ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.grid(True, alpha=1)
        plt.show(block=False)
        plt.pause(pause_time)
        plt.close()

    def simulate(self, pause_time=1.0):
        for timestep in self.robot_path:
            fig, ax = plt.subplots(1, 1, figsize=(12, 12))
            ax.add_patch(plt.Rectangle((self.start_x, self.start_y), 1, 1, color='green'))
            ax.add_patch(plt.Rectangle((self.end_x, self.end_y), 1, 1, color='red'))
            ax.add_patch(plt.Rectangle((self.robot_path[timestep]['x'], self.robot_path[timestep]['y']), 1, 1, color='lime'))
            ax.annotate('', (self.robot_path[timestep]['x'] + 0.5, self.robot_path[timestep]['y'] + 0.5), (self.robot_path[timestep]['x'] + 0.5 + self.robot_path[timestep]['dx'], self.robot_path[timestep]['y'] + 0.5 + self.robot_path[timestep]['dy']), arrowprops={'color': 'purple', 'arrowstyle': '<-'})
            for obstacle_id in self.obstacles:
                ax.add_patch(plt.Rectangle((self.obstacles[obstacle_id]['path'][timestep]['x'], self.obstacles[obstacle_id]['path'][timestep]['y']), 1, 1, color='black'))
                ax.annotate('', (self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5, self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5), (self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5 + self.obstacles[obstacle_id]['path'][timestep]['dx'], self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5 + self.obstacles[obstacle_id]['path'][timestep]['dy']), arrowprops={'color': 'purple', 'arrowstyle': '<-'})
                ax.plot([self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], [self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], label=f'OBSTACLE {obstacle_id} PATH')
                ax.scatter([self.obstacles[obstacle_id]['path'][timestep]['x'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], [self.obstacles[obstacle_id]['path'][timestep]['y'] + 0.5 for timestep in self.obstacles[obstacle_id]['path']], label=f'OBSTACLE {obstacle_id} PATH')
            ax.plot([self.robot_path[timestep]['x'] + 0.5 for timestep in self.robot_path], [self.robot_path[timestep]['y'] + 0.5 for timestep in self.robot_path], label=f'ROBOT PATH')
            ax.scatter([self.robot_path[timestep]['x'] + 0.5 for timestep in self.robot_path], [self.robot_path[timestep]['y'] + 0.5 for timestep in self.robot_path], label=f'ROBOT PATH')
            ax.legend(loc='best')
            ax.set_xlim(0, self.grid_w)
            ax.set_ylim(0, self.grid_h)
            ax.set_xticks([i for i in range(self.grid_w + 1)])
            ax.set_yticks([i for i in range(self.grid_h + 1)])
            ax.tick_params(axis='both')
            # ax.set_aspect('equal')
            ax.invert_yaxis()
            ax.grid(True, alpha=1)
            plt.show(block=False)
            plt.pause(pause_time)
            plt.close()
