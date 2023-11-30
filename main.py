import flet as ft
from flet.plotly_chart import PlotlyChart
import plotly.express as px
from settings_inputs import *
from vizualazing import analyze, createChart, createChoicesOfDataFrame

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
        expand=False,
        spacing=5,
        max_extent=400
    )

    page.add(content)

    def open_settings(e, i):
        # Сделать на выбор отображение оси X и Y 
        def close_settings(e):
            settings.open = False
            types = {'political':[int(not check.value)*(i+1) for i,check in enumerate(p_checkers) if not check.value],
            'people_main':[int(not check.value)*(i+1) for i,check in enumerate(pm_checkers) if not check.value],
            'life_main':[int(not check.value)*(i+1) for i,check in enumerate(lm_checkers) if not check.value]}
            chart = dropdown_charts.value
            content.controls[i].content.controls[0].controls[0].value = chart
            content.controls[i].content.controls[1] = createChart(createChoicesOfDataFrame(data, types), dropdown_options[chart], use_axis=axis_check.value, types=interests)
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

        def open_life(e):
            def close_window(e):
                window.open = False
                settings.open = True
                page.update()

            window = ft.AlertDialog(
                modal=True,
                title=ft.Text("Главное в жизни"),
                content=ft.Container(
                            content=ft.Column(expand=False,
                            controls=lm_checkers), 
                            height=400),
                actions=[ft.TextButton("Done", on_click=close_window)])

            page.add(window)
            window.open = True
            page.update()

        def on_change(e):
            settings.content.content.controls = settings.content.content.controls[:5]
            match dropdown_options[dropdown_charts.value]:
                case 'political' | 'people_main' | "life_main":
                    settings.content.content.controls.append(axis_check)
                case 'interests':
                    settings.content.content.controls.append(dropdown_interests)
                    settings.content.content.controls.append(ft.OutlinedButton(text="Добавить", on_click=add_interest))
                    for label in interests:
                        settings.content.content.controls.append(ft.Text(f'Добавлено: {label}', size=10))
            page.update()

        
        def delete_card(e):
            content.controls.pop(i)
            settings.open = False
            page.update()


        def add_interest(e):
            interests.append(dropdown_interests.value)
            on_change(e)


        dropdown_charts.on_change=on_change
        interests = []
        dropdown_interests.options = [ft.dropdown.Option(type_) for type_ in sorted(data.columns[11:], key=lambda x: sum(data[x].apply(lambda x: int(x)>0)))]

        settings = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройки"),
            content=ft.Container(content = ft.Column(controls=[dropdown_charts,ft.Text("Настроить пересечения интересов"), 
            ft.TextButton(text="Политические предпочтения", on_click=open_political), 
            ft.TextButton(text="Главное в людях", on_click=open_people),
            ft.TextButton(text="Главное в жизни", on_click=open_life)]), 
            height=400, width=300),
            actions=[ft.TextButton("Done", on_click=close_settings), ft.TextButton("Delete card", on_click=delete_card)]
        )
        on_change(e)

        page.add(settings)
        settings.open = True
        page.update()

    def add_card(e):

        i = len(content.controls)-1

        open_settings(e, i)

        content.controls[i] = (
            ft.Container(content=ft.Stack(
                controls=[ft.Row([ft.Text(dropdown_charts.value, size=16)], top=11, left=30),
                createChart(data, 'political', types=None),
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
               border_radius=20,
               expand=False
        ))

        content.controls.append(
        ft.Container(
            content=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor=BG_COLOR),
            width=400,
            height=400,
            border_radius=20,
            border=ft.border.all(2, SECONARY_BG_COLOR),
            expand=False
            )
        )
        page.update()

    content.controls.append(
        ft.Container(
            content=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor=BG_COLOR),
            width=400,
            height=400,
            border_radius=20,
            border=ft.border.all(2, SECONARY_BG_COLOR),
            expand=False
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)