import flet as ft
import numpy as np
import pandas as pd
from math import prod
import flet.canvas as cv
from itertools import combinations


class VennChart(ft.UserControl):

    __graph_data : dict
    __circles: list[cv.Circle] = []
    __layers: list[cv.Canvas] = []

    width: int
    height: int 
    _collision: int
    padding: int

    colors = [ft.colors.RED, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.GREEN]

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

        degrees = np.linspace(0.01, 3.14*2, num=len(types) + 1)[:-1]

        center_x = width//2
        center_y = height//2
        radius = min(center_x, center_y)//2

        for degree, color in zip(degrees, self.colors):
            x = center_x + np.cos(degree)*(radius*self._collision)
            y = center_y + np.sin(degree)*(radius*self._collision)
            paint = ft.Paint(color=color, style=ft.PaintingStyle.FILL)
            self.__circles.append(cv.Circle(x,y,radius,paint=paint))
            self.__layers.append(cv.Canvas(expand=True, shapes=[self.__circles[-1]], opacity=0.6))


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