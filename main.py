import flet as ft
from flet.plotly_chart import PlotlyChart
import plotly.express as px
from settings_inputs import p_checkers, pm_checkers, dropdown_charts, dropdown_options
from vizualazing import analyze, createBarChart, createChoicesOfDataFrame

def main(page: ft.Page):
    MAIN_COLOR = "#3366CC"
    BG_COLOR = "#11151C"
    SECONARY_BG_COLOR = "#1A202A"
    SECONARY_COLOR = "#212D40"
    CONTRAST_COLOR = "#D66853"
    page.title = "Behemoth"
    page.bgcolor = BG_COLOR
    header = ft.AppBar(toolbar_height=75, 
                       bgcolor=SECONARY_BG_COLOR,
                       title=ft.Text(value="Behemoth", size=36, weight=ft.FontWeight.W_600))
    page.appbar = header
    page.update()

    data = analyze()
    
    content = ft.GridView(
        expand=1,
        spacing=5,
        max_extent=400
    )

    page.add(content)

    def open_settings(e, i):
        # Сделать на выбор отображение оси X и Y 
        def close_settings(e):
            settings.open = False
            types = {'political':[int(not check.value)*(i+1) for i,check in enumerate(p_checkers) if not check.value],
            'people_main':[int(not check.value)*(i+1) for i,check in enumerate(pm_checkers) if not check.value]}
            chart = dropdown_charts.value
            content.controls[i].content.controls[0].controls[0].value = chart
            content.controls[i].content.controls[1] = createBarChart(createChoicesOfDataFrame(data, types), dropdown_options[chart])
            page.update()

        def open_political(e):
            def close_window(e):
                window.open = False
                settings.open = True
                page.update()

            window = ft.AlertDialog(
                modal=True,
                title=ft.Text("Политические предпочтения"),
                content=ft.Container(
                            content = ft.Column(expand=False,
                            controls=p_checkers), 
                            height=400),
                actions=[ft.TextButton("Done", on_click=close_window)])

            page.add(window)
            window.open = True
            page.update()

        def open_people(e):
            def close_window(e):
                window.open = False
                settings.open = True
                page.update()

            window = ft.AlertDialog(
                modal=True,
                title=ft.Text("Главное в людях"),
                content=ft.Container(
                            content=ft.Column(expand=False,
                            controls=pm_checkers), 
                            height=400),
                actions=[ft.TextButton("Done", on_click=close_window)])

            page.add(window)
            window.open = True
            page.update()

        settings = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройки"),
            content=ft.Container(content = ft.Column(controls=[dropdown_charts,ft.Text("Настроить пересечения интересов"), 
            ft.TextButton(text="Политические предпочтения", on_click=open_political), 
            ft.TextButton(text="Главное в людях", on_click=open_people)]), height=400, width=300),
            actions=[ft.TextButton("Done", on_click=close_settings)]
        )

        page.add(settings)
        settings.open = True
        page.update()

    def add_card(e):

        i = len(content.controls)-1

        open_settings(e, i)

        content.controls[i] = (
            ft.Container(content=ft.Stack(
                controls=[ft.Row([ft.Text(dropdown_charts.value, size=16)], top=11),
                createBarChart(data, dropdown_options[dropdown_charts.value]),
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    icon_color=SECONARY_COLOR,
                    icon_size=30,
                    tooltip="Settings",
                    on_click=lambda x: open_settings(x, i),
                    right=0
                )]
            ), width=400,
               height=400,
               padding=20,
               border = ft.border.all(2, SECONARY_BG_COLOR),
               border_radius=20
        ))

        content.controls.append(
        ft.Container(
            content=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor=BG_COLOR),
            width=600,
            height=600,
            border_radius=20,
            border=ft.border.all(2, SECONARY_BG_COLOR)
            )
        )
        page.update()

    content.controls.append(
        ft.Container(
            content=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor=BG_COLOR),
            width=600,
            height=600,
            border_radius=20,
            border=ft.border.all(2, SECONARY_BG_COLOR)
        )
    )

    page.update()


ft.app(target=main)