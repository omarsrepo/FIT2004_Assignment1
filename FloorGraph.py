from dataclasses import dataclass
import heapq
import networkx as nx
import matplotlib.pyplot as plt


@dataclass
class FloorGraph:
    paths: list = None  # List of vertices --> paths = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
    keys: list = None  # List of keys for each given vertex keys = [(0, 5), (3, 2), (1, 3)]

    def __post_init__(self):
        """
        Creates two class variables -> self.edges and self.vertices
        Populates self.edges with all the edges of the graph
        Populates self.vertices with all the vertices of the graph

        :Input:
            paths: list of paths and keys represented as a list of tuples
        :Output,return or post condition:
            vertices and edges: unique and sorted list of vertices

        Time complexity: Best and worst case O(|E|)
        :Aux space complexity: Best and worst case O(|V| + |E|)
        :return:
        """
        if self.paths is None and self.keys is None:
            return None

        # Create a list of all the edges
        # Complexity of O(E) because it iterates through all the edges
        # self.edges = []
        # for path in self.paths:
        #     self.edges.append(Edge(path[0], path[1], path[2]))

        # Create a list of all the vertices and populate the edges list for each vertex
        # Complexity of O(E+E) = O(E) because get_vertices iterates through all the edges,
        # and we also iterate through the edges to populate the edge list for every vertex
        self.vertices: list = self.get_vertices(self.paths)
        for edge in self.paths:
            u, v, w = edge
            self.vertices[u].edges.append(Edge(u, v, w))

    def climb(self, start: int, exits: list) -> tuple | None:
        """
        This function returns the shortest route from start to one of the exits as a tuple (Shortest time, Path)
        to climb to the next floor. It computes the most optimal route needed to collect a key and then head to
        an exit.

        :param start: Starting location (integer)
        :param exits: Possible exit points (list of exits)
        :return: tuple (Shortest time, Path)
        """
        # Check if we can even get to the exits from the start
        distances_from_start = self.dijkstra(start)
        valid_exits = []
        for exit in exits:
            distance_to_exit = distances_from_start[exit]
            if distance_to_exit is not None:
                valid_exits.append(exit)
            elif exit == start:
                valid_exits.append(exit)
        if not valid_exits:
            return None

        total_time = float('inf')
        final_route = []
        for key in self.keys:  # keys = [(0,5),(3,2),(1,3)]
            self.reset_state()
            memo = self.dijkstra(start)

            vertex_id, key_time = key
            if memo[vertex_id] is not None:
                time_to_key_room = memo[vertex_id] + key_time  # Time to get to key and obtain it

                # Back track from key to start
                route = []
                route.insert(0, vertex_id)
                vertex = self.vertices[vertex_id]
                while True:
                    if vertex.id == start:
                        break
                    route.insert(0, vertex.previous.id)
                    vertex = vertex.previous
            else:
                time_to_key_room = key_time  # Time to get to key and obtain it

                # Back track from key to start
                route = []
                route.insert(0, vertex_id)
                vertex = self.vertices[vertex_id]
                while True:
                    if vertex.id == start:
                        break
                    route.insert(0, vertex.previous.id)
                    vertex = vertex.previous

            self.reset_state()
            memo2 = self.dijkstra(vertex_id)  # Distances from key to all other rooms
            # print(f"Distances from key {vertex_id} to all other rooms: {memo2}")

            for exit in exits:
                if memo2[exit] is not None:
                    if time_to_key_room + memo2[exit] < total_time:
                        route2 = []
                        total_time = time_to_key_room + memo2[exit]
                        exit_route = Stack()
                        # Backtrack from exit to the key
                        vertex = self.vertices[exit]
                        # print(f"Hey I am here right now {vertex} with a route so far of {route}")
                        while True:
                            if vertex.id == key[0]:
                                break
                            exit_route.push(vertex.id)
                            vertex = vertex.previous

                        while exit_route.size() > 0:
                            route2.append(exit_route.pop())

                        # print(f"From key at {myfloor.vertices[key[0]].id} to exit {exit}:", total_time, route + route2, "\n")
                        final_route = route + route2
                else:
                    if time_to_key_room < total_time:
                        route2 = []
                        total_time = time_to_key_room
                        exit_route = Stack()
                        # Backtrack from exit to the key
                        vertex = self.vertices[exit]
                        # print(f"Hey I am here right now {vertex} with a route so far of {route}")
                        while True:
                            if vertex.id == key[0]:
                                break
                            exit_route.push(vertex.id)
                            vertex = vertex.previous

                        while exit_route.size() > 0:
                            route2.append(exit_route.pop())

                        # print(f"From key at {myfloor.vertices[key[0]].id} to exit {exit}:", total_time, route + route2, "\n")
                        final_route = route + route2

        self.reset_state()
        return total_time, final_route

    def reset_state(self):
        for vertex in self.vertices:
            if vertex is not None:
                vertex.distance = 0
                vertex.previous = None
                vertex.discovered = False
                vertex.visited = False

    def dijkstra(self, source: int):
        """
        Dijkstra's algorithm which is a modified bfs that accepts as input a vertex id which is where
        we start at and computes the shortest distance to every other vertex from the start/source.

        :param source: Vertex
        :return:
        """
        # Creating a list
        memo = [None] * len(self.vertices)
        start = self.vertices[source]
        start.distance = 0

        discovered = MinHeap()
        discovered.push(start.id)
        start.discovered = True
        i = 0
        while discovered.size() > 0:
            # From the heap/array, pop the vertex, and now it is visited so update the visited
            # Once the vertex has been visited, it
            if i == 0:
                u = self.vertices[discovered.pop()]
                u.visited = True
            else:
                u_distance = discovered.pop()
                for vertex in self.vertices:
                    if vertex is not None:
                        if not vertex.visited:
                            if vertex.distance == u_distance:
                                u = vertex
                                u.visited = True
                                break

            # Now we will look at all the edges that this vertex (u) has in its edges list
            for edge in u.edges:
                # print(f"distance of vertex{u.id} is {u.distance}")
                v = self.vertices[edge.v]  # Look at the neighboring vertex
                if not v.discovered:
                    v.discovered = True
                    v.distance = u.distance + edge.time
                    v.previous = u
                    discovered.push(v.distance)
                    memo[v.id] = v.distance
                elif not v.visited:
                    if v.distance > u.distance + edge.time:
                        # update distance
                        v.distance = u.distance + edge.time
                        v.previous = u
                        discovered.push(v.distance)
                        memo[v.id] = v.distance

            i += 1
        return memo

    def get_vertices(self, paths: list[tuple]) -> list:
        """
        This function will take in the list of tuples of paths in the graph
        and will return to us a unique list of all the vertices in ascending order
        :Input:
            paths: list of paths represented as a list of tuples(u,v,x)
        :Output,return or postcondition:
            vertices: unique and sorted list of vertices
        Time complexity: Best and worst case O(E)
        :Aux space complexity: Best and worst case O(V)
        """
        # First we obtain the biggest vertex ID
        greatest_vertex = 0
        for path in paths:  # Worst case time complexity of O(E)
            u, v, x = path
            if u > greatest_vertex:
                greatest_vertex = u
            if v > greatest_vertex:
                greatest_vertex = v
        # Now we create a unique list of vertices in ascending order
        vertices = [None] * (greatest_vertex + 1)
        for i in range(len(paths)):  # Worst case time complexity of O(E)
            u, v, x = paths[i]
            vertices[u] = Vertex(u)
            vertices[v] = Vertex(v)
        return vertices

    # Tester function
    def draw_graph(self):
        """
        Visualize the graph using networkx and matplotlib.
        """
        G = nx.Graph()
        # Add nodes
        for vertex in self.vertices:
            G.add_node(vertex)
        # Add edges
        for edge in self.edges:
            G.add_edge(edge.u, edge.v, weight=edge.time)
        # Draw the graph
        pos = nx.spring_layout(G)  # You can change the layout algorithm as needed
        nx.draw(G, pos, with_labels=True, node_size=500, font_size=10, node_color='lightblue')
        # Draw edges with arrows
        edge_labels = {(edge.u, edge.v): edge.time for edge in self.edges}  # Optional edge labels
        nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), connectionstyle="arc3, rad=0.2", arrowsize=20)
        # Draw node labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=10)
        # Draw edge labels (optional)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.title("Graph Visualization")
        plt.show()  #


@dataclass
class Vertex:
    id: int

    def __post_init__(self):
        self.edges = []  # This is the adjacency list as we can see every edge for this vertex
        self.distance = 0

        # for backtracking
        self.previous = None  # Previous vertex that it came from

        # Becomes True when added to the Discovered Queue/Stack
        self.discovered = False
        self.visited = False


@dataclass
class Edge:
    u: Vertex
    v: Vertex
    time: int


class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Heap is empty")
        return heapq.heappop(self.heap)

    def peek(self):
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def print_heap(self):
        if self.is_empty():
            print("Heap is empty")
            return

        def visualize(index, indent=""):
            if index < len(self.heap):
                print(indent + str(self.heap[index]))
                left_child = 2 * index + 1
                right_child = 2 * index + 2
                if left_child < len(self.heap):
                    visualize(left_child, indent + "  |__ ")
                if right_child < len(self.heap):
                    visualize(right_child, indent + "  |__ ")

        visualize(0)


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Stack is empty")

    def size(self):
        return len(self.items)


if __name__ == "__main__":
    # The paths and keys represented as a list of tuples
    paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2), (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4),
             (7, 8, 2), (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    keys = [(0, 5), (3, 2), (1, 3)]
    graph = FloorGraph(paths, keys)
    start = 3
    exits = [3]

    for vertex in graph.vertices:
        print(f"{vertex}: {vertex.edges}")
