import flet as ft
from time import sleep


class Settings:
    '''
    title

    content
    '''
    page: ft.Page
    _title = ''
    last_dialog = None
    content: ft.AlertDialog

    def __init__(self, page: ft.Page, title: str, *args, **kwargs):
        self._title = title
        self.content = ft.AlertDialog(title = ft.Text(title), 
                                      modal=True, 
                                      actions=[ft.TextButton("Done", on_click=self.close)],
                                      *args, **kwargs)
        self.page = page
        self.page.add(self.content)


    def close(self, e:ft.ControlEvent = None):
        self.content.open = False
        sleep(.1)
        self.page.dialog = self.last_dialog
        self.page.update()


    def fopen(self, e:ft.ControlEvent = None):
        self.last_dialog = self.page.dialog
        self.page.dialog = self.content
        self.content.open = True
        self.page.update()