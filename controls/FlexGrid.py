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


    def add(self, value: GridCard, pos: tuple):
        self.__index += 1
        value.index = self.__index
        self.grid[pos[0]-1][pos[1]-1] = value.index

        x = (pos[1]-1)*self.card_width + (pos[1]-1)*15
        y = (pos[0]-1)*self.card_width + (pos[0]-1)*15

        value.left = x
        value.top = y
        self.content.controls.append(value)
        self.page.update()
