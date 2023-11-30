import flet as ft
from Card import Card, NewCard


# Сделать двойную индексацию
# Не работает pop
class MyGrid(ft.Container):
    size = (4,4)
    curr_row = 0
    curr_elem = 0
    space = []
    cards = []
    
    def __init__(self, size: tuple[int, int], spacing: int, **kwargs):
        self.size = size
        super().__init__(**kwargs)
        self.content = ft.Column(
            controls=[ft.Row(spacing=spacing, height=400) for _ in range(size[0])],
            expand=True,
            scroll=ft.ScrollMode.ALWAYS
        )
        self.space = [[0]*size[0] for _ in range(size[1])]


    def append(self, elem: Card | NewCard):
        self.cards.append(elem)
        self.content.controls[self.curr_row].controls.append(self.cards[-1])
        self.space[self.curr_row][self.curr_elem] = len(self.cards)
        self.curr_row += (self.curr_elem+1)//self.size[0]
        self.curr_elem = (self.curr_elem+1)%self.size[0]
        print(self.space)


    def __getitem__(self, key: int) -> Card | NewCard:
        return self.cards[key]


    def __setitem__(self, key: int, value: Card | NewCard):
        self.cards[key] = value
        self.update()


    def pop(self, i: int):
        num = i + 1
        print(num)
        for i, row in enumerate(self.space):
            if num not in row: continue
            self.cards[num-1] = None
            print(i, row.index(num))
            self.__shrink(i, row.index(num))
        self.update()
        self.curr_elem-=1
        if self.curr_elem<0:
            self.curr_row -= 1
            self.curr_elem = self.size[0]-1
        print(self.space, self.cards)


    def __shrink(self, i, j):
        self.space[i] = self.space[i][:j]+self.space[i][j+1:] + [self.space[i+1][0]]
        for ind in range(i+1,len(self.space)-1):
            self.space[ind] = self.space[ind][1:] + [self.space[i+1][0]]
        self.space[-1] = self.space[-1][1:] + [0]


    def update(self):
        for i,row in enumerate(self.space):
            for j,elem in enumerate(row):
                if elem==0: continue
                if self.cards[elem-1] == None:
                    self.content.controls[i].controls.pop(elem-1)
                    break
                self.content.controls[i].controls[j] = self.cards[elem-1]