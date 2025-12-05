import networkx as nx  # libreria per grafi
from database.dao import DAO  # import DAO per accedere ai dati

class Model:
    def __init__(self):
        self._lista_nodes = []  # lista interna usata per tracciare i nodi visitati
        self.G = nx.Graph()  # inizializza il grafo vuoto

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        self.G = nx.Graph()  # ricrea un grafo vuoto
        dict_connessioni = DAO.get_connessione()  # recupera tutte le connessioni dal DB
        dict_rifugi = DAO.get_rifugio()  # recupera tutti i rifugi dal DB
        for connessione in dict_connessioni.values():  # scorre ogni connessione
            # reset per ogni connessione (evita usare valori residui)
            rifugio1 = ""  # nome del primo rifugio
            rifugio2 = ""  # nome del secondo rifugio
            if int(connessione.anno) <= year:  # considera solo connessioni fino all’anno dato
                for rifugio in dict_rifugi.values():  # cerca nomi dei rifugi
                    if rifugio.id == connessione.id_rifugio1:
                        rifugio1 = rifugio.nome  # salva nome rifugio 1
                    if rifugio.id == connessione.id_rifugio2:
                        rifugio2 = rifugio.nome  # salva nome rifugio 2
                # aggiungo l'arco solo se ho trovato entrambi i nomi
                if rifugio1 and rifugio2:
                    self.G.add_edge(rifugio1, rifugio2)  # aggiunge l'arco nel grafo
        return self.G  # restituisce il grafo costruito

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        lista_nodi = nx.nodes(self.G)  # prende i nodi dal grafo
        lista_rifugi = []  # lista degli oggetti Rifugio
        dict_rifugi = DAO.get_rifugio()  # recupera rifugi dal DB
        for nodo in lista_nodi:  # scorri nodi (nomi)
            for rifugio in dict_rifugi.values():  # scorri oggetti rifugio
                if nodo == rifugio.nome:
                    lista_rifugi.append(rifugio)  # aggiungi oggetto rifugio corrispondente
        return lista_rifugi  # restituisci lista rifugi

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        if hasattr(node, "nome"): # Se node è un oggetto Rifugio, usa il suo nome
            node = node.nome  # estrai nome
        return self.G.degree[node]  # restituisce il grado del nodo nel grafo

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # reset lista interna per evitare conteggi errati su chiamate multiple
        self._lista_nodes = []  # reset nodi visitati
        n = 0  # contatore componenti connesse
        lista_nodi = nx.nodes(self.G)  # lista nodi del grafo
        for nodo in lista_nodi:  # scorri tutti i nodi
            if nodo not in self._lista_nodes:  # se nodo non ancora visitato
                self._lista_nodes.append(nodo)  # segna come visitato
                nuovi_archi = self.get_reachable(nodo)  # trova i nodi raggiungibili
                for nuovo_nodo1, nuovo_nodo2 in nuovi_archi:  # ogni arco della componente
                    if nuovo_nodo1 not in self._lista_nodes:
                        self._lista_nodes.append(nuovo_nodo1)  # aggiungi nodo1 visitato
                    elif nuovo_nodo2 not in self._lista_nodes:
                        self._lista_nodes.append(nuovo_nodo2)  # aggiungi nodo2 visitato
                n += 1  # incrementa numero componenti
        return n  # restituisci numero componenti

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
            start = start.nome  # se arriva un oggetto Rifugio usa il nome

        # METODO 1
        edges = []  # lista archi trovati nella DFS ricorsiva
        visited = set()  # insieme nodi visitati
        def dfs(v):  # funzione ricorsiva DFS
            for nbr in self.G.neighbors(v):  # scorri vicini del nodo
                if nbr not in visited:  # se non visitato
                    visited.add(nbr)  # marca visitato
                    edges.append((v, nbr))  # salva arco esplorato
                    dfs(nbr)  # chiamata ricorsiva
        visited.add(start)  # aggiunge nodo iniziale
        dfs(start)  # avvia DFS
        #return edges  # (non usato, ma valido)

        # METODO 2
        tree = nx.dfs_tree(self.G, source=start)  # DFS con NetworkX
        return list(tree.edges())  # restituisce lista archi del DFS tree
