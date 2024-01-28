import flet as ft
from time import sleep


class Settings(ft.AlertDialog):
    '''
    title

    content
    '''
    page = None
    _title = ''
    last_dialog = None

    def __init__(self, page: ft.Page, title: str, *args, **kwargs):
        self._title = title
        super().__init__(title = ft.Text(title), 
                        modal=True, 
                        actions=[ft.TextButton("Done", on_click=self.close)],
                        *args, **kwargs)
        self.page = page


    def close(self, e:ft.ControlEvent = None):
        self.open = False
        sleep(0.1)
        self.page.dialog = self.last_dialog
        self.page.update()


    def fopen(self, e:ft.ControlEvent = None):
        self.last_dialog = self.page.dialog
        self.page.dialog = self
        self.open = True
        self.page.update()