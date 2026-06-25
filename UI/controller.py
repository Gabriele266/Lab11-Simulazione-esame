import itertools

import flet as ft
import networkx as nx
from mysql.connector import DatabaseError

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
        if self._model.selected_genre_id is None:
            self._view.create_alert("Nessun genere selezionato, sceglierne uno dal menu a tendina. ")
            return

        try:
            self._model.create_graph()
            self.__show_results__()
        except DatabaseError as e:
            print(f"Errore durante la costruzione del grafo {e}")
            self._view.create_alert(e.msg)

    def __show_results__(self):
        graph: nx.DiGraph = self._model.graph
        txt_result: ft.ListView = self._view.txt_result
        most_influent = self._model.search_most_influent_artist()
        ordered = self._model.get_ordered_edges()

        txt_result.controls = [
            ft.Text(
                f"Il grafo creato ha {graph.number_of_nodes()} nodi e {graph.number_of_edges()} archi"
            ),
            ft.Text(
                f"L'artista con maggiore influenza è {most_influent.Name} con influenza {graph.nodes[most_influent]["influence"]}"
            ),
        ]

        for o in ordered[0:5]:
            txt_result.controls.append(
                ft.Text(f"{o[0].Name} -> {o[1].Name} con peso {o[2]["weight"]}")
            )

        self._view.update_page()

    def handleCammino(self,e):
        pass