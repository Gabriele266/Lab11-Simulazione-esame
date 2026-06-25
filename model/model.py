import itertools

import networkx as nx

from database.DAO import DAO
from model.Artist import Artist


class Model:

    def __init__(self):
        self.selected_genre_id: int | None = None       # Id correntemente selezionato nel dropdown genere
        self.graph: nx.DiGraph | None = None

    def create_graph(self):
        dao = DAO()
        # carico la lista di autori che hanno fatto almeno un brano con il genere giusto
        artists = dao.load_artists_info(self.selected_genre_id)
        graph = nx.DiGraph()
        graph.add_nodes_from(artists)

        info_table = dao.load_info_table(self.selected_genre_id)

        # carico le popolarità di tutti gli artisti
        for artist in graph.nodes:
            artist.popularity = self.calc_popularity(info_table, artist.ArtistId)

        for a, b in itertools.combinations(artists, 2):
            customers_a = list(filter(lambda row: row["ArtistId"] == a.ArtistId, info_table))
            customers_b = list(filter(lambda row: row["ArtistId"] == b.ArtistId, info_table))

            customer_ids_a = set(map(lambda row: row["CustomerId"], customers_a))
            customer_ids_b = set(map(lambda row: row["CustomerId"], customers_b))

            if len(customer_ids_a & customer_ids_b) > 0:
                print(f"Tra l'artista {a} e {b} esiste un arco")
                self.__add_edge_between(a, b, graph)

        self.graph = graph
        dao.close()

    def __add_edge_between(self, a: Artist, b: Artist, graph: nx.DiGraph):
        if a.popularity > b.popularity:
            graph.add_edge(a, b, weight = a.popularity + b.popularity)
        elif a.popularity < b.popularity:
            graph.add_edge(b, a, weight = a.popularity + b.popularity)
        else:
            graph.add_edge(a, b, weight = a.popularity + b.popularity)
            graph.add_edge(b, a, weight = a.popularity + b.popularity)

    def calc_popularity(self, info_table, artist_id: int):
        rowsForArtist = filter(lambda row: row["ArtistId"] == artist_id, info_table)

        pop = 0
        for r in rowsForArtist:
            pop += r["conteggio_track"]

        return pop


    def search_most_influent_artist(self)-> Artist:
        graph: nx.DiGraph = self.graph

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

    def get_ordered_edges(self):
        print(list(self.graph.edges(data=True)))
        return sorted(list(self.graph.edges(data=True)),
                      key=lambda t: t[2]["weight"], reverse=True)