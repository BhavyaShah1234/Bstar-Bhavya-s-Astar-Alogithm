import math

class Bstar:
    def __init__(self, occupancy_grid, obstacle_penalty):
        self.occupancy_grid = occupancy_grid
        self.obstacle_penalty = obstacle_penalty
        self.open_list = []
        self.closed_list = []

    def get_offsets_based_on_movement(self, movement, max_distance):
        move_offsets = []
        if movement == 'queen':
            for i in range(-1 * max_distance, max_distance + 1, 1):
                for j in range(-1 * max_distance, max_distance + 1, 1):
                    if i != 0 or j != 0:
                        move_offsets.append([i, j])
        elif movement == 'rook':
            for i in range(-1 * max_distance, max_distance + 1, 1):
                for j in range(-1 * max_distance, max_distance + 1, 1):
                    if (i == 0 and j != 0) or (i != 0 and j == 0):
                        move_offsets.append([i, j])
        return move_offsets

    def euclidian_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    def weighted_expansion(self, x, y, movement='queen', k_factor=0.5):
        for dx, dy in self.get_offsets_based_on_movement(movement, 1):
            index_x, index_y = x + dx, y + dy
            if self.occupancy_grid.is_inside_grid(index_x, index_y):
                if self.occupancy_grid.is_free_to_move(index_x, index_y):
                    if self.occupancy_grid[index_x, index_y] not in self.open_list and self.occupancy_grid[index_x, index_y] not in self.closed_list:
                        self.occupancy_grid[index_x, index_y]['k'] = self.occupancy_grid[x, y]['k'] + self.euclidian_distance(x, y, index_x, index_y)
                        self.open_list.append(self.occupancy_grid[index_x, index_y])
                    else:
                        new_k = self.occupancy_grid[x, y]['k'] + self.euclidian_distance(x, y, index_x, index_y)
                        if new_k <= self.occupancy_grid[index_x, index_y]['k']:
                            self.occupancy_grid[index_x, index_y]['k'] = new_k
                            self.open_list[self.open_list.index(self.occupancy_grid[index_x, index_y])]['k'] = self.occupancy_grid[index_x, index_y]['k']
                else:
                    self.occupancy_grid[index_x, index_y]['k'] = self.obstacle_penalty
            else:
                continue
        self.open_list = sorted(self.open_list, key=lambda a: (k_factor * a['k']) + ((1 - k_factor) * a['start_distance']))
        return self.open_list.pop(0)

    def find_path(self, movement='queen', max_speed=1, k_factor=0.5):
        x, y = self.occupancy_grid.end_x, self.occupancy_grid.end_y
        self.occupancy_grid[x, y]['k'] = 0
        self.open_list.append(self.occupancy_grid[x, y])
        while True:
            # self.occupancy_grid.plot_grid(2.0)
            if x == self.occupancy_grid.start_x and y == self.occupancy_grid.start_y:
                break
            else:
                top_node = self.weighted_expansion(x, y, movement, k_factor)
                self.closed_list.append(top_node)
                if len(self.open_list) > 0:
                    x, y = self.open_list[0]['x'], self.open_list[0]['y']
        # self.occupancy_grid.plot_grid(pause_time=10.0)
        path = {}
        timestep = 0
        x, y = self.occupancy_grid.start_x, self.occupancy_grid.start_y
        while True:
            path[timestep] = {'x': x, 'y': y, 'dx': 0, 'dy': 0, 'speed': 0.0}
            if x == self.occupancy_grid.end_x and y == self.occupancy_grid.end_y:
                break
            else:
                for speed in range(max_speed, 0, -1):
                    moves = [[x + dx, y + dy] for dx, dy in self.get_offsets_based_on_movement(movement, speed) if self.occupancy_grid.is_inside_grid(x + dx, y + dy) and self.occupancy_grid[x + dx, y + dy]['k'] is not None]
                    if speed > 1 and any([not self.occupancy_grid.is_free_to_move(index_x, index_y) for index_x, index_y in moves]):
                        continue
                    else:
                        moves = sorted(moves, key=lambda a: self.occupancy_grid[a[0], a[1]]['k'])
                        x, y = moves[0]
                        break
                timestep = timestep + 1
                path[timestep - 1]['dx'] = x - path[timestep - 1]['x']
                path[timestep - 1]['dy'] = y - path[timestep - 1]['y']
                path[timestep - 1]['speed'] = math.sqrt(math.pow(path[timestep - 1]['dx'], 2) + math.pow(path[timestep - 1]['dy'], 2))
        return path
