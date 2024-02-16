import flet as ft
import flet.canvas as cv
from flet_core.canvas.shape import Shape


class VennCircle:
    x = 0
    y = 0
    radius = 0
    text = None
    fill_color = None
    stroke_color = None

    __inner_circle = None
    __outer_circle = None


    def __init__(self, x:int, y:int, radius:int, text: cv.Text = None,
                fill_color: ft.Paint = ft.Paint(color = "surface,0.5", style=ft.PaintingStyle.FILL),
                stroke_color: ft.Paint = ft.Paint(color=ft.colors.BLACK, style=ft.PaintingStyle.STROKE, stroke_width=3)):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.fill_color = fill_color
        self.stroke_color = stroke_color

        self.__inner_circle = cv.Circle(x=self.x, y=self.y, radius=self.radius, paint=self.fill_color)
        self.__outer_circle = cv.Circle(x=self.x, y=self.y, radius=self.radius, paint=self.stroke_color)


    @property
    def inner(self):
        return self.__inner_circle


    @property
    def outer(self):
        return self.__outer_circle
    