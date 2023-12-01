import flet as ft
from Card import Card, NewCard


# Сделать двойную индексацию
# Не работает pop
class MyGrid(ft.Container):
    size = (4,4)
    curr_row = 0
    curr_elem = 0
    spacing = 0
    space = []
    positions = []
    lenght = 0
    
    def __init__(self, size: tuple[int, int], spacing: int, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.spacing = spacing

        self.content = ft.Stack(width=size[0]*400+(size[0]+1)*self.spacing,
        height=size[1]*400+(size[1]+1)*self.spacing)
        self.space = [[0]*size[0] for _ in range(size[1])]


    def append(self, elem: Card | NewCard):
        elem.left = self.curr_elem*400 + abs(self.curr_elem+1)*self.spacing
        elem.top = self.curr_row*400 + abs(self.curr_row+1)*self.spacing
        self.content.controls.append(elem)

        self.space[self.curr_row][self.curr_elem] = self.lenght+1

        self.curr_row += (self.curr_elem+1)//self.size[0]
        self.curr_elem = (self.curr_elem+1)%self.size[0]

        self.lenght += 1


    def __getitem__(self, key: int) -> Card | NewCard:
        return self.content.controls[key]


    def __setitem__(self, key: int, value: Card | NewCard):
        value.left = self[key].left
        value.top = self[key].top
        self.content.controls[key] = value


    def __len__(self):
        return self.lenght


    def pop(self, i):
        top = self.content.controls[i].top
        left = self.content.controls[i].left
        self.content.controls[i] = ft.Container(disabled=True, width=0, height=0, left=10, top=10)
        for j in range(i+1, len(self.content.controls)):
            ntop = self.content.controls[j].top
            nleft = self.content.controls[j].left
            self.content.controls[j].top = top
            self.content.controls[j].left = left
            top, left = ntop, nleft
        if self.curr_elem-1<0:
            self.curr_elem = self.size[0]-1
            self.curr_row -= 1
        else: self.curr_elem -= 1
