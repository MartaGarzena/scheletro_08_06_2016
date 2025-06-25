from itertools import combinations
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._listRacesIdYear = []
        self._listYears = DAO.getYears()

    def getYears(self):
        return self._listYears

    def buildGraph(self, anno):
        self._listRacesIdYear = DAO.getRacesofYear(anno)
        self._graph.add_nodes_from(self._listRacesIdYear)
        self.addEdges()

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def addEdges(self):
        for id1, id2 in combinations(self._graph.nodes, 2):
            archi = DAO.getEdges(id1, id2)
            if archi[0] > 0:
                self._graph.add_edge(id1, id2, weight=archi[0])

    def getArcoMax(self):
        peso_massimo = float('-inf')
        archi_massimi = []

        for u, v, data in self._graph.edges(data=True):
            weight = data['weight']
            if weight > peso_massimo:
                peso_massimo = weight
                archi_massimi = [(u, v, weight)]
            elif weight == peso_massimo:
                archi_massimi.append((u, v, weight))

        return archi_massimi

    def getGare(self):
        return self._graph.nodes()


    def simulazioneGara(sef, raceId, probabilita, tempoProb):
        tempi, piloti, numero_giri = DAO.getDatiRace(raceId)
        # tempi[driverId][lap] → accesso rapido al tempo
        # piloti → lista dei partecipanti
        # #numero_giri → per sapere quanti giri simulare

        tempo_totale = {d: 0 for d in piloti}
        punti = {d: 0 for d in piloti}
        print("model, pre inzio")

        for lap in range(1, numero_giri + 1):
            print(f"{lap}")
            giro_corrente = {}
            # Dizionario temporaneo che memorizza il tempo totale accumulato da ciascun pilota dopo aver completato questo giro.
            # Serve per sapere chi è stato il più veloce al termine del giro attuale.
            for driver in piloti:
                print(f"{driver}")
                t = tempi[driver].get(lap, None) #recupera il tempi[driver][lap], se non lo ha NONE
                if t is None:
                    continue  # Il pilota non ha completato questo giro
                # Simula pit stop
                if random.random() < probabilita:
                    t += tempoProb * 1000  # aggiungi T secondi in millisecondi

                tempo_totale[driver] += t
                giro_corrente[driver] = tempo_totale[driver]

            # Trova il pilota più veloce in questo giro
            print("fine cerca, ora migliore")
            if giro_corrente: #Controlla che ci siano dati nel giro attuale (cioè che almeno un pilota abbia completato il giro).
                leader = min(giro_corrente, key=giro_corrente.get) # contiene il tempo totale di ogni pilota dopo questo giro.
                punti[leader] += 1

        return punti

        # --- Mostra classifica finale ---
        print("Classifica finale per punti (leader di giro):")
        for driver, score in sorted(punti.items(), key=lambda x: x[1], reverse=True):
            print(f"Pilota {driver}: {score} punti")

 
