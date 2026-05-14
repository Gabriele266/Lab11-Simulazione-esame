import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDGenre(self):
        genres = self._model.getGenres()
        for genre in genres:
            self._view._ddGenre.options.append(ft.dropdown.Option(genre))
        self._view.update_page()

    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        artists = self._model.getArtists()
        for artist in artists:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=artist.ArtistID,text=artist.Name))
        self._view.update_page()

    def handleCammino(self,e):
        bestPath = self._model.getBestPath(self._view._ddArtist.value)
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo trovato ({len(bestPath)} nodi):"))

        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.Name))

        self._view.update_page()
    def handleCreaGrafo(self,e):
        self._model.buildGraph(self._view._ddGenre.value)
        self.fillDDArtist()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{self._model.getNumEdges()}"))

        bestartist, best = self._model.getBestArtist()

        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {bestartist}, con influenza: {best}"))

        topEdges = self._model.getTop5Edges()

        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))

        for u, v, data in topEdges:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} : {data['weight']}"))

        self._view.update_page()