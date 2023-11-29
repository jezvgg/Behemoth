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

lm_check1 = ft.Checkbox(label="семья и дети", value=True)
lm_check2 = ft.Checkbox(label="карьера и деньги", value=True)
lm_check3 = ft.Checkbox(label="развлечения и отдых", value=True)
lm_check4 = ft.Checkbox(label="наука и исследования", value=True)
lm_check5 = ft.Checkbox(label="совершенствование мира", value=True)
lm_check6 = ft.Checkbox(label="саморазвитие", value=True)
lm_check7 = ft.Checkbox(label="красота и искусство", value=True)
lm_check8 = ft.Checkbox(label="слава и влияние", value=True)

lm_checkers = [lm_check1, lm_check2, lm_check3, lm_check4, lm_check5, lm_check6, lm_check7, lm_check8]

dropdown_charts = ft.Dropdown(
            value="Политика (столбцы)",
            label="Выбор графика",
            width=300,
            options=[
                ft.dropdown.Option("Политика (столбцы)"),
                ft.dropdown.Option("Главное в людях (столбцы)"),
                ft.dropdown.Option("Главное в жизни (столбцы)"),
                ft.dropdown.Option("Политика (пирог)"),
                ft.dropdown.Option("Главное в людях (пирог)"),
                ft.dropdown.Option("Главное в жизни (пирог)"),
                ft.dropdown.Option("Пол"),
                ft.dropdown.Option("Интересы")
            ]
        )

dropdown_options = {"Политика (столбцы)":'political',
"Главное в людях (столбцы)":"people_main",
"Главное в жизни (столбцы)":"life_main",
"Политика (пирог)":"politicalPie",
"Главное в людях (пирог)":"people_mainPie",
"Главное в жизни (пирог)":"life_mainPie",
"Пол":"sexPie"}

axis_check = ft.Checkbox(label="Отобразить оси", value=True)