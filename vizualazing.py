import pandas as pd
from time import perf_counter
from math import prod
from itertools import combinations

typesTitles = {'political': 'Политические предпочтения', 'people_main': 'Главное в людях',
               'life_main': 'Главное в жизни', 'sub': 'Главные интересы по подпискам',
               'alcohol': 'Отношение к алкоголю', 'smoking': 'Отношение к курению'}
tips = {'political': ["p - коммунистические", "p - социалистические", "p - умеренные", "p - либеральные",
                      "p - консервативные", "p - монархические", "p - ультраконсервативные", "p - индифферентные",
                      "p - либертарианские"],
        'people_main': [
            "m - ум и креативность",
            "m - доброта и честность",
            "m - красота и здоровье",
            "m - власть и богатство",
            "m - смелость и упорство",
            "m - юмор и жизнелюбие"],
        'life_main': [
            "l - семья и дети",
            "l - карьера и деньги",
            "l - развлечения и отдых",
            "l - наука и исследования",
            "l - совершенствование мира",
            "l - саморазвитие",
            "l - красота и искусство",
            "l - слава и влияние"],
        'sex': ["s - муж", "s - жен"]}


def cleanDataFrame(df):  # Очищает датафрем от лишних колонок (подписок) вроде 28 августа встреча или Этот метриал запрещён
    dropedColumns = []
    for columns in df.columns.tolist():
        if columns[0].isdigit() or columns[0:4] == 'Этот':
            dropedColumns.append(columns)
    df = df.drop(columns=dropedColumns)
    return df


def isBool(input):  # Возращает True если больше 0 и False иначе
    if int(input) > 0:
        return True
    return False


def DataFrameConvertBool(df):  # Делает значения у колонок подписок булевыми
    for columns in df.columns.tolist()[10:]:
        df[columns] = df[columns].apply(isBool)
    return df


def getSeriesfromList(df, columns):  # Возращает Series в списке по списку колонок (нужно для prod)
    result = []
    for i in range(len(columns)):
        result.append(df[columns[i]])
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


def createDictionaryOfBarChart(df, types):  # Делает словарь который отправляют клиенту для столбчатого графика(ов)
    BarCharts = []
    for i in range(len(types)):
        barchart = {}
        barchart['id'] = i
        barchart['title'] = typesTitles[types[i]]
        barchart['x'] = [tips[types[i]][type-1] for type in df[types[i]].unique()[1:]]
        barchart['y'] = df[types[i]].value_counts().tolist()[1:]
        barchart['xAxis'] = 'Предпочтения'
        barchart['yAxis'] = 'Кол-во людей (не в процентах)'
        BarCharts.append(barchart)
    return {'barcharts': BarCharts}


# {'choice':{'political':[types]}}
def createChoicesOfDataFrame(df, vibor):  # Оставляет в датафреме только нужные строки
    choice = vibor['choice']
    filter = df.head(0).copy()
    for key in choice.keys():
        for j in range(len(choice[key])):
            filter = filter.append(filter[filter[key] == choice[key][j]], ignore_index=True)
    return filter


def analyze(): # Создаёт датафрейм из CSV
    startTime = perf_counter()
    filename = 'content.csv'
    raw_df = pd.read_csv(filename)
    pd.set_option('display.max.columns', None)
    df = raw_df.fillna(0)
    df = cleanDataFrame(df)
    print('Done for', perf_counter() - startTime)
    return df
