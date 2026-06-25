import networkx as nx

from model.Artist import Artist


class RecursivePath:
    def __init__(self, graph, artist: Artist):
        self.max_length = 0
        self.graph: nx.DiGraph = graph
        self.artist = artist
        self.optimal_path = None

    def get_max_path_vricorsiva(self) -> list[Artist] | None:
        path = []
        self.__explore_dfs(self.artist, path, 0)

        return self.optimal_path

    def __explore_dfs(self,
                      node: Artist,
                      path: list[Artist],
                      previous_weight: int):
        out_edges = self.graph.out_edges(node, data=True)  # Archi in uscita dal nodo che devo esplorare

        if len(out_edges) == 0:
            # Percorso terminato
            if len(path) > self.max_length:
                # Controllo se è un nuovo ottimo
                self.max_length = len(path)  # Nuovo percorso ottimo.
                self.optimal_path = [self.artist] + list(path)  # Copio il percorso per averlo da parte
        else:
            for edge in out_edges:
                destination = edge[1]
                if destination in path:
                    continue

                weight = edge[2]["weight"]
                if weight > previous_weight:
                    path.append(destination)
                    self.__explore_dfs(destination, path, weight)
                    # Backtracking
                    path.remove(destination)
