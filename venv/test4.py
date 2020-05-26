"""test3.py
    Created by Aaron at 08-May-20"""
from pprint import pprint as pp
import heapq


# node to become a list to store location name, val as value in dictionary
class AdjNode:
    def __init__(self, data, val):
        self.location = data  # store location name
        self.val = val  # store outgoing value
        self.next = None  # store next node


# graph to store each vertices as key and its outgoing vertices in a list-like object type as value
class Graph:
    # construct default graph
    def __init__(self, def_location, def_edge):
        self.graph = {x: None for x in def_location}  # creation of graph/dictionary with default vertices
        for x in range(len(def_edge)):  # add all default edges
            src, des, val = def_edge[x]  # creation of nodes with location name, value
            self.add_edge(src, des, int(val))
        self.getrandom()  # generate dictionary of all possible endpoints for random edges
        # self.changes=False

    # add outgoing edge to the source location
    def add_edge(self, src, des, val):
        node = AdjNode(des, val)  # create node to be inserted
        node.next = self.graph[src]  # set recent added location to be first and its next is the previous
        self.graph[src] = node  # set all outgoing locations to the source location

    # print the graph
    def print_graph(self):
        for src, node in self.graph.items():  # source, locations
            if not node:  # if no outgoing edge, no location
                print('Source {0} :- /'.format(src))
            else:  # if there is outgoing edge, show locations
                str = 'Source {0} :- '.format(src)
                while node:
                    str += '{0} {1}, '.format(node.location, node.val)
                    node = node.next
                str = str[:len(str) - 2] + '/'
                print(str)

    # depth first search of locations
    def dfs(self, src, visited):
        visited.append(src)  # insert this location as visited
        node = self.graph[src]  # get location's outgoing node
        outgoing = []  # to store location's outgoing location0
        if not node:  # small improvement to save 1 call of dfs for location that has no outgoing edge at all
            return []
        while node:  # if location has outgoing node
            outgoing.append(node.location)  # store this outgoing node
            if node.location not in visited:  # else if location that hasn't haven't fully dfs and havent visit before yet
                outgoing += self.dfs(node.location, visited)  # dfs
            node = node.next
        return outgoing

    # check cycle graph
    def check_cycle(self):
        print('cycle')
        cycle = False
        while True:
            self.traversal()  # traversal vertices to get each reachability
            result = []
            for src, node in self.reachabilty.items():  # check all vertices
                if src in node:  # if location is in its reachability
                    result.append((src, self.reachabilty[src]))
                    print(src, 'yes cycle')  # to remove
                    cycle = True
                    break
                else:  # to remove
                    cycle = False
            if cycle == False:  # if cycle check is false, then add edges and continue check
                self.add_random()
                # break                              #to remove
            else:  # else if cycle check is true, then print result
                pp(result)
                break

    # check strongly connected graph
    def check_strongly(self):
        print('connec')
        strongly = True
        while True:
            self.traversal()  # traversal vertices to get each reachability
            result = []
            for src, node in self.reachabilty.items():  # check all vertices
                node = set([x for x in node if x is not src])  # use set to eliminate duplication and self
                if len(node) == len(
                        def_location) - 1:  # if total of reachbility is same as number of vertices except self
                    result.append((src, node))
                    strongly = True
                else:  # else if total of reachbility is not same as number of vertices except self
                    print(src, '1st no strongly')  # to remove
                    strongly = False
                    break
            if strongly == False:  # if strongly connected check is false, then add edges and continue check
                self.add_random()
                # break                           # to remove
            else:  # else if stronlgy connected check is true, then print result
                pp(result)
                break

    # generate random vertices with random value
    def add_random(self):
        # print('can', self.can_random)  # to remove
        from random import randint, choice
        src = choice(list(self.can_random))  # find 1st endpoint
        des = choice(self.can_random[src])  # find 2nd endpoint
        # print(src, des)  # to remove
        self.add_edge(src, des, randint(1, 20))  # add random edges
        self.can_random[src].remove(des)  # remove the 2nd endpoint from the list of 1st endpoint
        if len(self.can_random[src]) == 0:  # remove the 1st endpoint if no more 2nd endpoint for it
            del self.can_random[src]
        # self.print_graph()

    # generate dictionary of all possible endpoints for random edges
    def getrandom(self):
        self.can_random = {}  # to compile a dictionary of 1st endpoints and 2nd endpoints from the list
        for src, node in self.graph.items():  # find each edges existed in graph
            des_random = [x for x in def_location if
                          x is not src]  # compute all vertices and eliminate self as 2nd endpoints(prevent self loop)
            while node:
                des_random.remove(node.location)  # eliminate existed 2nd endpoints from the list
                node = node.next
            self.can_random[src] = des_random  # pair up the 1st endpoints with all non-existed 2nd endpoints

    # shortest path using Dijkstra Algorithm
    def dijkstra_shortest_path(self, src, des):
        vertices = {}
        for i in range(len(def_location)):
            # distance value, current node ,and previous node
            vertices[def_location[i]] = (float('inf'), def_location[i], None)

        vertices[src] = (0, src, None)  # initialize the source node

        reachable_nodes = set(self.dfs(src, []))

        while des not in reachable_nodes:
            self.add_random()
            reachable_nodes = set(self.dfs(src, []))

        dict_heap = []
        # Create a min heap of the vertices dictionary based on the distance value
        heapq.heappush(dict_heap, vertices[src])
        for j in vertices:
            if vertices[j][1] in reachable_nodes:
                heapq.heappush(dict_heap, vertices[j])

        visited = []  # List to store visited nodes

        path = []  # The shortest path
        while len(dict_heap) != 0:
            u = heapq.heappop(dict_heap)  # Get the minimum distance value node from the heap and remove it

            if u[1] in visited:  # Skip the redundant visited nodes in Queue
                continue

            visited.append(u[1])  # Store the current node into the list

            # nodes_list = [i for i in def_location if i != u[1]]  # Get list of nodes other than itself
            node = self.graph[u[1]]  # Get the adjacent nodes from the current nodes

            while node:
                if u[0] + node.val < vertices[node.location][0]:
                    # Convert tuple to list to update value and revert back
                    temp_list = list(vertices[node.location])
                    temp_list[0] = u[0] + node.val
                    temp_list[2] = u[1]
                    vertices[node.location] = tuple(temp_list)
                    heapq.heappush(dict_heap, vertices[node.location])
                node = node.next

        current_node = des
        while current_node != src:
            current_cost = vertices[current_node][0] - vertices[vertices[current_node][2]][0]
            path.insert(0, (vertices[current_node][2], current_node, current_cost))
            current_node = vertices[current_node][2]

        print(src, 'to', des, '=> Cost: ', vertices[des][0], ' Shortest path: ', path)


def_location = ['AU', 'EG', 'BE', 'DK', 'HK']
def_edge = [['AU', 'EG', '12'], ['AU', 'HK', '6'], ['DK', 'EG', '4'], ['DK', 'BE', '1'], ['HK', 'BE', '9'],
            ['AU', 'DK', '6']]
# def_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all have cycle

run = Graph(def_location, def_edge)
# run.print_graph()
# run.check_cycle()
# run.check_strongly()
run.dijkstra_shortest_path('AU', 'EG')
# run.print_graph()
