import math
import node as n
import matplotlib.pyplot as plt

class Grid:
    def __init__(self, grid_h: int, grid_w: int):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.reset_grid()

    def reset_grid(self):
        self.obstacles = {}
        self.grid = [[n.Node(i, j) for i in range(self.grid_w)] for j in range(self.grid_h)]

    def __getitem__(self, index: list):
        index_x, index_y = index
        return self.grid[index_y][index_x]

    def __setitem__(self, index, value):
        index_x, index_y = index
        self.grid[index_y][index_x] = value

    def is_inside_grid(self, x, y):
        return -1 < x < self.grid_w and -1 < y < self.grid_h

    def is_free_to_move(self, x, y):
        return not self.grid[y][x]['obstacle'] and self.grid[y][x]['repulsion_factor'] == 0.0

    def put_start(self, start_x, start_y):
        if self.is_inside_grid(start_x, start_y):
            self.start_x, self.start_y = start_x, start_y
            self.grid[start_y][start_x]['start'] = True
        else:
            raise ValueError("START CANNOT BE OUTSIDE GRID.")

    def put_end(self, end_x, end_y):
        if self.is_inside_grid(end_x, end_y):
            self.end_x, self.end_y = end_x, end_y
            self.grid[end_y][end_x]['end'] = True
        else:
            raise ValueError("END CANNOT BE OUTSIDE GRID.")

    def put_oval_repulsion(self, obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, major_axis, minor_axis):
        for major in range(major_axis[0], major_axis[1] + 1, 1):
            center_x, center_y = obstacle_x + major * obstacle_dx, obstacle_y + major * obstacle_dy
            for i in range(minor_axis[0], minor_axis[1] + 1, 1):
                for j in range(minor_axis[0], minor_axis[1] + 1, 1):
                    index_x, index_y = center_x + i, center_y + j
                    if self.is_inside_grid(index_x, index_y):
                        self.grid[index_y][index_x]['repulsion_factor'] = self.grid[index_y][index_x]['repulsion_factor'] + 1.0

    def put_obstacle(self, obstacle_id, obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, major_axis, minor_axis):
        if self.is_inside_grid(obstacle_x, obstacle_y):
            self.grid[obstacle_y][obstacle_x]['obstacle'] = True
            self.grid[obstacle_y][obstacle_x]['obstacle_movement'] = [obstacle_dx, obstacle_dy]
            self.obstacles[obstacle_id] = {'x': obstacle_x, 'y': obstacle_y, 'dx': obstacle_dx, 'dy': obstacle_dy, 'major_axis': major_axis, 'minor_axis': minor_axis}
        self.put_oval_repulsion(obstacle_x, obstacle_y, obstacle_dx, obstacle_dy, major_axis, minor_axis)

    def euclidian_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    def calculate_distances(self):
        for i in range(self.grid_h):
            for j in range(self.grid_w):
                self.grid[i][j]['start_distance'] = self.euclidian_distance(self.start_x, self.start_y, j, i)
                self.grid[i][j]['end_distance'] = self.euclidian_distance(self.end_x, self.end_y, j, i)

    def plot_grid(self, robot_path=None, pause_time=1.0, text=True):
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        for i in range(self.grid_h):
            for j in range(self.grid_w):
                if self.grid[i][j]['start']:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='green'))
                elif self.grid[i][j]['end']:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='red'))
                elif self.grid[i][j]['obstacle']:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
                elif self.grid[i][j]['repulsion_factor'] > 0.0:
                    ax.add_patch(plt.Rectangle((j, i), 1, 1, color='grey'))
                if text:
                    ax.text(j + 0.5, i + 0.3, f'{round(self.grid[i][j]["k"], 1) if self.grid[i][j]["k"] is not None else ""}', horizontalalignment='center', verticalalignment='center', color='black')
                    ax.text(j + 0.5, i + 0.8, f'{round(self.grid[i][j]["repulsion_factor"], 1) if self.grid[i][j]["repulsion_factor"] > 0.0 else ""}', horizontalalignment='center', verticalalignment='center', color='black')
        if robot_path is not None:
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
