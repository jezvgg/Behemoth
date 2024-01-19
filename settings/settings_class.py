import flet as ft


class Settings(ft.AlertDialog):
    '''
    title

    content
    '''
    page = None

    def __init__(self, page: ft.Page, title: str, *args, **kwargs):
        super().__init__(title = ft.Text(title), 
                        modal=True, 
                        actions=[ft.TextButton("Done", on_click=self.close)],
                        *args, **kwargs)
        self.page = page


    def close(self, e:ft.ControlEvent = None):
        self.open = False
        self.page.update()


    def fopen(self, e:ft.ControlEvent = None):
        self.open = True
        self.page.update()