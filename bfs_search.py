from collections import deque

class BFSPathfinder:
    
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
    
    def find_path(self, start, target, obstacles=None):
        if obstacles is None:
            obstacles = set()
        
        if start == target:
            return []
        
        queue = deque([(start, [start])])
        visited = {start}
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        while queue:
            (x, y), path = queue.popleft()
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if self._is_valid_position(nx, ny, visited, obstacles):
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    
                    if (nx, ny) == target:
                        return new_path[1:]
                    
                    queue.append(((nx, ny), new_path))
        
        return []
    
    def _is_valid_position(self, x, y, visited, obstacles):
        return (
            0 <= x < self.grid_width and
            0 <= y < self.grid_height and
            (x, y) not in visited and
            (x, y) not in obstacles
        )
    
    def find_safe_direction(self, start, target, obstacles=None):
        path = self.find_path(start, target, obstacles)
        
        if not path:
            return (0, 0)
        
        next_pos = path[0]
        dx = next_pos[0] - start[0]
        dy = next_pos[1] - start[1]
        
        return (dx, dy)
