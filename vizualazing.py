import pandas as pd
from math import prod
from itertools import combinations
import flet as ft


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


def DataFrameConvertBool(df):
    '''
    Делает булевыми значения
    '''
    for columns in df.columns[10:]:
        df[columns] = df[columns].apply(lambda x: int(x)>0)
    return df


def getSeriesfromList(df, columns):  # Возращает Series в списке по списку колонок (нужно для prod)
    result = []
    for column in columns:
        result.append(df[column])
    return result


def getCombinatiosOfList(rawList):  # Делает все возможные комбинации длиной больше 1-го по списку
    combos = []
    for i in range(len(rawList)):
        for combo in combinations(rawList, i + 1):
            combos.append(list(map(str, combo)))
    return combos


def createDictionaryOfVenna(df, columns):  # Делает словарь который отправляют клиенту для графика Венна
    dfVenna = DataFrameConvertBool(df[columns].copy())
    list = []
    for column in getCombinatiosOfList(columns):
        dict = {}
        dfVenna["+".join(column)] = prod(getSeriesfromList(df, column))  # Делает новую колонку путём перемножения старых
        dict['sets'] = column
        dict['size'] = dfVenna["+".join(column)].tolist().count(True)
        list.append(dict)
    Venna = {'interest': list}
    return Venna


def createBarChart(df, type) -> ft.BarChart:  # Делает словарь который отправляют клиенту для столбчатого графика(ов)

    def hover(e: ft.BarChartEvent):
        for group_index, group in enumerate(barchart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                if e.group_index == group_index and e.rod_index == rod_index:
                    rod.color = "#D66853"
                else:
                    rod.color = "#3366CC"
        barchart.update()

    barchart = ft.BarChart(tooltip_bgcolor="#11151C", 
    max_y=max(df[type].value_counts().tolist()[1:])+max(df[type].value_counts().tolist()[1:])//4,
    on_chart_event=hover
    )

    axis = dict(df[type].value_counts())
    if 0 in axis.keys():
        del axis[0]
    AxisX = [tips[type][name-1] for name in axis.keys()]
    AxisY = list(axis.values())
    for i, value in enumerate(zip(AxisX,AxisY)):
        barchart.bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=value[1],
                        width=35,
                        color="#3366CC",
                        tooltip=f'{value[0]} \n{value[1]}',
                        border_radius=5
                    )
                ]
            )
        )
    return barchart


def createChoicesOfDataFrame(df, choice: dict[str, list[int]]) -> pd.DataFrame:  # Оставляет в датафреме только нужные строки
    '''
    Переделать
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
    print(createChoicesOfDataFrame(data, {'political':[1,2,3,4,5,6,6]}))