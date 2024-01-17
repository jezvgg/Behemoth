import flet as  ft
from settings import *
from vizualazing import createChart


class GridCard(ft.Container):

    width = 400
    height = 400
    padding = 20
    border = ft.border.all(2, "#1A202A")
    border_radius=20
    settings = None
    political_settings = None
    people_settings = None
    life_settings = None
    contains = []

    def __init__(self):
        self.content = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_card, bgcolor="#11151C")
        
        self.political_settings = Settings(
            title=ft.Text("Политические предпочтения"),
            content=ft.Container(
                content = ft.Column(
                    controls = p_checkers,
                    height=400
                )
            )
        )

        self.people_settings = Settings(
            title=ft.Text("Главное в людях"),
            content=ft.Container(
                content = ft.Column(
                    controls = pm_checkers,
                    height=400
                )
            )
        )

        self.life_settings = Settings(
            title=ft.Text("Главное в жизни"),
            content=ft.Container(
                content = ft.Column(
                    controls = lm_checkers,
                    height=400
                )
            )
        )

        # Добавить удаление карточки
        self.settings = Settings(
            title = ft.Text('Настройки'),
            content = ft.Container(
                content = ft.Column(
                    controls=[
                        dropdown_charts,
                        dropdown_sizes,
                        ft.Text('Настроить пересечения интересов:'),
                        ft.TextButton(text=self.political_settings.title, on_click=self.political_settings.open()),
                        ft.TextButton(text=self.people_settings.title, on_click=self.people_settings.open()),
                        ft.TextButton(text=self.life_settings.title, on_click=self.life_settings.open())
                    ]
                ), height=400, width=300
            )
        )

        self.contains = [self.settings, self.people_settings, self.political_settings, self.life_settings]


    def create_card(self):
        self.settings.open()

        self.content = ft.Stack(
            controls=[
                ft.Row([ft.Text(self.settings.content.content.controls[0].value, size=16)], top=11, left=30),
                createChart(self.settings.content.content.controls[0].value),
                ft.IconButton(
                    icon = ft.icons.SETTINGS,
                    icon_color = "#212D40",
                    icon_size = 30,
                    tooltip = "Settings",
                    on_click=self.settings.open(),
                    right = 0
                )
            ]
        )

