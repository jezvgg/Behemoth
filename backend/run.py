from flask import Flask, request, jsonify
from backend.parsing import parsing
from backend.vizualazing import analyze, createDictionaryOfBarChart, createChoicesOfDataFrame, createDictionaryOfVenna


app = Flask(__name__)
df = analyze().copy()


def convertToList(rawList, deley=","): # Проверяет наличие параметра
    if type(rawList)!=list:
        rawList = list(map(int, rawList.split(deley)))
    return rawList


@app.route("/")
def hello_world(): # Тестовая функция
    return "<p>Hello, world</p>"


@app.route("/Behemoth", methods=['GET']) # Парсирает группу ВК по указанному токену и групп_ид
def pars():
    content = request.json['content']
    token = content['token']
    group_id = content['group_id']
    parsing(token, group_id)
    return "Done", 200


@app.route("/subscriptions", methods=['GET']) # Возращает возможные множества графика Венна
def returnSubscriptions():
    return jsonify({"subscriptions":df.columns.tolist()[10:]})


@app.route("/barchart", methods=['GET']) # Возращает JSON файл для построения столбчатого графика
def returnBarChart():
    types = request.args.get('type').split(",")
    print(types)
    filters = {'choice':{'political':convertToList(request.args.get('political', default=[1,2,3,4,5,6,7,8,9])),
                         'people_main':convertToList(request.args.get('people_main', default=[1,2,3,4,5,6])),
                         'life_main':convertToList(request.args.get('life_main', default=[1,2,3,4,5,6,7,8])),
                         'smoking':convertToList(request.args.get('smoking', default=[1,2,3,4,5])),
                         'alcohol':convertToList(request.args.get('alcohol', default=[1,2,3,4,5]))}}
    createDictionaryOfBarChart(createChoicesOfDataFrame(df, filters), types)
    return jsonify(createDictionaryOfBarChart(createChoicesOfDataFrame(df, filters), types))


@app.route("/venn", methods=['GET']) # Возращает JSON файл для построения столбчатого графика
def returnVennChart():
    subs = request.args.get('subscriptions', default=df.columns.tolist()[10:20])
    subs = list(map(str, subs.split("."))) if type(subs) != list else subs
    filters = {
        'choice': {'political': convertToList(request.args.get('political', default=[1, 2, 3, 4, 5, 6, 7, 8, 9])),
                   'people_main': convertToList(request.args.get('people_main', default=[1, 2, 3, 4, 5, 6])),
                   'life_main': convertToList(request.args.get('life_main', default=[1, 2, 3, 4, 5, 6, 7, 8])),
                   'smoking': convertToList(request.args.get('smoking', default=[1, 2, 3, 4, 5])),
                   'alcohol': convertToList(request.args.get('alcohol', default=[1, 2, 3, 4, 5]))}}
    return createDictionaryOfVenna(createChoicesOfDataFrame(df, filters), subs)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7007)