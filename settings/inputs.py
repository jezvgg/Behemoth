import flet as ft
from pathlib import Path
import json


class Inputs:
    '''
    Класс, который создаёт каждый раз, когда нужно инпуты.

    Данные для инпутов хранятся в json файле.
    '''

    inputs = None


    def __init__(self, json_path: Path = Path(Path.cwd(), 'settings/inputs.json')):
        with open(json_path, 'r') as f:
            json_file = f.read()
        self.inputs = json.loads(json_file)


    def __getitem__(self, input_name: str) -> list:
        if input_name not in self.inputs.keys(): 
            raise KeyError("Таких инпутов в json нет!")

        return [eval(f'ft.{elem["class"]}({self.__get_kwargs(elem["kwargs"])})') for elem in self.inputs[input_name]]


    def __get_kwargs(self, kwargs: dict):
        result = []
        for key, item in kwargs.items():
            match item:
                case str(): 
                    result.append(f'{key}="{item}"')
                case list():
                    result.append(f"{key}=[{', '.join([f'''ft.{elem['class']}({self.__get_kwargs(elem['kwargs'])})''' for elem in item])}]")
                case _: 
                    result.append(f'{key}={item}')

        return ', '.join(result)


inputs = Inputs()