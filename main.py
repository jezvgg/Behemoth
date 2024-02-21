import flet as ft
import pandas as pd
from controls.GridCard import GridCard
from controls.FlexGrid import FlexGrid


MAIN_COLOR = "#3366CC"
BG_COLOR = "#11151C"
SECONARY_BG_COLOR = "#1A202A"
SECONARY_COLOR = "#212D40"
CONTRAST_COLOR = "#D66853"


def main(page: ft.Page):
    page.title = "Behemoth"
    page.bgcolor = BG_COLOR

    header = ft.AppBar(toolbar_height=75, 
                       bgcolor=SECONARY_BG_COLOR,
                       title=ft.Text(value="Behemoth", size=36, weight=ft.FontWeight.W_600))
    page.appbar = header
    page.update()

    filename = 'content.csv'
    raw_df = pd.read_csv(filename)
    data = raw_df.fillna(0)

    page.analyze = data
    
    # content = ft.Container(
    #             content=ft.Row(
    #                         controls = [GridCard(page), GridCard(page)]
    #                         )
    #             )
    # page.add(content)
    grid = FlexGrid(page=page, card_height=400, card_width=400, fwidth=page.window_width, fheight=page.window_height, expand=True)
    # page.add(GridCard(page=page))
    # grid.add(GridCard(page=page), (1,1))
    # grid.add(GridCard(page=page), (1,2))
    page.update()


if __name__ == "__main__":
    ft.app(target=main)