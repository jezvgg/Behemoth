import flet as ft
from Card import Card, NewCard

class MyGrid(ft.Container):
    size = (4,4)
    curr_row = 0
    curr_colmn = 0
    space = []
    cards = []
    
    def __init__(self, size: tuple[int, int], spacing: int):
        self.size = size
        super().__init__()
        self.content = ft.Column(
            controls=[ft.Row(spacing=spacing, expand=True) for _ in range(size[0])],
            expand=True
        )
        self.space = [[0]*size[0] for _ in size[1]]


    def append(self, elem: Card | NewCard):
        self.cards.append(elem)
        self.content.controls.controls.append(self.cards[-1])
        self.space[self.curr_row][self.curr_colmn] = len(self.cards)-1


    def __getitem__(self, key: int) -> Card | NewCard:
        return self.cards[key]


    def __setitem__(self, key: int, value: Card | NewCard):
        self.cards[key] = value