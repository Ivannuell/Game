

class UIManager:
    def __init__(self):
        self.menus = {}
        self._menu_stack = []

    def register(self, name, menu):
        self.menus[name] = menu

    def show(self, name, exclusive=True):
        if exclusive:
            for menu in self.menus.values():
                menu.hide()

        menu = self.menus[name]
        menu.show()         

        if name not in self._menu_stack:
            self._menu_stack.append(name)

    def hide(self, name):
        self.menus[name].hide()
        if name in self._menu_stack:
            self._menu_stack.remove(name)

    def toggle(self, name):
        if self.menus[name].visible:
            self.hide(name)
        else:
            self.show(name)
    
    def handle_event(self, event):
        if self._menu_stack:
            top = self.menus[self._menu_stack[-1]]
            top.handle_event(event)

    def update(self, dt):
        for m in self.menus.values():
            m.update(dt)

    def draw(self, screen):
        for m in self.menus.values():
            m.draw(screen)
            # screen.display_surface.blit(m.surface, m.pos)
