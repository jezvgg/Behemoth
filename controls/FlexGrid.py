import flet as ft
from controls.GridCard import GridCard


class FlexGrid:
    page: ft.Page = None
    card_width: int
    card_height: int

    fwidth: int
    fheight: int
    size: tuple

    grid: list
    content: ft.Stack

    __index: int
    __next_pos: tuple

    def __init__(self, page: ft.Page, card_width: int, card_height: int,
                fwidth: int = 0, fheight: int = 0, size = (), expand: bool = False,
                padding: int = 15, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = ft.Stack()

        self.page = page
        self.card_width = card_width
        self.card_height = card_height

        if expand:
            fwidth = page.window_width
            fheight = page.window_height

        if not(fwidth or fheight or size):
            raise Exception("FlexGrid need width and height or size for creation.")

        self.size = size

        if fwidth and fheight:
            self.fwidth = fwidth
            self.fheight = fheight
            self.size = (int(self.fwidth//self.card_width), int(self.fheight//self.card_height))

        self.grid = [[0]*self.size[0] for _ in range(self.size[1])]
        self.controls = []

        self.__index = 0
        self.page.add(self.content)
        self.append()


    def append(self, e=None):
        card = GridCard(self.page, self.card_width, self.card_height)

        pos_x = int(self.__index%self.size[0])+1
        pos_y = int(self.__index//self.size[0])+1
        pos = (pos_x, pos_y)

        card.content.on_click = self.append
        self.page.update()
        
        if not (pos[0] > self.size[0] or pos[1] > self.size[1]):
            self.add(card, pos)
        else:
            self.__index += 1

        if self.__index > 1:
            list(filter(lambda x: x.index == self.__index-1 , self.content.controls))[0].create_card(e)


    def delete(self, index: int, e):
        if e:
            self.content.controls[index-1].settings.close()
        self.content.controls.pop(index-1)

        for card in list(filter(lambda x: x.index > index, self.content.controls)):
            card.index -= 1
            pos_x = int(card.index%self.size[0])
            pos_y = int((card.index-1)/self.size[0])+1
            x = (pos_x-1)*self.card_width + (pos_x-1)*15
            y = (pos_y-1)*self.card_width + (pos_y-1)*15
            card.left = x
            card.top = y

        self.__index -= 1
        self.page.update()


    def add(self, value: GridCard, pos: tuple):
        self.__index += 1
        value.index = self.__index
        value.settings.content.actions.append(ft.TextButton("Delete", on_click=lambda x: self.delete(value.index, x)))
        print([pos[0]-1],[pos[1]-1])
        self.grid[pos[1]-1][pos[0]-1] = value.index

        x = (pos[0]-1)*self.card_width + (pos[0]-1)*15
        y = (pos[1]-1)*self.card_width + (pos[1]-1)*15

        value.left = x
        value.top = y
        self.content.controls.append(value)
        self.page.update()
