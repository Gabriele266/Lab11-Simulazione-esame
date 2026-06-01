import copy

from database.DAO import DAO
import networkx as nx
from collections import defaultdict
import itertools
class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []

    def getBestPath(self, source):

        self._bestPath = []

        partial = [self._idMap[int(source)]]

        for _, v, data in self._graph.out_edges(self._idMap[int(source)], data=True):
            partial.append(v)

            self._ricorsione(partial, data["weight"])
            partial.pop()


        return self._bestPath

    def _ricorsione(self, partial, lastWeight):

        # update best solution
        if len(partial) > len(self._bestPath):
            self._bestPath = copy.deepcopy(partial)

        current = partial[-1]

        for _, successor, data in self._graph.out_edges(current, data=True):

            weight = data["weight"]

            # strictly decreasing weights
            if weight > lastWeight:

                # simple path
                if successor not in partial:
                    partial.append(successor)

                    self._ricorsione(partial, weight)

                    partial.pop()
    def buildGraph(self, genere):
        self._graph.clear()
        self._artist = DAO.getAllArtistbyGenre(genere)
        for a in self._artist:
            self._idMap[a.ArtistID] = a

        self._graph.add_nodes_from(self._artist)

        custom_artist_list = DAO.getCustomerArtistCounts(genere)

        customerMap = defaultdict(dict)

        for customer_id, artist_id, ntracks in custom_artist_list:
            customerMap[customer_id][artist_id] = ntracks

        artist_popularity = defaultdict(int)

        for customer, artists in customerMap.items():
            for artist_id, ntracks in artists.items():
                artist_popularity[artist_id] += ntracks

        for customer_id, artists in customerMap.items():

            for a, b in itertools.combinations(artists.keys(), 2):

                pop_a = artist_popularity[a]
                pop_b = artist_popularity[b]

                weight = pop_a + pop_b

                if pop_a < pop_b:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
                elif pop_a > pop_b:
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)
                else:
                    self._graph.add_edge(self._idMap[a], self._idMap[b], weight=weight)
                    self._graph.add_edge(self._idMap[b], self._idMap[a], weight=weight)


    def getBestArtist(self):

        bestArtist = None
        bestScore = None

        for v in self._graph.nodes():

            outWeight = 0
            for _, _, data in self._graph.out_edges(v, data=True):
                outWeight += data["weight"]

            inWeight = 0
            for _, _, data in self._graph.in_edges(v, data=True):
                inWeight += data["weight"]

            score = outWeight - inWeight

            if bestScore is None or score > bestScore:
                bestScore = score
                bestArtist = v

        return bestArtist.Name, bestScore

    def getTop5Edges(self):

        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )

        return edges[:5]

    def getGenres(self):
        return DAO.getAllGenres()

    def getArtists(self):
        return self._graph.nodes()
    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)