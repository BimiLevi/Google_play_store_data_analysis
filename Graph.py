from Linked_list import Weighted_linked_list
from collections import deque

class Graph:

    # Complexity time - O(|V|+|E|)
    @staticmethod
    def deserialize(dictionary):
        graph = Graph(dictionary)
        return graph

    # Complexity time - O(|V|+|E|)
    def __init__(self, dictionary):
        self.ll_dict = dictionary
        # First loop - running on all Vertices and creating edges LL for each.
        for vertex in self.ll_dict.keys():
            linked_list = Weighted_linked_list()
            # Second loop - running on all Edges and adding to the relevant LL.
            for edge, weight in dictionary[vertex]:
                linked_list.new_head(edge, weight)
            self.ll_dict[vertex] = linked_list

    def __str__(self):
        graph_as_string = ''
        for vertex in self.ll_dict:
            graph_as_string += str(vertex) + ' -> '
            graph_as_string += self.ll_dict[vertex].__str__() + '\n'
        return graph_as_string



    # Complexity time - O(|V|)
    def get_vertices(self):
        return list(self.ll_dict.keys())

    # Complexity time - O(|V|+|E|)
    def get_edges(self):
        edges = []
        for vertex in self.ll_dict.keys():
            current_node = self.ll_dict[vertex].head
            while current_node is not None:
                if {vertex, current_node.weight, current_node.data} not in edges:
                    edges.append({vertex, current_node.weight, current_node.data})
                current_node = current_node.next
        return edges

    # Complexity time - O(|V|+|E|)
    def get_paths_head(self, num, order_method, start, goal):
        paths = self.BFS(start, goal)
        if paths:
            paths_head = None
            if order_method == 'asc':
                paths_head = paths[0:num]
                return paths_head
            elif order_method == 'desc':
                paths_head = paths[:-num-1:-1]
                return paths_head
            else:
                print('Error')
                return paths_head

    # Complexity time - O(|V|+|E|)
    def BFS(self, start, goal):
        results = []
        if start not in self.get_vertices():
            print("vertex " + start + " doesn't exist in the graph. There are no available paths.")
            return results
        elif goal not in self.get_vertices():
            print("vertex " + goal + " doesn't exist in the graph. There are no available paths.")
            return results
        else:
            x = (start, [start], 0)
            queue = deque()
            queue.append(x)
            while queue:
                (vertex, path, weight) = queue.popleft()
                vertex_edges = self.ll_dict[vertex].linked_list_to_dict()
                for next_vertex in set(vertex_edges.keys()) - set(path):
                    if next_vertex == goal:
                        results.append((path + [next_vertex], round(weight + vertex_edges[next_vertex], 3)))
                    else:
                        queue.append((next_vertex, path + [next_vertex], weight + vertex_edges[next_vertex]))
            if results:
                # sorting the BFS results by: distance, order: asc.
                sorted_paths = sorted(results, key = lambda x: x[1])
                return sorted_paths
            else:
                print("There are no available paths between the start and goal vertices.")
                return results

    # Complexity time - O(|V|+|E|)
    def delete_vertex(self, del_vertex):
        if del_vertex not in self.ll_dict.keys():
            print("Cannot delete the Vertex " + del_vertex + " - It doesn't exist in the Graph.")
        else:
            for vertex in self.ll_dict.keys():              # Deleting the relevant edges
                self.ll_dict[vertex].delete_node(del_vertex)
            del self.ll_dict[del_vertex]                    # Deleting the relevant key

    # Complexity time - O(|V|+|E|)
    def add_vertex_from_dict(self, dictionary):
        if not isinstance(dictionary, dict):
            return 'you need to enter a dictionary if you want to add a vertex'
        # O(|V|)
        for new_vertex in dictionary:
            # 1 case  - the vertex doesnt exist in the graph, needs to add the vertex and it's edges.
            if new_vertex not in self.ll_dict:
                linked_list = Weighted_linked_list()
                # O(E)
                for edge, weight in dictionary[new_vertex]:
                    linked_list.new_head(edge, weight)
                    if edge in self.ll_dict:
                        self.ll_dict[edge].new_head(new_vertex, weight)
                    else:
                        self.ll_dict[edge] = Weighted_linked_list()
                        self.ll_dict[edge].new_head(new_vertex, weight)
                self.ll_dict[new_vertex] = linked_list
            # 2 case  - the vertex is already inside the graph - add the edges
            else:
                # O(E)
                for edge, weight in dictionary[new_vertex]:
                    self.ll_dict[new_vertex].new_head(edge, weight)

    # Complexity time - O(|V|+|E|)
    def shortest_path(self, start, goal):
        paths = self.BFS(start, goal)
        if paths:
            shortest_paths = []
            # case 1 - there is only one path.
            if len(paths) == 1:
                return paths
            # case 2 - there is more then one path vut the shortest one as got the min sum of weights from BFS.
            else:
                minimum = paths[0][1]
                for path in paths:
                    if path[1] < minimum:
                        minimum = path[1]
                for path in paths:
                    if path[1] == minimum:
                        shortest_paths.append(path)
                return shortest_paths
        # case 3 - there is no path
        else:
            return paths

    # Complexity time - O(|V|+|E|)
    def serialize(self):
        graph_hash = self.ll_dict
        for vertex in graph_hash:
            graph_edges = graph_hash[vertex].linked_list_to_list()
            graph_hash[vertex] = graph_edges
        return graph_hash

    # Complexity time - O(|V|+|E|)
    def set_data_visual(self):
        graph_dict = {}
        for vertex in self.ll_dict.keys():
            graph_dict[vertex] = self.ll_dict[vertex].linked_list_to_dict()
        gr = {
            from_: {
                to_: {'weight': w}
                for to_, w in to_nodes.items()
                }
            for from_, to_nodes in graph_dict.items()
            }
        return gr

    def visualise_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        data = self.set_data_visual()

        G = nx.from_dict_of_dicts(data, create_using = nx.Graph)
        G.edges.data('weight')

        plt.figure(figsize = (13, 12), edgecolor = 'b')
        pos = nx.spring_layout(G, scale=4, k = 30)

        node_color = [G.degree(v) for v in G]
        edge_width = [0.1 * G[u][v]['weight'] for u, v in G.edges()]
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx(G, pos, node_color = node_color, node_size = 1500, alpha = 0.85,
                         with_labels = True, width = edge_width,
                         edge_color = '.5', cmap = plt.cm.Blues, font_size = 10)

        nx.draw_networkx_edge_labels(G, pos, edge_labels = labels, font_size = 8, label_pos = 0.3, rotate = False)
        plt.axis('off')
        plt.savefig(' entire graph')
        plt.show()


