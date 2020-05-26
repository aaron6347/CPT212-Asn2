"""test4.py
    Created by Aaron at 26-May-20"""
import heapq
import os

"""node to become a list to store location name, val as value in dictionary"""
class AdjNode:
    """construct node"""
    def __init__(self, data, val):
        self.location = data    # store location name
        self.val = val          # store outgoing value
        self.next = None        # store next node

"""graph to store each vertices as key and its outgoing vertices in a list-like object type as value"""
class Graph:
    """construct default graph"""
    def __init__(self, def_location, def_edge):
        self.graph = { x: None for x in def_location}       # creation of graph/dictionary with default vertices
        for x in range(len(def_edge)):                      # add all default edges
            src, des, val = def_edge[x]                     # creation of nodes with location name, value
            self.addEdge(src, des, int(val))
        self.possible_random = {}                           # to store a dictionary of non-existed edge {source : [destination]} for add random edge purpose
        self.getRandom()                                    # get all other non-existed edges for add random edges purpose

    """add outgoing edge to the source location"""
    def addEdge(self, src, des, val):
        node = AdjNode(des, val)        # create node to be inserted
        node.next = self.graph[src]     # set recent added location to be first and its next is the previous
        self.graph[src] = node          # set all outgoing locations to the source location

    """generate dictionary of all possible endpoints for random edges"""
    def getRandom(self):
        for src, node in self.graph.items():        # find each existed edges in graph
            destination = [x for x in default_location if
                           x is not src]                # compute all vertices and eliminate self as 2nd endpoints(prevent self loop)
            while node:
                destination.remove(node.location)           # eliminate existed 2nd endpoints from the list
                node = node.next
            self.possible_random[src] = destination     # pair up the 1st endpoints with all non-existed 2nd endpoints

    """generate random vertices with random value"""
    def addRandom(self):
        # print('can', self.possible_random)           # to remove
        from random import randint, choice
        src = choice(list(self.possible_random))            # choose 1st endpoint
        des = choice(self.possible_random[src])             # choose 2nd endpoint from 1st endpoint's list
        val = randint(1,20)                                 # random value from 1 to 20
        self.addEdge(src, des, val)                         # add random edges
        self.possible_random[src].remove(des)               # remove the 2nd endpoint from the list of 1st endpoint
        if len(self.possible_random[src]) == 0:             # remove the 1st endpoint if no more 2nd endpoint for it
            del self.possible_random[src]
        print("Newly added edge     {0} -> {1}  ({2})".format(src, des, val))
        # self.printGraph()                       # to remove

    """strongly connected main function"""
    def stronglyConnectedMain(self):
        result = False
        while not result:       # process of repeat checking and adding random edges else show graph
            result = self.checkStronglyConnected()
            if result:              # if graph is strongly connected
                print("The graph is strongly connected. Showing resulted graph.\n")
                self.printGraph()
            else:
                self.addRandom()

    """strongly connected main function"""
    def checkStronglyConnected(self):
        visited = { x: False for x in self.graph.keys()}                # set all vertices as non-visited yet
        self.stronglyConnectedDFS(default_location[0], visited)         # use AU as vertices and start depth first search
        if any(v == False for _,v in visited.items()):                  # check if the AU cannot reach any vertices, then return False
            return False

        """reverse graph direction helper function"""
        def reverseGraph():
            from time import sleep
            reversed_edge=[]
            for location, node in self.graph.items():                       # traverse each vertices
                while node:                                                     # traverse each vertices' outgoing and add the reversed edges
                    reversed_edge.append([node.location, location, -node.val])
                    node = node.next
            return Graph(default_location, reversed_edge)

        reversed_graph = reverseGraph()                                     # create a graph with reversed direction by calling helper function
        visited = { x: False for x in self.graph.keys()}                    # set all vertices as non-visited yet
        reversed_graph.stronglyConnectedDFS(default_location[0], visited)   # use AU as vertices and start depth first search
        if any(v == False for _, v in visited.items()):                     # check if the AU cannot reach any vertices, then return False
            return False
        return True                                                         # else if AU can reach any vertices, then return True

    """strongly connected depth first search function"""
    def stronglyConnectedDFS(self, location, visited):
        visited[location] = True                # set location as visited
        node = self.graph[location]
        while node:                             # check its outgoing location
            if visited[node.location] == False:     # if its outgoing location isn't visited yet, then visit it
                self.stronglyConnectedDFS(node.location, visited)
            node = node.next

    """shortest path using Dijkstra Algorithm"""
    def dijkstraShortestPath(self, src, des):
        vertices = {}
        for i in range(len(default_location)):
            # distance value, current node ,and previous node
            vertices[default_location[i]] = (float('inf'), default_location[i], None)
        vertices[src] = (0, src, None)  # initialize the source node
        reachable_nodes = set(self.dfs(src, []))
        while des not in reachable_nodes:
            self.addRandom()
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
        print(src, 'to', des, '=> Cost: ', vertices[des][0], ' Shortest path: ', path, '\n')

    """depth first search of locations"""
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

    """print the graph"""
    def printGraph(self):
        for src, node in self.graph.items():            # traverse each vertices
            str = 'Source {} :- '.format(src)
            while node:                                 # traverse each outgoing nodes
                str += '{0} {1}, '.format(node.location, node.val)
                node = node.next
            if str[-2] == ",":
                str = str[:len(str) - 2]
            str += ' /'
            print(str)
        print()

"""main body"""
default_location=['AU','EG','BE','DK','HK']
default_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
# default_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere can detect BE in cycle
# default_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere can detect BE in cycle
# default_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all cycle and all strongly connected
run = Graph(default_location, default_edge)
dic={"1":"run.stronglyConnectedMain()", "2":"run.", "3":"run.dijkstraShortestPath", "4":None, "5":"run.printGraph()", "6":"exit()", "help":None}  #store functionality

clear=lambda : os.system('cls')
cmds=["\nCommand list: ",
    "              1            :   Strongly Connected in graph.",
    "              2            :   Cycle in graph.",
    "              3            :   Shortest Path in graph.",
    "              4            :   Reset to default graph.",
    "              5            :   Print the graph structure.",
    "              6            :   Exit.",
    "              help         :   Show commands.\n"]
print("Hi user, this is our CPT 212 Assignment 2: Graph Algorithms".center(120, '_'))
print("\n".join(cmds))
while True:
    query = input("What's your function query?\n")
    clear()
    if query in dic:                    # if query is valid in main menu
        if query != "4":                    # if query is not reset graph
            if query == "3":                    # if query is shortest path and need arguments
                while True:
                    choices = default_location[:]       # copy all locations
                    src = input("\nWhich starting location ? {}\n".format(choices))
                    if src.rstrip() in choices:
                        choices.remove(src)                 # remove selected location to avoid self finding
                        des = input("Which destination location ? {}\n".format(choices))
                        if des.rstrip() in choices:
                            eval(dic[query] + "(src,des)")
                            break
                        else:
                            print("Invalid location.\n")
                            break
                    else:
                        print("Invalid location.\n")
                        break
            elif query == "help":
                print("\n".join(cmds))
            else:
                eval(dic[query])
        else:                           # if query is reset graph
            run = Graph(default_location, default_edge)
            print("The graph has been reset.\n")
    else:
        print("Usage query : number 1-6 .\n")