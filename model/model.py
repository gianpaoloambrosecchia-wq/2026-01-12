import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapIdC = {}
        # Visto che non tutti i costruttori sono nodi del grafo,
        # mi trovo tutti i costruttori e li metto in una lista e
        # ci costruisco l'idMap, così nell'idMap ho anche i costruttori
        # che non sono nel grafo
        costruttori = DAO.getAllConstructors()
        for c in costruttori:
            self._idMapIdC[c.constructorId] = c
        self._solBest = []
        self._scartoBest = 0


    def getAllYears(self):
        anni = DAO.getAllYears()
        return anni

    def buildGrafo(self, anno1, anno2):
        self._graph.clear()
        nodes = DAO.getAllNodes(anno1,anno2, self._idMapIdC)
        self._graph.add_nodes_from(nodes)
        self.addEdges(anno1,anno2)

    def addEdges(self, anno1, anno2):
        edges = DAO.getAllEdges(self._idMapIdC, anno1,anno2)
        for e in edges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)

    def infoConnessa(self):
        # Restituisce una lista di set (ognuno con una componente connessa)
        componenti = list(nx.connected_components(self._graph))
        # c) Componente più grande
        componente_grande = max(componenti, key=len)

        # Ordino i nodi per grado decrescente
        nodi_ordinati = sorted(componente_grande,
                               key=lambda n: self._graph.degree(n),
                               reverse=True)
        return len(componenti), componente_grande, nodi_ordinati

    def getPrimiTreArchi(self):
        # Se ci sono meno di due 3 archi restituisce gli archi presenti
        if self.getNumEdges() < 3:
            return self._graph.edges

        # Ordino in ordine decrescente (reverse = True) gli archi in base al peso e prendo i primi 3 (cioè
        # i primi 3 con peso maggiore)
        # RICORDA!!! data=True per considerare il peso
        archi_ordinati = sorted(self._graph.edges(data = True), key = lambda x: x[2]["weight"], reverse = True)
        primiTreArchi = []
        for i in range(0, 3):
            primiTreArchi.append(archi_ordinati[i])
        return primiTreArchi



    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)


    def cerca(self, k):
        DAO.getPilotaPiuAnzianoPerCostruttore(self._idMapIdC)
        print(f"Nodi totali: {self._graph.number_of_nodes()}")
        print(f"Componenti connesse: {nx.number_connected_components(self._graph)}")
        print(f"Nodi con dob valido: {sum(1 for n in self._graph.nodes if n.oldest_driver_dob is not None)}")
        parziale = []
        self._solBest = []
        self._scartoBest = 0
        self._ricorsione(parziale,k)


    def _ricorsione(self, parziale, k):

        if len(parziale) == k:
            if self.verifica_soluzione_ottima(parziale):
                self._solBest = copy.deepcopy(parziale)

        else:
            for c in self._graph.nodes():
                if self.step_is_valid(parziale, c):
                    parziale.append(c)
                    self._ricorsione(parziale, k)
                    parziale.pop()




    def verifica_soluzione_ottima(self, parziale):
        # Accetta sempre la prima soluzione (quando soluzione_migliore è vuoto)
        if not self._solBest:
            self._scartoBest = self.calcolaScarto(parziale)
            return True

        scarto_parz = self.calcolaScarto(parziale)
        if self._scartoBest > scarto_parz:
            self._scartoBest = scarto_parz
            return True

        return False

    def calcolaScarto(self, lista_costr):
        # Faccio lo scarto come differenza tra pilota piu vecchio e piu giovane nella lista (fino ad ora)
        piu_vecchio = min(lista_costr, key=lambda c: c.oldest_driver_dob)  # dob minima = nato prima
        piu_giovane = max(lista_costr, key=lambda c: c.oldest_driver_dob)  # dob massima = nato dopo

        scarto = (piu_giovane.oldest_driver_dob - piu_vecchio.oldest_driver_dob).days
        return scarto  # numero di giorni di differenza



    def step_is_valid(self, parziale, c):
        if c.oldest_driver_dob is None:  # scarta costruttori senza dati
            return False
        if c in parziale:  # evita duplicati
            return False
        if len(parziale) == 0:
            return True

        # Verifico, per ogni costruttore in parziale, che il costruttore che voglio aggiungere
        # non faccia parte della componente connessa.
        for con in parziale:
            albero = nx.bfs_tree(self._graph, con)
            if c in albero.nodes:
                return False

        return True






