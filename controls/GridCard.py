import flet as  ft
from settings.settings_class import Settings
from settings.inputs import inputs
from controls.Charts import BarChart, VennChart, PieChart


class GridCard(ft.Container):

    settings = None
    political_settings = None
    people_settings = None
    life_settings = None
    page = None
    interests: list = []


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
        self.settings.content.content.content.controls[0].on_change = self.on_change_plot

        self.content = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.create_card, bgcolor="#11151C")


    def create_card(self, e: ft.ControlEvent):
        self.settings.fopen()

        while any([self.settings.content.open, 
                   self.life_settings.content.open, 
                   self.people_settings.content.open, 
                   self.political_settings.content.open]): continue

        key = self.settings.content.content.content.controls[0].value
        name = list(filter(lambda x: x.key == key, self.settings.content.content.content.controls[0].options))[0].text

        self.content = ft.Stack(
            controls = [
                ft.Row([ft.Text(name, size=16)], top=11, left=30),
                self.__create_chart(df=self.__filter_data(self.page.analyze, self.types), 
                            type=key, 
                            types=self.interests),
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

    
    def on_change_plot(self, e):
        self.settings.content.content.content.controls = self.settings.content.content.content.controls[:6]
        match self.settings.content.content.content.controls[0].value:
            case 'interests':
                self.interests = []
                self.settings.content.content.content.controls += [
                                inputs['dropdown_interests'][0],
                                ft.ListView(controls=[], height=60)]
                self.settings.content.content.content.controls[-2].options = [ft.dropdown.Option(opt) for opt in self.page.analyze.columns[10:]]
                self.settings.content.content.content.controls[-2].on_change = self.add_interest
        self.page.update()


    def add_interest(self, e):
        self.interests.append(self.settings.content.content.content.controls[-2].value)
        self.settings.content.content.content.controls[-1].controls.append(
            ft.Text(self.settings.content.content.content.controls[-2].value))
        self.page.update()


    def __filter_data(self, df, choice: dict[str, list[int]]):
        '''
        Оставляет в датафреме только нужные строки, переделал
        '''
        filter = []
        for key in choice.keys():
            for value in choice[key]:
                filter.append(f"(df['{key}']!={value})")
        if filter:
            return df[eval("&".join(filter))]
        return df


    def __create_chart(self, df, type : str, types:list = None, *args, **kwargs):
        if type.endswith('Bar'):
            return BarChart(df, type[:-3], *args, **kwargs)
        elif type.endswith('Pie'):
            return PieChart(df, type[:-3], *args, **kwargs)
        elif type == 'interests':
            return VennChart(df, types=types, width=400, height=400, *args, **kwargs)