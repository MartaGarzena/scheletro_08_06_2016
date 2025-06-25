import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Simulazione Gara"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()

        self._controller = None

    def load_interface(self):
        self._title = ft.Text("Simulazione Gara", color="blue", size=24)
        self._page.controls.append(self._title)

        # Dropdown Anno + Bottone Seleziona stagione
        self._ddAnno = ft.Dropdown(label="Anno", width=200)
        self._controller.fillDDYear()

        self._btnSelezionaStagione = ft.ElevatedButton(text="Seleziona stagione", on_click=self._controller.handleSelezionaStagione)

        row1 = ft.Row([
            self._ddAnno,
            self._btnSelezionaStagione
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Dropdown Gara + Bottone Simula Gara
        self._ddGara = ft.Dropdown(label="Gara", width=250)

        self._btnSimulaGara = ft.ElevatedButton(text="Simula gara", on_click=self._controller.handleSimulaGara)

        row2 = ft.Row([
            self._ddGara,
            self._btnSimulaGara
        ], alignment=ft.MainAxisAlignment.CENTER)

        # TextFields: Valore P e Valore T
        self._txtValoreP = ft.TextField(label="Valore P", width=150,   keyboard_type=ft.KeyboardType.NUMBER)
        self._txtValoreT = ft.TextField(label="Valore T", width=150)

        row3 = ft.Row([
            self._txtValoreP,
            self._txtValoreT
        ], alignment=ft.MainAxisAlignment.CENTER)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Aggiunta dei componenti alla pagina
        self._page.controls.extend([row1, row2, row3, self.txt_result])
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()
