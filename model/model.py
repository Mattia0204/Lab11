import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self._nodes = None  # memorizza il numero di nodi del grafo
        self._lista_nodes = []
        self._edges = None  # memorizza il numero di archi del grafo
        self._lista_edges = []
        self.G = nx.Graph()  # inizializza il grafo vuoto

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        lista_rifugi = DAO.get_rifugio()  # recupera tutti i rifugi dal database
        lista_rifugi_distinti = []
        for rifugio in lista_rifugi.values():  # scorre tutti i rifugi
            if rifugio.id not in lista_rifugi_distinti:  # verifica se il rifugio è già aggiunto
                lista_rifugi_distinti.append(rifugio.id)
                self._lista_nodes.append(rifugio)
        self._nodes = len(lista_rifugi_distinti)  # calcola il numero totale di nodi
        return self._lista_nodes

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
