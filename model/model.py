import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapIdC = {}


    def getAllYears(self):
        anni = DAO.getAllYears()
        return anni

    def buildGrafo(self, anno1, anno2):
        self._graph.clear()
        nodes = DAO.getAllNodes(anno1,anno2)
        self._graph.add_nodes_from(nodes)
        self.addEdges(anno1,anno2)

    def addEdges(self, anno1, anno2):

        self.buildIdMap()
        edges = DAO.getAllEdges(self._idMapIdC, anno1,anno2)
        for e in edges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)

    def buildIdMap(self):
        for n in self._graph.nodes:
            self._idMapIdC[n.constructorId] = n

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
        # Ordino in ordine decrecente (reverse = True) gli archi in base al peso
        archi_ordinati = sorted(self._graph.edges(data = True), key = lambda x: x[2]["weight"], reverse = True)
        primiTreArchi = []
        for i in range(0, 3):
            primiTreArchi.append(archi_ordinati[i])
        return primiTreArchi


    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)


