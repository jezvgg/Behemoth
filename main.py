import flet as ft
from settings_inputs import *
from vizualazing import analyze, createChart, createChoicesOfDataFrame
from Card import Card, NewCard
from myGrid import FlexGrid
from time import sleep


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

    # Переписать data, чтоб не сохраняла csv а сразу передавала DataFrame
    data = analyze()
    
    # Переписать FlexGrid на любой размер экрана без заданных конекретных размеров
    main_content = FlexGrid(size=(4,4), spacing=10, expand=True)

    page.add(main_content)

    # Вынести все настройки в GridCard
    def open_settings(e, i):

        def close_settings(e):
            settings.open = False
            types = {'political':[int(not check.value)*(i+1) for i,check in enumerate(p_checkers) if not check.value],
            'people_main':[int(not check.value)*(i+1) for i,check in enumerate(pm_checkers) if not check.value],
            'life_main':[int(not check.value)*(i+1) for i,check in enumerate(lm_checkers) if not check.value]}
            chart = dropdown_charts.value
            main_content.resize(i, sizes_values[dropdown_sizes.value])
            main_content[i] = Card(label=chart, 
            chart=createChart(createChoicesOfDataFrame(data, types), dropdown_options[chart], use_axis=axis_check.value, types=interests),
            size=sizes_values[dropdown_sizes.value],
            open_settings=lambda x: open_settings(x, i))
            page.update()
            dropdown_charts.value = 'Политика (столбцы)'
            dropdown_sizes.value = '1 х 1'
            dropdown_interests.value = 'Юмор'
            settings.content.content.controls = settings.content.content.controls[:6]


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
            settings.content.content.controls = settings.content.content.controls[:6]
            match dropdown_options[dropdown_charts.value]:
                case 'political' | 'people_main' | "life_main":
                    settings.content.content.controls.append(axis_check)
                case 'interests':        
                    settings.content.content.controls.append(dropdown_interests)
                    settings.content.content.controls.append(append_button)
                    for label in interests:
                        settings.content.content.controls.append(ft.Text(f'Добавлено: {label}', size=10))
                    page.update()
            page.update()

        
        def delete_card(e):
            main_content.pop(i)
            settings.open = False
            page.update()


        def add_interest(e):
            interests.append(dropdown_interests.value)
            sleep(0.02)
            on_change(e)


        dropdown_charts.on_change=on_change
        interests = []
        dropdown_interests.options = dropdown_interests.options = [ft.dropdown.Option(type_) for type_ in sorted(data.columns[11:], key=lambda x: sum(data[x].apply(lambda x: int(x)>0)))]
        dropdown_interests.value = 'Юмор'
        append_button.on_click=add_interest

        # Вот это вынести в GridCard
        settings = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройки"),
                content=ft.Container(content = ft.Column(controls=[
                dropdown_charts,ft.Text("Настроить пересечения интересов"), 
                dropdown_sizes,
                ft.TextButton(text="Политические предпочтения", on_click=open_political), 
                ft.TextButton(text="Главное в людях", on_click=open_people),
                ft.TextButton(text="Главное в жизни", on_click=open_life)]), 
            height=400, width=300),
            actions=[ft.TextButton("Done", on_click=close_settings), ft.TextButton("Delete card", on_click=delete_card)],
            on_dismiss=lambda _: print("Dismiss")
        )
        on_change(e)
        settings.open = True
        page.add(settings)

    def add_card(e):

        i = len(main_content)-1

        open_settings(e, i)

        # Переписать Card
        main_content[i] = Card(
            label='Политика (столбцы)',
            chart=createChart(data, 'political', ['political']),
            size=(1,1),
            open_settings=lambda x: open_settings(x,i)
        )

        main_content.append(NewCard(add_card))
        page.update()

    main_content.append(NewCard(add_card))

    page.update()

if __name__ == "__main__":
    ft.app(target=main)