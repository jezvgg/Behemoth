import flet as ft
import numpy as np
import pandas as pd
from math import prod
import flet.canvas as cv
from flet_core.canvas.shape import Shape
from itertools import combinations
from controls.VennCircle import VennCircle



class VennChart(ft.UserControl):

    __graph_data : dict
    __circles: list[cv.Circle]
    __layers: list[cv.Canvas]

    width: int
    height: int 
    _collision: int
    padding: int

    colors = [ft.colors.RED, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.GREEN]
    start = [0, 0, 0.01, 1.0472, 0.7854, 0.01]
    stroke_paint = ft.Paint(color=ft.colors.BLACK, style=ft.PaintingStyle.STROKE, stroke_width=3)

    def __init__(self, data: pd.DataFrame, 
                types: list, 
                width: int,
                height: int,
                collision:int = 0.3,
                padding: int = 15):

        super().__init__()
        self.width = width
        self.height = height
        self._collision = 1-collision
        self.padding = padding

        degrees = np.linspace(self.start[len(types)], 3.14*2 + self.start[len(types)], num=len(types) + 1)[:-1]

        center_x = width//2
        center_y = height//2
        radius = min(center_x, center_y)//2-16
        self.__filter_data(data, types)

        labels = []
        self.__layers = []
        self.__circles = []

        for degree, color, name in zip(degrees, self.colors, types):
            # Создаём круги
            x = center_x + np.cos(degree)*(radius*self._collision)
            y = center_y + np.sin(degree)*(radius*self._collision)
            paint = ft.Paint(color=color, style=ft.PaintingStyle.FILL)

            # Подпись к кругу
            text_x = x
            text_y = y + (1 if y > center_y else -1)*radius
            start_draw = ft.alignment.bottom_center if y < center_y else ft.alignment.top_center
            style = ft.TextStyle(size=16, color=ft.colors.WHITE)
            text = cv.Text(x=text_x, y=text_y, text=name, alignment=start_draw, style=style)

            self.__circles.append(VennCircle(x=x, y=y, radius=radius, text=text, fill_color=paint))
            self.__layers.append(cv.Canvas(expand=True, shapes=[self.__circles[-1].inner], opacity=0.65))
            labels += [self.__circles[-1].outer, self.__circles[-1].text]

            # Подписываем размер круга
            x = center_x + np.cos(degree)*(radius*(self._collision+0.25))
            y = center_y + np.sin(degree)*(radius*(self._collision+0.25))
            labels.append(cv.Text(x=x, y=y, text=self.__graph_data[name], style=style, alignment=ft.alignment.center))

        names = self.__combinations_data(types)
        for degree, name in zip(degrees, names[len(types):-1]):
            # Подписываем пересечения кругов
            x = center_x + np.cos(degree+((degrees[0]-degrees[1])/2))*(radius*(self._collision-0.2))
            y = center_y + np.sin(degree+((degrees[0]-degrees[1])/2))*(radius*(self._collision-0.2))
            name = '&'.join(name)
            labels.append(cv.Text(x=x, y=y, text=self.__graph_data[name], style=style, alignment=ft.alignment.center))

        labels.append(cv.Text(x=center_x, y=center_y, text=self.__graph_data['&'.join(names[-1])], style=style, alignment=ft.alignment.center))
        self.__layers.append(cv.Canvas(expand=True, shapes=labels))


    def build(self):
        return ft.Stack(controls = self.__layers,
                        width=self.width-self.padding,
                        height=self.height-self.padding,
                        right=-(self.padding//2))


    def __filter_data(self, data: pd.DataFrame, types: list):
        '''
        Делает пересеченние данных по нужным типам и возращает новые данные для графика.
        '''
        graph_data = {}
        for combo in self.__combinations_data(types):
            graph_data['&'.join(combo)] = sum(prod([data[element].apply(lambda x: int(x)>0) for element in combo]))
        self.__graph_data = graph_data


    def __combinations_data(self, types: list):
        '''
        Делает все возможные комбинации длиной больше 1-го по списку
        '''
        combos = []
        for i,_ in enumerate(types):
            for combo in combinations(types, i + 1):
                combos.append(list(map(str, combo)))
        return combos


    @property
    def collision(self):
        return self._collision


    @collision.setter
    def collision(self, value: int):
        self._collision = 1 - value