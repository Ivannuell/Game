class GridLayout:
    def __init__(self, start_pos, cols, spacing):
        self.start_x, self.start_y = start_pos
        self.cols = cols
        self.spacing = spacing

    def position(self, index, size):
        col = index % self.cols
        row = index // self.cols

        x = self.start_x + col * (size + self.spacing)
        y = self.start_y + row * (size + self.spacing)
        return x, y




class VBoxLayout:
    def __init__(self, start_pos, spacing):
        self.x, self.y = start_pos
        self.spacing = spacing
        self.current_y = self.y

    def next(self, height):
        pos = (self.x, self.current_y)
        self.current_y += height + self.spacing
        return pos
