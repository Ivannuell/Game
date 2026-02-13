

import pygame
from UI.Widgets.button import Button
from UI.Widgets.label import Label
from UI.Widgets.widget import Widget
from UI.styles import SHOP_STYLE
from components.data_compnents import Item, Item_Placeholder


class Shop_ItemSlot(Widget):
    def __init__(self, menu, pos, item: Item, size = (100, 100)):
        super().__init__(menu)
        pos_x, pos_y = pos
        width, height = size
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        if item is None:
            item = Item_Placeholder

        self.buy_button = Button(
                            menu,
                            pos=(pos_x+5, pos_y+height-25),
                            size=(width - 10, 20),
                            style=SHOP_STYLE,
                            text=item.price,
                            on_click=lambda: self.menu.command_manager.send("SPAWN", item.name)
                        )
        
        self._children.append(self.buy_button)

        self._children.append(Label(
            menu,
            pos = (pos_x+5, pos_y+height-40),
            size = (width - 10, 15),
            style=SHOP_STYLE,
            text= item.name
        ))

    def handle_self_event(self, event):
        return True

    def update_self(self, dt):
        pass
        
    def draw_self(self, screen: pygame.Surface):
        pygame.draw.rect(screen, 'white', self.rect)


