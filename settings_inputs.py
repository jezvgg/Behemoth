import flet as ft

p_check1 = ft.Checkbox(label="коммунистические", value=True)
p_check2 = ft.Checkbox(label="социалистические", value=True)
p_check3 = ft.Checkbox(label="умеренные", value=True)
p_check4 = ft.Checkbox(label="либеральные", value=True)
p_check5 = ft.Checkbox(label="консервативные", value=True)
p_check6 = ft.Checkbox(label="монархические", value=True)
p_check7 = ft.Checkbox(label="ультраконсервативные", value=True)
p_check8 = ft.Checkbox(label="индифферентные", value=True)
p_check9 = ft.Checkbox(label="либертарианские", value=True)

p_checkers = [p_check1, p_check2, p_check3, p_check4, p_check5, p_check6, p_check7, p_check8, p_check9]

pm_check1 = ft.Checkbox(label="ум и креативность", value=True)
pm_check2 = ft.Checkbox(label="доброта и честность", value=True)
pm_check3 = ft.Checkbox(label="красота и здоровье", value=True)
pm_check4 = ft.Checkbox(label="власть и богатсво", value=True)
pm_check5 = ft.Checkbox(label="смелость и упорство", value=True)
pm_check6 = ft.Checkbox(label="юмор и жизнелюбие", value=True)

pm_checkers = [pm_check1, pm_check2, pm_check3, pm_check4, pm_check5, pm_check6]

dropdown_charts = ft.Dropdown(
            value="Политические предпочтения",
            label="Выбор графика",
            width=300,
            options=[
                ft.dropdown.Option("Политические предпочтения"),
                ft.dropdown.Option("Главное в людях"),
                ft.dropdown.Option("Главное в жизни"),
                ft.dropdown.Option("Интересы")
            ]
        )

dropdown_options = {"Политические предпочтения":'political',
"Главное в людях":"people_main",
"Главное в жизни":"life_main"}