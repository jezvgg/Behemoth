import flet as ft


class Settings(ft.AlertDialog):
    '''
    title

    content
    '''


    def __init__(self, *args):
        super().__init__(*args)
        self.modal = True
        self.actions=[ft.TextButton("Done", on_click=self.close())]


    def open(self):
        self.open = True
        self.update()


    def close(self):
        self.open = False
        self.update()