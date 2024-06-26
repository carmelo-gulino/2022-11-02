import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.chosen_genre = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_genre(self):
        for g in self.model.genres:
            self.view.dd_genre.options.append(ft.dropdown.Option(data=g, text=g.Name, on_click=self.choose_genre))

    def choose_genre(self, e):
        if e.control.data is None:
            self.chosen_genre = None
        self.chosen_genre = e.control.data

    def handle_grafo(self, e):
        if self.chosen_genre is None:
            self.view.create_alert("Scegliere un genere")
            return
        try:
            d_min = to_milliseconds(float(self.view.txt_min.value))
            d_max = to_milliseconds(float(self.view.txt_max.value))
        except ValueError:
            self.view.create_alert("Inserire una durata minima e una massima")
            return
        if d_min < self.model.durate_min[self.chosen_genre.GenreId][0]:
            self.view.create_alert("La durata minima è troppo bassa per questo genere")
        else:
            graph = self.model.build_graph(self.chosen_genre.GenreId, d_min, d_max)
            self.view.txt_result.controls.clear()
            self.view.txt_result.controls.append(
                ft.Text(f"Grafo con {len(graph.nodes)} nodi e {len(graph.edges)} archi"))
            self.handle_connesse()
            self.view.txt_dTot.disabled = False
            self.view.btn_playlist.disabled = False
            self.view.update_page()

    def handle_connesse(self):
        connesse = self.model.get_connesse()
        self.view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(connesse)} componenti connesse"))
        for c in connesse:
            distinct_playlists = self.model.get_distinct_playlists(c)
            self.view.txt_result.controls.append(
                ft.Text(f"{len(c)} vertici, inseriti in {distinct_playlists} playlist"))

    def handle_playlist(self, e):
        try:
            d_tot = to_milliseconds(float(self.view.txt_dTot.value)*60)
        except ValueError:
            self.view.create_alert("Inserire una durata totale")
            return
        playlist = self.model.get_playlist(d_tot)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"La playlist trovata è la seguente:"))
        for p in playlist:
            self.view.txt_result.controls.append(ft.Text(f"{p}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model


def to_milliseconds(d):
    return d*1000
