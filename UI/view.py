import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self.page = page
        self.page.title = "Template application using MVC and DAO"
        self.page.horizontal_alignment = 'CENTER'
        self.page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.dd_genre = None
        self.btn_grafo = None
        self.txt_min = None
        self.txt_max = None
        self.txt_dTot = None
        self.btn_playlist = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Hello World", color="blue", size=24)
        self.page.controls.append(self._title)

        self.dd_genre = ft.Dropdown(label="Genre")
        self.controller.fill_dd_genre()
        self.btn_grafo = ft.ElevatedButton(text="Crea grafo", on_click=self.controller.handle_grafo)
        row1 = ft.Row([self.dd_genre, self.btn_grafo], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row1)

        self.txt_min = ft.TextField(label="Min")
        row2 = ft.Row([self.txt_min], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row2)

        self.txt_max = ft.TextField(label="Max")
        row3 = ft.Row([self.txt_max], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(row3)

        self.txt_dTot = ft.TextField(label="dTot",
                                     disabled=True)
        self.btn_playlist = ft.ElevatedButton(text="La mia playlist",
                                              disabled=True,
                                              on_click=self.controller.handle_playlist)
        ro4 = ft.Row([self.txt_dTot, self.btn_playlist], alignment=ft.MainAxisAlignment.CENTER)
        self.page.controls.append(ro4)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.page.controls.append(self.txt_result)
        self.page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_page(self):
        self.page.update()
