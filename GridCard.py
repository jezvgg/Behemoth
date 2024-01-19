import flet as  ft
from settings.settings_class import Settings
from settings.settings_inputs import *
from vizualazing import createChart


class GridCard(ft.Container):

    settings = None
    political_settings = None
    people_settings = None
    life_settings = None
    page = None


    def __init__(self, page: ft.Page, *args, **kwargs):
        super().__init__(
            width=400,
            height=400,
            border=ft.border.all(2, "#1A202A"),
            border_radius=20,
            padding=20,
            *args, **kwargs)

        self.page = page

        self.political_settings = Settings(
            page=page,
            title="Политические предпочтения",
            content=ft.Container(
                content = ft.Column(
                    controls = p_checkers,
                    height=400
                )
            )
        )
        self.page.add(self.political_settings)

        self.people_settings = Settings(
            page=page,
            title="Главное в людях",
            content=ft.Container(
                content = ft.Column(
                    controls = pm_checkers,
                    height=400
                )
            )
        )
        self.page.add(self.people_settings)

        self.life_settings = Settings(
            page=page,
            title="Главное в жизни",
            content=ft.Container(
                content = ft.Column(
                    controls = lm_checkers,
                    height=400
                )
            )
        )
        self.page.add(self.life_settings)

        # Добавить удаление карточки
        self.settings = Settings(
            page=page,
            title = 'Настройки',
            content = ft.Container(
                content = ft.Column(
                    controls=[
                        dropdown_charts,
                        dropdown_sizes,
                        ft.Text('Настроить пересечения интересов:'),
                        ft.TextButton(text=self.political_settings.title, on_click=self.political_settings.fopen),
                        ft.TextButton(text=self.people_settings.title, on_click=self.people_settings.fopen),
                        ft.TextButton(text=self.life_settings.title, on_click=self.life_settings.fopen)
                    ]
                ), height=400, width=300
            )
        )
        self.page.add(self.settings)

        self.content = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.create_card, bgcolor="#11151C")


    def create_card(self, e: ft.ControlEvent):
        self.settings.fopen()

        while self.settings.open == True: continue

        self.content = ft.Stack(
            controls = [
                ft.Row([ft.Text(self.settings.content.content.controls[0].value, size=16)], top=11, left=30),
                createChart(self.page.analyze, self.settings.content.content.controls[0].value),
                ft.IconButton(
                    icon = ft.icons.SETTINGS,
                    icon_color = "#212D40",
                    icon_size = 30,
                    tooltip = "Settings",
                    on_click=self.create_card,
                    right = 0
                )
            ], expand=True
        )
        self.page.update()

