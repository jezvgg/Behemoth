import pandas as pd
from math import prod, cos, sin
from itertools import combinations
import flet as ft
import flet.canvas as cv
from controls.VennChart import VennChart
import math



tips = {'political': ["коммунистические", "социалистические", "умеренные", "либеральные",
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


def getCombinatiosOfList(rawList):  # Делает все возможные комбинации длиной больше 1-го по списку
    combos = []
    for i in range(len(rawList)):
        for combo in combinations(rawList, i + 1):
            combos.append(list(map(str, combo)))
    return combos


def createBarChart(df, type, size:int = 1, use_axis: bool = True, **kwargs) -> ft.BarChart:  # Делает словарь который отправляют клиенту для столбчатого графика(ов)

    # ----- Функция срабатывающая при наведении -----
    def hover(e: ft.BarChartEvent):
        for group_index, group in enumerate(barchart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                if e.group_index == group_index and e.rod_index == rod_index:
                    rod.color = "#D66853"
                else:
                    rod.color = "#3366CC"
        barchart.update()


    # ----- Создание данных графика -----
    axis = dict(df[type].value_counts())
    if 0 in axis.keys():
        del axis[0]
    AxisX = [tips[type][name-1] for name in axis.keys()]
    AxisY = list(axis.values())


    # ----- Объявление графика и основные настройки -----
    max_y = max(df[type].value_counts().tolist()[1:])+max(df[type].value_counts().tolist()[1:])//4
    barchart = ft.BarChart(tooltip_bgcolor="#11151C", 
    max_y=max_y,
    on_chart_event=hover
    )


    # ----- Создание осей -----
    if use_axis:
        name_size = int((500/len(AxisX))//10)
        barchart.left_axis = ft.ChartAxis(labels=[ft.ChartAxisLabel(value=i*5, label=ft.Text(f"{i*5}")) for i in range(max_y//5)])
        barchart.bottom_axis = ft.ChartAxis()
        barchart.bottom_axis.labels = [ft.ChartAxisLabel(value=i, label=ft.Text(name[:name_size], size=10)) for i,name in enumerate(AxisX)]
        barchart.horizontal_grid_lines=ft.ChartGridLines(
            color="#1A202A", width=1, dash_pattern=[3, 3]
        )


    # ----- Создание графика -----
    for i, value in enumerate(zip(AxisX,AxisY)):
        barchart.bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=value[1],
                        width=(size*280)//len(AxisX),
                        color="#3366CC",
                        tooltip=f'{value[0]} \n{value[1]}',
                        border_radius=5
                    )
                ]
            )
        )
    return barchart


def createPieChart(df, type, space: bool = True, **kwargs) -> ft.PieChart:

    # ----- Стили для Hover -----
    normal_radius = 65
    hover_radius = 70
    normal_title_style = ft.TextStyle(
        size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=19,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    colors = [ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PURPLE, ft.colors.GREEN, ft.colors.RED, ft.colors.PINK, ft.colors.PURPLE, ft.colors.DEEP_PURPLE, ft.colors.INDIGO]


    # ----- hover -----
    def hover(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()


    # ----- Data -----
    axis = dict(df[type].value_counts())
    if 0 in axis.keys():
        del axis[0]
    AxisX = [tips[type][name-1] for name in axis.keys()]
    AxisY = [value/(sum(axis.values())/100) for value in axis.values()]


    # ----- Create chart -----
    chart = ft.PieChart(
        sections=[ft.PieChartSection(value[1], title=f"{value[0]}\n{int(value[1])}" if value[1]>10 else "", color=colors[i], 
        radius=normal_radius, title_style=normal_title_style) for i,value in enumerate(zip(AxisX, AxisY))],
        sections_space=1,
        on_chart_event=hover)


    # ----- Add space -----
    if space:
        chart.center_space_radius=40

    return chart
    

def createChart(df:pd.DataFrame, type : str, types:list = None, *args, **kwargs):
    print(type)
    if type.endswith('Bar'):
        return createBarChart(df, type[:-3], *args, **kwargs)
    elif type.endswith('Pie'):
        return createPieChart(df, type[:-3], *args, **kwargs)
    elif type == 'interests':
        chart = VennChart(df, types=types, width=400, height=400, *args, **kwargs)
        return chart

def createChoicesOfDataFrame(df, choice: dict[str, list[int]]) -> pd.DataFrame:
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


def analyze(): # Создаёт датафрейм из CSV
    filename = 'content.csv'
    raw_df = pd.read_csv(filename)
    pd.set_option('display.max.columns', None)
    df = raw_df.fillna(0)
    return df