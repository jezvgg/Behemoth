import pandas as pd
import flet as ft
from controls.VennChart import VennChart
from controls.BarChart import BarChart



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
        return BarChart(df, type[:-3], *args, **kwargs)
    elif type.endswith('Pie'):
        return createPieChart(df, type[:-3], *args, **kwargs)
    elif type == 'interests':
        chart = VennChart(df, types=types, width=400, height=400, *args, **kwargs)
        return chart


def analyze(): # Создаёт датафрейм из CSV
    filename = 'content.csv'
    raw_df = pd.read_csv(filename)
    pd.set_option('display.max.columns', None)
    df = raw_df.fillna(0)
    return df