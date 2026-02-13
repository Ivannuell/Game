from UI.Menus.menu import Menu
from UI.Widgets.shop_itemSlot import Shop_ItemSlot
from UI.Widgets.window import Window
from UI.displayLayouts import GridLayout
from components.data_compnents import Item_Placeholder



class Shop_Menu(Menu):
    def __init__(self, ui_manager, command_manager, pos=(100, 200), size=(280, 400)):
        super().__init__(pos, size)
        self.window = Window(self)
        self.width, self.height = size
        self.command_manager = command_manager


    def on_show(self):
        self.item_slots = []

        if self.context is None:
            self.context = [Item_Placeholder]
        
        layout = GridLayout((20,20), 2, 20)
        for i, item in enumerate(self.context):
            self.item_slots.append(
                Shop_ItemSlot(
                    self, 
                    pos = layout.position(i, (100, 100)),
                    item = item,
                )
            )


        self.widgets = [
            self.window,
            *self.item_slots
        ]

        
        
