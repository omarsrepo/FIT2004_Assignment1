from dataclasses import dataclass
import heapq


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
        None. It simply initializes a FloorGraph object with a list of vertices


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

        # Add the keys into the respective vertices
        for key in self.keys:
            key_vertex, time = key
            self.vertices[key_vertex].key_time = time
            self.vertices[key_vertex].contains_key = True

    def climb(self, start: int, exits: list) -> tuple | None:
        """
        This function returns the shortest route from start to one of the exits as a tuple (Shortest time, Path)
        to climb to the next floor. It computes the most optimal route needed to collect a key and then head to
        an exit.

        Approach description: The approach used here is to first calculate the distances to all other vertexes from
        our start point. We then iterate through all the vertexes with keys and compute the time it takes to get to
        the key vertex and also obtain the key.
        From there, we run dijkstras again to compute the distances to all the exits from the key vertex and calculate
        the least time it takes from that key to one of the exits.
        We then compare the least times of all keys-exits to find the best combination of which key to go for and
        which exit to head to. We keep track of the routes taken as well from start to key to exit and finalise
        the best route based on the least time we are able to find.

        The complexity suffers a bit in this method BECAUSE dijkstras has to be run for EACH AND EVERY key and then
        for each and every key we also have to iterate through the list of exits.

        :Input:
        paths: Integer of the vertex id indicating which vertex/location on the floor to start at
        exits: list of integers (vertex ids) of all possible exits

        :Output,return or post condition:
        Tuple (Shortest time, Path) to climb to the next floor.

        :Time complexity:
        ----------------------
        Dijkstra:
        Best case is O(K*|V|) when the graph is spare and has very few edges (1 edge per vertex)
        Worst case is O(K*(|E|+|V|log|V|))
        Where K is the no.of vertices/locations with keys

        :Aux space complexity:
        ----------------------
        valid_exits: Best and worst case is O(|Exits|) where |Exits| is the no.of total exits
        final_route: Worst case is O(|V|) where we would have to traverse every single vertex from start to end

        :return: Tuple (Shortest time, Path) to climb to the next floor.
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
            distances_from_start = self.dijkstra(start)

            vertex_id, key_time = key
            if distances_from_start[vertex_id] is not None:
                time_to_key_room = distances_from_start[vertex_id] + key_time  # Time to get to key and obtain it

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

            memo2 = self.dijkstra(vertex_id)  # Distances from key to all other rooms
            for exit in exits:
                if memo2[exit] is not None:
                    if time_to_key_room + memo2[exit] < total_time:
                        total_time = time_to_key_room + memo2[exit]

                        # Backtrack from exit to the key
                        route2 = []
                        exit_route = Stack()
                        vertex = self.vertices[exit]
                        while True:
                            if vertex.id == key[0]:
                                break
                            exit_route.push(vertex.id)
                            vertex = vertex.previous
                        while exit_route.size() > 0:
                            route2.append(exit_route.pop())

                        final_route = route + route2
                else:
                    if time_to_key_room < total_time:
                        route2 = []
                        total_time = time_to_key_room
                        exit_route = Stack()
                        # Backtrack from exit to the key
                        vertex = self.vertices[exit]

                        while True:
                            if vertex.id == key[0]:
                                break
                            exit_route.push(vertex.id)
                            vertex = vertex.previous

                        while exit_route.size() > 0:
                            route2.append(exit_route.pop())

                        final_route = route + route2

        return total_time, final_route

    def reset_state(self):
        """
        This function simply resets all the class variables of every vertex object that exits.

        :Time complexity:
        ----------------------
        Best and worst case time complexity of O(|V|) where |V| is the total no.of vertices

        :Aux space complexity:
        ----------------------
        Best and worst case is O(1)

        :return: None
        """
        for vertex in self.vertices:
            if vertex is not None:
                vertex.distance = 0
                vertex.previous = None
                vertex.discovered = False
                vertex.visited = False

    def dijkstra(self, source: int) -> list:
        """
        Dijkstra's algorithm which is a modified bfs that accepts as input a vertex id which is where
        we start at and computes the shortest distance to every other vertex from the start/source.

        :Input:
            paths: list of paths and keys represented as a list of tuples
        :Output,return or post condition:
            vertices and edges: unique and sorted list of vertices

        :Time complexity:
        ----------------------
        Best case is O(|V|) when the graph is spare and has very few edges (1 edge per vertex)
        Worst case is O(Section2+Section1) = O(|E|+|V|log|V|)

        :Aux space complexity:
        ----------------------
        distances_from_start: This is an array of length |V|, where |V| is the number of vertices in the graph.
                              It stores the shortest distances from the source vertex to all other vertices.
                              The space complexity for this array is O(|V|).
        discovered: This is a priority queue (implemented as a MinHeap) to keep track of vertices to be explored.
                    The space complexity for the priority queue can be up to O(|V|) in the worst case.

        Best and worst case Auxiliary space complexity is O(|V|) respectively where |V| is the no.of vertices

        :return: List of distances from start to every other vertex
        """
        self.reset_state()
        # Creating a list of distances from start vertex to all other vertexes to act as a look-up table.
        distances_from_start = [None] * len(self.vertices)

        current_vertex = self.vertices[source]

        # Creating a priority queue to decide which discovered vertex to visit next
        discovered = MinHeap()
        discovered.push(current_vertex.id)
        current_vertex.discovered = True
        i = 0

        while discovered.size() > 0:
            """ ---------------------------------Section 1-----------------------------------"""
            # i is a counter which decides what we push into the heap. On the first iteration, we only push the start vertex id
            # From the second iteration onwards, we push the distances of discovered vertices instead. When we pop from the heap
            # we will always be choosing to visit the closest neighboring vertex
            # This section has a time complexity of |V|*log|V|
            if i == 0:
                discovered.pop()
                current_vertex.visited = True
            else:
                u_distance = discovered.pop()
                for vertex in self.vertices:
                    if vertex is not None and not vertex.visited:
                        if vertex.distance == u_distance:
                            current_vertex = vertex
                            current_vertex.visited = True
                            break

            """ Things to note """
            # u = current vertex
            # v = neighboring vertex

            """ ---------------------------------Section 2-----------------------------------"""
            # This section has a time complexity of O(|E|)
            # Now we will look at all the edges that this vertex has in its edges list
            for edge in current_vertex.edges:
                v = self.vertices[edge.v]  # Look at the neighboring vertex
                if not v.discovered:
                    v.discovered = True
                    v.distance = current_vertex.distance + edge.time
                    v.previous = current_vertex
                    discovered.push(v.distance)  # adding the newly discovered neighbouring vertex into the heap based on its distance
                    distances_from_start[v.id] = v.distance  # Updating the distance to this neighbouring vertex from the start vertex
                elif not v.visited:
                    if v.distance > current_vertex.distance + edge.time:
                        # update distance
                        v.distance = current_vertex.distance + edge.time
                        v.previous = current_vertex
                        discovered.push(v.distance)
                        distances_from_start[v.id] = v.distance
            i += 1
        return distances_from_start

    def get_vertices(self, paths: list[tuple]) -> list:
        """
        This function will take in the list of tuples of paths in the graph
        and will return to us a unique list of all the vertices in ascending order

        :Input:
            paths: list of paths represented as a list of tuples(u,v,x)
        :Output,return or postcondition:
            vertices: unique and sorted list of vertices

        :Time complexity:
        ----------------------
        Best and worst case O(|E|+|V|) as we have to iterate through all edges and all vertices

        :Aux space complexity:
        ----------------------
        Best and worst case is O(|V|) as we create a list of all vertices, thus the size is equal to total no.of vertices
        """
        # First we obtain the biggest vertex ID
        greatest_vertex = 0
        for path in paths:  # Iterate through every edge, thus time complexity of O(|E|)
            u, v, x = path
            if u > greatest_vertex:
                greatest_vertex = u
            if v > greatest_vertex:
                greatest_vertex = v
        # Now we create a unique list of vertices in ascending order
        vertices = [None] * (greatest_vertex + 1)
        for i in range(len(vertices)):  # Iterate through every vertex, thus time complexity of O(|V|)
            vertices[i] = Vertex(i)
        return vertices


@dataclass
class Vertex:
    id: int

    def __post_init__(self):
        """
        Class for creating a vertex object

        :Input: None
        :Output,return or post condition: None

        :Time complexity:
        ----------------------
        Best and worst case of O(1)

        :Aux space complexity:
        ----------------------
        Best and worst case of O(1)

        :return: None
        """
        self.edges = []  # This is the adjacency list as we can see every edge for this vertex
        self.distance = 0
        self.key_time = None
        self.contains_key = False

        # for backtracking
        self.previous = None  # Previous vertex that it came from

        # Becomes True when added to the Discovered Queue/Stack
        self.discovered = False
        self.visited = False


@dataclass
class Edge:
    """
    Class for creating Edge object.

    :Input: None
    :Output,return or post condition: None

    :Time complexity:
    ----------------------
    Best and worst case of O(1)

    :Aux space complexity:
    ----------------------
    Best and worst case of O(1)

    :return: None
    """
    u: Vertex
    v: Vertex
    time: int


class MinHeap:
    """
    This is a class for a binary min-heap data structure.

    :Input: None
    :Output,return or post condition: None

    :Time complexity:
    ----------------------
    Best case of O(1) for certain operations and worst case of O(log n) for certain operations

    :Aux space complexity:
    ----------------------
    Best and worst case of O(1)

    :return: None
    """

    def __init__(self):  # O(1)
        self.heap = []

    def push(self, item):  # O(log n)
        heapq.heappush(self.heap, item)

    def pop(self):  # O(log n)
        if self.is_empty():
            raise IndexError("Heap is empty")
        return heapq.heappop(self.heap)

    def peek(self):  # O(1)
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.heap[0]

    def is_empty(self):  # O(1)
        return len(self.heap) == 0

    def size(self):  # O(1)
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
    """
    This is a class for a Stack ADT.

    :Input: None
    :Output,return or post condition: Stack object

    :Time complexity:
    ----------------------
    Best and worst case of O(1) for all operations

    :Aux space complexity:
    ----------------------
    Best and worst case of O(1)

    :return: None
    """

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
    keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    graph = FloorGraph(paths, keys)

    # Modified Dijkstra (change GRAPH.VERTICES to SELF.VERTICES)
    distances_from_start = [None] * len(graph.vertices)
    exits = [2, 4, 7]
    source = 1  # Source input
    current_vertex = graph.vertices[source]

    discovered = MinHeap()
    discovered.push(current_vertex.id)
    current_vertex.discovered = True

    initial_route = [current_vertex.id]

    best_time = float('inf')
    temp = float('inf')
    time_with_key = float('inf')
    time_without_key = 0

    i = 0

    while discovered.size() > 0:
        if i == 0:
            discovered.pop()
            current_vertex.visited = True
        else:
            u_distance = discovered.pop()
            for vertex in graph.vertices:
                if vertex is not None and not vertex.visited:
                    if vertex.distance == u_distance:
                        current_vertex = vertex
                        current_vertex.visited = True
                        break

        for edge in current_vertex.edges:  # (1,5,2), (1,7,4), (1,2,2)
            v = graph.vertices[edge.v]  # Look at the neighboring vertex
            if not v.discovered:
                v.discovered = True
                v.distance = current_vertex.distance + edge.time
                v.previous = current_vertex
                discovered.push(v.distance)  # adding the newly discovered neighbouring vertex into the heap based on its distance
                distances_from_start[v.id] = v.distance  # Updating the distance to this neighbouring vertex from the start vertex

                if v.contains_key and time_with_key > v.distance + v.key_time:
                    time_with_key = v.distance + v.key_time
                    key_room = v.id
                if v.id in exits:
                    while True:
                        for edge in graph.vertices[key_room].edges:
                            if edge.v == v.id:
                                time_with_key += edge.time
                                break
                            else:
                                key_room = graph.vertices[edge.v].id
                        best_time = time_with_key
                        break

            elif not v.visited:
                if v.distance > current_vertex.distance + edge.time:
                    # update distance
                    v.distance = current_vertex.distance + edge.time
                    v.previous = current_vertex
                    discovered.push(v.distance)
                    distances_from_start[v.id] = v.distance
            #
            # v = graph.vertices[edge.v]
            # route = [current_vertex.id]
            # if edge.v in exits:
            #     if graph.vertices[edge.v].key_time + edge.time < temp:
            #         best_time = graph.vertices[edge.v].key_time + edge.time
            #         temp = best_time  # Store the best time found so far
            #     else:
            #         temp = best_time
            # elif graph.vertices[edge.v].contains_key:
            #     time_with_key += edge.time + graph.vertices[edge.v].key_time
            #     time_without_key += edge.time
            #     best_time = time_with_key
            # else:
            #     graph.vertices[edge.v].distance = 0



    # print(graph.vertices)
    # for vertex in graph.vertices:
    #     if vertex is not None:
    #         print(f"{vertex}: {vertex.edges}")

    # distance_from_start = graph.dijkstra(1)
    # print(f"distances_from_{1}: {distance_from_start}\n")

    # key_heap = MinHeap()
    # for key in keys:
    #     key_heap.push(key[0])

    # print(f"keys are at {key_heap.heap}\n")
    # for key in key_heap.heap:
    #     print(f"key at {key} takes {graph.vertices[key].key_time} mins")

    # total = float('inf')
    # key_to_go_for = None
    # while key_heap.size() > 0:
    #     vertex_id = key_heap.pop()
    #     if distance_from_start[vertex_id] is not None:
    #         if total > distance_from_start[vertex_id] + graph.vertices[vertex_id].key_time:
    #             total = distance_from_start[vertex_id] + graph.vertices[vertex_id].key_time
    #             key_to_go_for = vertex_id
    #
    # print(total, key_to_go_for)

    """
    Climb function logic:
    ---------------------
    climb(start: int, exits: list)
    
    start  = 1 --> Vertex(1)
    distances_from_start = self.dijkstra(start) 
    
    distances_from_start = [17, None, 2, 5, 6, 2, 7, 4, 6]
    total_time = float('inf')
    final_route = []
    
    ------------------------------------ITERATE THROUGH EVERY KEY------------------------------------
            REMEMBER THAT --> distances_from_start = [17, None, 2, 5, 6, 2, 7, 4, 6]
    
    for key in keys:  # keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
        vertex, time = key
        if distances_from_start[vertex] is not None:
            time = distances_from_start[vertex] + self.vertices.key_time  # Time to get to key and obtain it
            
    """
