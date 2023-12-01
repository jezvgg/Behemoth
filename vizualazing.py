import pandas as pd
from math import prod
from itertools import combinations
import flet as ft
import matplotlib_venn as svenn
from venn._venn import *
from venn._constants import *
from functools import partial
import matplotlib.pyplot as plt
import matplotlib
from flet.matplotlib_chart import MatplotlibChart
from time import sleep

matplotlib.use("svg")

typesTitles = {'political': 'Политические предпочтения', 'people_main': 'Главное в людях',
               'life_main': 'Главное в жизни', 'sub': 'Главные интересы по подпискам',
               'alcohol': 'Отношение к алкоголю', 'smoking': 'Отношение к курению'}
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


def createVennChartSmall(df, types: list, *args, **kwargs):
    df = df.copy()

    # ----- Collect data for venn -----
    result = {}
    for combo in getCombinatiosOfList(types):
        result['&'.join(combo)] = sum(prod([df[element].apply(lambda x: int(x)>0) for element in combo]))

    plt.rcParams.update({"text.color": "white",
    'font.size':20,
    'font.weight':550})

    # ----- Create PLT venn -----
    fig, ax = plt.subplots()

    match len(types):
        case 2:
            svenn.venn2(subsets=list(result.values()), set_labels=types)
        case 3:
            svenn.venn3(subsets=list(result.values()), set_labels=types)
        case _:
            raise Exception("types invalid!")

    return MatplotlibChart(figure=fig, transparent=True, expand=True)


def draw_venn(*, petal_labels, dataset_labels, hint_hidden, colors, figsize, fontsize, legend_loc, ax):
    """Draw true Venn diagram, annotate petals and dataset labels"""
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if 2 <= n_sets < 6:
        draw_shape = draw_ellipse
    elif n_sets == 6:
        draw_shape = draw_triangle
    else:
        raise ValueError("Number of sets must be between 2 and 6")
    ax = init_axes(ax, figsize)
    shape_params = zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors
    )
    for coords, dims, angle, color in shape_params:
        draw_shape(ax, *coords, *dims, angle, color)
    for logic, petal_label in petal_labels.items():
        # some petals could have been modified manually:
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            draw_text(ax, x, y, petal_label, fontsize=fontsize, color='white')
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
    return ax


def createVennChartMedium(df, types: list, *args, **kwargs):
    df = df.copy()

    # ----- Collect data for venn -----
    result = {}
    for label in types:
        result[label] = set(df[df[label].apply(lambda x: int(x)>0)==True].index)
    

    # ----- Settings plt -----
    fig, ax = plt.subplots(figsize=(7,7))
    plt.figure(1,1)

    plt.rcParams.update({"text.color": "black",
    'font.size':16,
    'font.weight':400})


    # ----- Create venn chart -----
    venn = partial(venn_dispatch, func=draw_venn, hint_hidden=False)
    venn(result, ax=ax)

    return MatplotlibChart(figure=fig, transparent=True, expand=True)


def createChart(df, type, types: None, *args, **kwargs):
    match type:
        case 'political' | 'people_main' | "life_main":
            return createBarChart(df, type, *args, **kwargs)
        case 'politicalPie' | 'people_mainPie' | "life_mainPie" | "sexPie":
            return createPieChart(df, type[:-3], *args, **kwargs)
        case 'interests':
            if len(types)<4:
                return createVennChartSmall(df, types)
            else:
                return createVennChartMedium(df, types)

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

if __name__ == "__main__":
    data = analyze()
    createVennChartMedium(data, ['Юмор', 'Футбол','Культура и искусство'])