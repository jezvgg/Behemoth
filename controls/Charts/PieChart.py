import flet as ft
from pandas import DataFrame


class PieChart(ft.UserControl):
    chart: ft.PieChart
    x: int
    y: int

    __normal_radius = 105
    __hover_radius = 110
    __normal_title_style = ft.TextStyle(
        size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )
    __hover_title_style = ft.TextStyle(
        size=19,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )

    __colors = [ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PURPLE, ft.colors.GREEN, ft.colors.RED, ft.colors.PINK, ft.colors.PURPLE, ft.colors.DEEP_PURPLE, ft.colors.INDIGO]

    __tips = {'political': ["коммунистические", "социалистические", "умеренные", "либеральные",
                      "консервативные", "монархические", "ультраконсервативные", "индифферентные",
                      "либертарианские"],
        'people_main': [
            "ум и креативность",
            "доброта и честность",
            "красота и здоровье",
            "власть и богатство",
            "смелость и упорство",
            "юмор и жизнелюбие"],
        'life_main': [
            "семья и дети",
            "карьера и деньги",
            "развлечения и отдых",
            "наука и исследования",
            "совершенствование мира",
            "саморазвитие",
            "красота и искусство",
            "слава и влияние"],
        'sex': ["s - муж", "s - жен"]}


    def __init__(self, data: DataFrame, name: str, space: bool = False):
        super().__init__()
        axis = dict(data[name].value_counts())
        if 0 in axis.keys():
            del axis[0]
        self.x = [self.__tips[name][index-1] for index in axis.keys()]
        self.y = [value/(sum(axis.values())/100) for value in axis.values()]
        self.__create_chart()

        self.chart.center_space_radius = 0
        self.__hover_radius = 110
        self.__normal_radius = 105
        if space:
            self.__normal_radius -= 40
            self.__hover_radius -= 40
            self.chart.center_space_radius=40


    def build(self):
        return self.chart


    def hover(self, e: ft.PieChartEvent):
        for idx, section in enumerate(self.chart.sections):
            if idx == e.section_index:
                section.radius = self.__hover_radius
                section.title_style = self.__hover_title_style
            else:
                section.radius = self.__normal_radius
                section.title_style = self.__normal_title_style
        self.chart.update()


    def __create_chart(self):
        self.chart = ft.PieChart(
            sections=[ft.PieChartSection(value[1], title=f"{value[0]}\n{int(value[1])}" if value[1]>10 else "", color=self.__colors[i%9], 
            radius=self.__normal_radius, title_style=self.__normal_title_style) for i,value in enumerate(zip(self.x, self.y))],
            sections_space=1,
            on_chart_event=self.hover)