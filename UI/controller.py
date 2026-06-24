import flet as ft
import networkx as nx

from database.DAO import DAO
from database.DB_connect import DBConnect
from model.Artist import Artist


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        allGenres = DAO.load_genres_list()
        dropdown: ft.Dropdown = self._view._ddGenre
        dropdown.options = [
            (ft.dropdown.Option(
                key=genre.GenreId,
                text=genre.Name
            )) for genre in allGenres
        ]
        self._view.update_page()

    def handleGenreDropdownSelect(self, event):
        self._model.selected_genre_id = event.data

    def handleCreaGrafo(self, e):
        dao = DAO()
        # carico la lista di autori che hanno fatto almeno un brano con il genere giusto
        artists = dao.load_artists_info(self._model.selected_genre_id)
        graph = nx.DiGraph()

        for a in artists:
            for b in artists:
                if a != b:
                    customers_a = dao.load_customers_for_artist(a.ArtistId)
                    customers_b = dao.load_customers_for_artist(b.ArtistId)

                    intersect = customers_b & customers_a
                    if len(intersect) > 0:
                        print(f"Tra l'artista {a.ArtistId} e {b.ArtistId} esiste una connessione")
                        self.__add_edge_between(a, b, graph)

        print(f"Il grafo creato ha {graph.number_of_nodes()} nodi e {graph.number_of_edges()} archi")
        dao.close()

    def __add_edge_between(self, a: Artist, b: Artist, graph: nx.DiGraph):
        if a.popularity > b.popularity:
            graph.add_edge(a, b, weight = a.popularity + b.popularity)
        elif a.popularity < b.popularity:
            graph.add_edge(b, a, weight = a.popularity + b.popularity)
        else:
            graph.add_edge(a, b, weight = a.popularity + b.popularity)
            graph.add_edge(b, a, weight = a.popularity + b.popularity)


    def handleCammino(self,e):
        pass