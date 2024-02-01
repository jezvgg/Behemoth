import flet as  ft
from settings.settings_class import Settings
from settings.inputs import inputs
from vizualazing import createChart, createChoicesOfDataFrame


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
                    controls = inputs['p_checkers'],
                    height=400
                )
            )
        )

        self.people_settings = Settings(
            page=page,
            title="Главное в людях",
            content=ft.Container(
                content = ft.Column(
                    controls = inputs['pm_checkers'],
                    height=400
                )
            )
        )

        self.life_settings = Settings(
            page=page,
            title="Главное в жизни",
            content=ft.Container(
                content = ft.Column(
                    controls = inputs['lm_checkers'],
                    height=400
                )
            )
        )

        self.settings = Settings(
            page=page,
            title = 'Настройки',
            content = ft.Container(
                content = ft.Column(
                    controls=[
                        inputs['dropdown_charts'][0],
                        inputs['dropdown_sizes'][0],
                        ft.Text('Настроить пересечения интересов:'),
                        ft.TextButton(text=self.political_settings._title, on_click=self.political_settings.fopen),
                        ft.TextButton(text=self.people_settings._title, on_click=self.people_settings.fopen),
                        ft.TextButton(text=self.life_settings._title, on_click=self.life_settings.fopen)
                    ]
                ), height=400, width=300
            )
        )

        self.content = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.create_card, bgcolor="#11151C")


    # В визуализации нужно баги исправить
    def create_card(self, e: ft.ControlEvent):
        self.settings.fopen()

        while any([self.settings.content.open, 
                   self.life_settings.content.open, 
                   self.people_settings.content.open, 
                   self.political_settings.content.open]): continue

        self.content = ft.Stack(
            controls = [
                ft.Row([ft.Text(self.settings.content.content.content.controls[0].value, size=16)], top=11, left=30),
                createChart(createChoicesOfDataFrame(self.page.analyze, self.types), self.settings.content.content.content.controls[0].value),
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


    @property
    def types(self):
        '''
        Возращает значения чекбоксов для пересечения графиков.
        '''
        return {'political':[int(not check.value)*(i+1) for i,check in enumerate(self.political_settings.content.content.content.controls) if not check.value],
                'people_main':[int(not check.value)*(i+1) for i,check in enumerate(self.people_settings.content.content.content.controls) if not check.value],
                'life_main':[int(not check.value)*(i+1) for i,check in enumerate(self.life_settings.content.content.content.controls) if not check.value]}
                