import networkx as nx
from database.dao import DAO
from UI.view import View



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
        self.G = nx.Graph()  # ricrea un grafo vuoto
        dict_connessioni = DAO.get_connessione()
        dict_rifugi = DAO.get_rifugio()
        for connessione in dict_connessioni.values():
            # reset per ogni connessione (evita usare valori residui)
            rifugio1 = ""
            rifugio2 = ""
            if int(connessione.anno) <= year:
                for rifugio in dict_rifugi.values():
                    if rifugio.id == connessione.id_rifugio1:
                        rifugio1 = rifugio.nome
                    if rifugio.id == connessione.id_rifugio2:
                        rifugio2 = rifugio.nome
                # aggiungo l'arco solo se ho trovato entrambi i nomi
                if rifugio1 and rifugio2:
                    self.G.add_edge(rifugio1, rifugio2)
        return self.G  # restituisce il grafo costruito

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        lista_nodi = nx.nodes(self.G)
        lista_rifugi = []
        dict_rifugi = DAO.get_rifugio()
        for nodo in lista_nodi:
            for rifugio in dict_rifugi.values():
                if nodo == rifugio.nome:
                    lista_rifugi.append(rifugio)
        return lista_rifugi

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        if hasattr(node, "nome"): # Se node è un oggetto Rifugio, usa il suo nome
            node = node.nome
        return self.G.degree[node]

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # reset lista interna per evitare conteggi errati su chiamate multiple
        self._lista_nodes = []
        n = 0
        lista_nodi = nx.nodes(self.G)
        for nodo in lista_nodi:
            if nodo not in self._lista_nodes:
                self._lista_nodes.append(nodo)
                nuovi_archi = self.get_reachable(nodo)
                for nuovo_nodo1, nuovo_nodo2 in nuovi_archi:
                    if nuovo_nodo1 not in self._lista_nodes:
                        self._lista_nodes.append(nuovo_nodo1)
                    elif nuovo_nodo2 not in self._lista_nodes:
                        self._lista_nodes.append(nuovo_nodo2)
                n += 1
        return n

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
        if hasattr(start, "nome"):
            start = start.nome
        tree = nx.dfs_tree(self.G, source=start)
        return list(tree.edges())

