import flet as ft
import json


class Inputs:
    '''
    Класс, который создаёт каждый раз, когда нужно инпуты.

    Данные для инпутов хранятся в json файле.
    '''

    json = None


    def __init__(self, json_path = '/home/jezvgg/Projects/Behemoth/settings/inputs.json'):
        with open(json_path, 'r') as f:
            self.json = f.read()


    def __getitem__(self, input_name: str):
        inputs_json = json.loads(self.json)
        if input_name not in inputs_json.keys(): 
            raise KeyError("Таких инпутов в json нет!")

        return self.unserialize(inputs_json[input_name])


    def __get_kwargs(self, kwargs: dict):
        result = []
        for key, item in kwargs.items():
            match item:
                case str(): 
                    result.append(f'{key}="{item}"')
                case list():
                    print(f'{key}={self.unserialize(item)}')
                    result.append(f'{key}={self.unserialize(item)}')
                case _: 
                    result.append(f'{key}={item}')

        return ', '.join(result)


    def unserialize(self, args: list):
        # print([f'ft.{elem["class"]}({self.__get_kwargs(elem["kwargs"])})' for elem in args])
        return [eval(f'ft.{elem["class"]}({self.__get_kwargs(elem["kwargs"])})') for elem in args]


inputs = Inputs()