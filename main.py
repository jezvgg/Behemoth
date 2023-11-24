import flet as ft
import time

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
    nav_rail = ft.NavigationRail(
        bgcolor=SECONARY_BG_COLOR,  
        group_alignment=-1.0,
        min_width=100,
        min_extended_width=400,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL)
    page.add(
        ft.Row(nav_rail, expand=True))
    page.update()


ft.app(target=main)