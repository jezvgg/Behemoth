import flet as ft
from pandas import DataFrame


class BarChart(ft.UserControl):
    chart: ft.BarChart
    x = None
    y = None

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


    def __init__(self, data: DataFrame, name: str, use_axis=bool):
        super().__init__()
        axis = dict(data[name].value_counts())
        if 0 in axis.keys():
            del axis[0]
        self.x = [self.__tips[name][index-1] for index in axis.keys()]
        self.y = list(axis.values())

        max_y = max(data[name].value_counts().tolist()[1:])+max(data[name].value_counts().tolist()[1:])//4

        self.chart = ft.BarChart(tooltip_bgcolor="#11151C", 
            max_y=max_y,
            on_chart_event=self.hover
            )

        if use_axis: self.__add_axis(max_y)

        self.__create_chart()


    def build(self):
        return self.chart


    def hover(self, e: ft.BarChartEvent):
        for group_index, group in enumerate(self.chart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                if e.group_index == group_index and e.rod_index == rod_index:
                    rod.color = "#D66853"
                else:
                    rod.color = "#3366CC"
        self.chart.update()


    def __add_axis(self, max_y):
        name_size = int((500/len(self.x))//10)
        self.chart.left_axis = ft.ChartAxis(labels=[ft.ChartAxisLabel(value=i*5, label=ft.Text(f"{i*5}")) for i in range(max_y//5)])
        self.chart.bottom_axis = ft.ChartAxis()
        self.chart.bottom_axis.labels = [ft.ChartAxisLabel(value=i, label=ft.Text(name[:name_size], size=10)) for i,name in enumerate(self.x)]
        self.chart.horizontal_grid_lines=ft.ChartGridLines(
            color="#1A202A", width=1, dash_pattern=[3, 3]
        )


    def __create_chart(self):
        for i, value in enumerate(zip(self.x,self.y)):
            self.chart.bar_groups.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=value[1],
                            width=(280)//len(self.x),
                            color="#3366CC",
                            tooltip=f'{value[0]} \n{value[1]}',
                            border_radius=5
                        )
                    ]
                )
            )