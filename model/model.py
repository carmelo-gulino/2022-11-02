import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.playlist = None
        self.genres = DAO.get_all_genres()
        self.durate_min = DAO.get_durate_min()
        self.distinct_playlists = DAO.get_distinct_playlist()
        self.graph = nx.Graph()

    def build_graph(self, genre, d_min, d_max):
        self.graph.clear()
        nodes = DAO.get_tracks(genre, d_min, d_max)
        self.graph.add_nodes_from(nodes)
        n_playlist = DAO.get_n_playlist(genre, d_min, d_max)
        for u in self.graph.nodes:
            for v in self.graph.nodes:
                if u != v:
                    if n_playlist[u.TrackId] == n_playlist[v.TrackId]:
                        self.graph.add_edge(u, v)
        return self.graph

    def get_connesse(self):
        return list(nx.connected_components(self.graph))

    def get_distinct_playlists(self, nodes):
        distinct_playlists = set()
        for n in nodes:
            for p in self.distinct_playlists[n.TrackId]:
                distinct_playlists.add(p)
        return len(distinct_playlists)

    def get_max_connessa(self):
        connesse = nx.connected_components(self.graph)
        sorted_connesse = []
        for c in connesse:
            sorted_connesse.append((c, len(list(c))))
        sorted_connesse.sort(key=lambda x: x[1], reverse=True)
        return sorted_connesse[0][0]

    def get_playlist(self, d_tot):
        connessa = self.get_max_connessa()
        self.playlist = []
        for track in connessa:
            parziale = [track]
            durata_cum = [track.Milliseconds]
            self.ricorsione(parziale, d_tot, connessa, durata_cum)
            parziale.pop()
        return self.playlist

    def ricorsione(self, parziale, d_tot, connessa, durata_cum):
        ultimo = parziale[-1]
        ultima_dur = durata_cum[-1]
        if len(parziale) > len(self.playlist) and ultima_dur < d_tot:
            self.playlist = copy.deepcopy(parziale)
            print(len(parziale), parziale)
        possibili = [n for n in self.graph.neighbors(ultimo) if n in connessa]
        for track in possibili:
            if track not in parziale:
                parziale.append(track)
                durata_cum.append(ultima_dur + track.Milliseconds)
                self.ricorsione(parziale, d_tot, connessa, durata_cum)
                parziale.pop()
                durata_cum.pop()
