class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0  # radians
        self.target = None
        self.scale = 1
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        self.zoom_step = 1.1
