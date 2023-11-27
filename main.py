import flet as ft
from settings_checkers import p_checkers, pm_checkers

def main(page: ft.Page):
    MAIN_COLOR = "#364156"
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
    
    content = ft.GridView(
        expand=1,
        spacing=5,
        max_extent=400
    )

    page.add(content)

    def open_settings(e):
        def close_settings(e):
            settings.open = False
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

        dropdown_charts = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Политические предпочтения"),
                ft.dropdown.Option("Главное в людях"),
                ft.dropdown.Option("Главное в жизни"),
                ft.dropdown.Option("Интересы")
            ]
        )

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

        open_settings(e)

        content.controls.append(content.controls[-1])
        
        content.controls[-2] = (
            ft.Container(
                width=400,
                height=400,
                border_radius=20,
                border=ft.border.all(2, SECONARY_BG_COLOR)
            )
        )
        page.update()

    content.controls.append(
        ft.Container(
            content=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_card, bgcolor=BG_COLOR),
            width=400,
            height=400,
            border_radius=20,
            border=ft.border.all(2, SECONARY_BG_COLOR)
        )
    )

    page.update()


ft.app(target=main)