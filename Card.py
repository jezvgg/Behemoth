import flet as ft


class Card(ft.Container):
    label = ''
    chart = None
    size = None
    
    def __init__(self, label: str, chart, size, open_settings, *args, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.chart = chart
        self.size = size
        self.content = ft.Stack(
            controls=[
                ft.Row([ft.Text(label, size=16)], top=11, left=30),
                chart,
                ft.IconButton(
                    icon = ft.icons.SETTINGS,
                    icon_color = "#212D40",
                    icon_size = 30,
                    tooltip = "Settings",
                    on_click=open_settings,
                    right = 0
                )
            ]
        )
        self.width = size[0] * 400
        self.height = size[1] * 400
        self.padding = 20
        self.border = ft.border.all(2, "#1A202A")
        self.border_radius=20


    def __str__(self):
        return f'MyCard({self.label}, {self.chart}, {self.size}) at ({self.right}, {self.top})'


    def __repr__(self):
        return str(self)



class NewCard(ft.Container):

    def __init__(self, add_card):
        super().__init__()
        self.content = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor="#11151C")
        self.width = 400
        self.height = 400
        self.padding = 20
        self.border = ft.border.all(2, "#1A202A")
        self.border_radius=20