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
    event = False

    _default_x = 0
    _default_y = 0
    _default_radius = 0
    _default_text = None
    _default_fill_color = None
    _default_stroke_color = None
    _default_opacity = None

    __inner_circle = None
    __outer_circle = None


    def __init__(self, x:int, y:int, radius:int, text: cv.Text = None, opacity: float = 0.7,
                fill_color: ft.Paint = ft.Paint(color = "surface,0.5", style=ft.PaintingStyle.FILL),
                stroke_color: ft.Paint = ft.Paint(color=ft.colors.BLACK, style=ft.PaintingStyle.STROKE, stroke_width=3)):
        self._default_x = x
        self._default_y = y
        self._default_radius = radius
        self._default_text = text
        self._default_fill_color = fill_color
        self._default_stroke_color = stroke_color
        self._default_opacity = opacity
        self.event = False
        self.to_default()

        self.__inner_circle = cv.Canvas(expand=True, shapes=[cv.Circle(x=self.x, y=self.y, radius=self.radius, paint=self.fill_color)], opacity=self.opacity)
        self.__outer_circle = cv.Circle(x=self.x, y=self.y, radius=self.radius, paint=self.stroke_color)


    def to_default(self):
        self.x = self._default_x
        self.y = self._default_y
        self.radius = self._default_radius
        self.text = self._default_text
        self.text.style = ft.TextStyle(size=16, color=ft.colors.WHITE)
        self.fill_color = self._default_fill_color
        self.stroke_color = self._default_stroke_color
        self.opacity = self._default_opacity


    @property
    def opacity(self):
        return self._default_opacity


    @opacity.setter
    def opacity(self, value: float):
        if self.inner: self.inner.opacity = value


    def update(self):
        self.inner.update()
        self.outer.update()
        self.text.update()


    @property
    def inner(self):
        return self.__inner_circle


    @property
    def outer(self):
        return self.__outer_circle
    