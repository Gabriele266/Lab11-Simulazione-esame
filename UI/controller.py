import itertools

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
        self._model.create_graph()
        self.__show_results__()

    def __show_results__(self):
        graph: nx.DiGraph = self._model.graph
        txt_result: ft.ListView = self._view.txt_result
        most_influent = self.__search_most_influent_artist()

        txt_result.controls = [
            ft.Text(
                f"Il grafo creato ha {graph.number_of_nodes()} nodi e {graph.number_of_edges()} archi"
            ),
            ft.Text(
                f"L'artista con maggiore influenza è {most_influent.Name} con influenza {graph.nodes[most_influent]["influence"]}"
            )
        ]
        self._view.update_page()

    def __search_most_influent_artist(self)-> Artist:
        graph: nx.DiGraph = self._model.graph

        max_influence = None
        max_artist = None

        for artist in graph.nodes:
            pred = graph.predecessors(artist)
            succ = graph.successors(artist)
            a = 0
            for p in pred:
                a += graph.edges[p, artist]["weight"]

            b = 0
            for p in succ:
                b += graph.edges[artist, p]["weight"]

            influence = b - a
            graph.nodes[artist]["influence"] = influence
            print(f"L'artista {artist} ha influenza {graph.nodes[artist]["influence"]}")
            if max_influence is None or influence > max_influence:
                max_influence = influence
                max_artist = artist

        return max_artist

    def handleCammino(self,e):
        pass