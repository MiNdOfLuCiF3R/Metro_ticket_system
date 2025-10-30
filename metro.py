from metro_oop import Station

class MetroGraph:
    
    def __init__(self, stations, lines):
        self.stations = stations
        self.lines = lines
        self.graph_dict = self._build_graph()

    def _build_graph(self):
        
        graph_dict = {}
        for line in self.lines.values():
            for i in range(len(line.stations)):
                station_name = line.stations[i]
                
                if station_name not in graph_dict:
                    graph_dict[station_name] = set()

                
                if i + 1 < len(line.stations):
                    next_station = line.stations[i+1]
                    graph_dict[station_name].add(next_station)
                   
                    if next_station not in graph_dict:
                         graph_dict[next_station] = set()
                    graph_dict[next_station].add(station_name)
        
       
        return {k: list(v) for k, v in graph_dict.items()}

    def get_shortest_path(self, start, end, path=None):
       
        if path is None:
            path = []
        path = path + [start]

        if start == end:
            return path
        
        if start not in self.graph_dict:
            return None

        shortest_path = None

        for node in self.graph_dict[start]:
            if node not in path:
                new_path = self.get_shortest_path(node, end, path)
                
                if new_path:
                    if shortest_path is None or len(new_path) < len(shortest_path):
                        shortest_path = new_path
        
        return shortest_path
    
    def get_station_lines(self, station_name):
        station = self.stations.get(station_name)
        return station.lines if station else []