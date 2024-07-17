import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allTeamsOfYear = []
        self._grafo = nx.Graph()
        self._idMapTeams = {}

    def buildGraph(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._allTeamsOfYear)

        #si tratta di un dizionario
        salariesOfTeams = DAO.getSalaryOfTeamOfYear(year, self._idMapTeams)

        # prima creo gli archi e poi agigungo i pesi
        # for t1 in self._allTeamsOfYear:
        #     for t2 in self._allTeamsOfYear:
        #         #DEVO ESCLUDERE IL CASO IN CUI SIA UGUALE
        #         #SÉ STESSO
        #         if t1.ID != t2.ID:
        #             self._grafo.add_edge(t1, t2)

        myedges = list(itertools.combinations(self._allTeamsOfYear, 2))

        self._grafo.add_edges_from(myedges)

        for edge in self._grafo.edges:
            self._grafo[edge[0]][edge[1]]["weight"] = salariesOfTeams[edge[0]] + salariesOfTeams[edge[1]]

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllTeamsOfYear(self, year):
        self._allTeamsOfYear = DAO.getAllTeamsOfYear(year)

        # forma compatta del ciclo
        # self._idMapTeams = {t.ID: t for t in self._allTeamsOfYear}

        for t in self._allTeamsOfYear:
            self._idMapTeams[t.ID] = t
        return self._allTeamsOfYear

    def getSalaryOfTeamPerYear(self, year):
        self._idMap = DAO.getSalaryOfTeamOfYear(year, self._idMapTeams)


    def getSortedNeighbours(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuples = []
        for v in vicini:
            # self._grafo[v0][v]["weight"] -----> per accedere al peso
            viciniTuples.append((v, self._grafo[v0][v]["weight"]))

        viciniTuples.sort(key = lambda x: x[1], reverse=True)
        return viciniTuples