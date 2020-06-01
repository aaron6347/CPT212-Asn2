"""test4.py
    Created by Aaron at 26-May-20"""
import heapq
import os

class AdjNode:
    """node to become a list to store location name, val as value in dictionary"""
    def __init__(self, data, val):
        """construct node"""
        self.location = data    # store location name
        self.val = val          # store outgoing value
        self.next = None        # store next node

class Graph:
    """graph to store each vertices as key and its outgoing vertices in a list-like object type as value"""
    def __init__(self, def_location, def_edge):
        """construct default graph"""
        self.graph = { x: None for x in def_location}       # creation of graph/dictionary with default vertices
        for x in range(len(def_edge)):                      # add all default edges
            src, des, val = def_edge[x]                     # creation of nodes with location name, value
            self.addEdge(src, des, int(val))
        self.possible_random = {}                           # to store a dictionary of non-existed edge {source : [destination]} for add random edge purpose
        self.getRandom()                                    # get all other non-existed edges for add random edges purpose

    def addEdge(self, src, des, val):
        """add outgoing edge to the source location"""
        node = AdjNode(des, val)        # create node to be inserted
        node.next = self.graph[src]     # set recent added location to be first and its next is the previous
        self.graph[src] = node          # set all outgoing locations to the source location

    def getRandom(self):
        """generate dictionary of all possible endpoints for random edges"""
        for src, node in self.graph.items():        # find each existed edges in graph
            destination = [x for x in default_location if
                           x is not src]                # compute all vertices and eliminate self as 2nd endpoints(prevent self loop)
            while node:
                destination.remove(node.location)           # eliminate existed 2nd endpoints from the list
                node = node.next
            self.possible_random[src] = destination     # pair up the 1st endpoints with all non-existed 2nd endpoints

    def addRandom(self):
        """generate random vertices with random value"""
        from random import randint, choice
        src = choice(list(self.possible_random))            # choose 1st endpoint
        des = choice(self.possible_random[src])             # choose 2nd endpoint from 1st endpoint's list
        val = randint(1,20)                                 # random value from 1 to 20
        self.addEdge(src, des, val)                         # add random edges
        self.possible_random[src].remove(des)               # remove the 2nd endpoint from the list of 1st endpoint
        if len(self.possible_random[src]) == 0:             # remove the 1st endpoint if no more 2nd endpoint for it
            del self.possible_random[src]
        print("Newly added edge     {0} -> {1}  ({2})".format(src, des, val))

    def cycleMain(self):
        """main function for cycle checking"""
        result = False
        print("1. Check one node \n2. Check all nodes")     # choose to either check cycle for one node or all nodes
        choice = input("Select an option : ")
        while choice != "1" and choice != "2":
            print("Invalid input. Please try again")
            choice = input("Select an option : ")

        if choice == "1":
            src = input("Enter a node :")
            while src not in self.graph.keys():
                print("Invalid input. Please try again")
                src = input("Enter a node :")

        while not result:
            if choice == "1":                               # user checks a single node
                result = self.checkCycle(src)
                if not result:
                    self.addRandom()
                else:
                    print(src + " has a cycle. The following is the graph")
                    self.printGraph()
            elif choice == "2":                             # user checks all node
                for src, node in self.graph.items():
                    if not result:
                        result = self.checkCycle(src)
                    else:
                        temp = self.checkCycle(src)
                if not result:
                    self.addRandom()
                else:
                    print("The following is the graph")
                    self.printGraph()

    def checkCycle(self, src):
        """uses dfs to check for a cycle, if cycle exists, return true, else return false"""
        cycle = False
        outgoing = []
        outgoing = self.dfs(src, outgoing)
        if src in outgoing:                                 # the src node is in the resultant visited list
            outgoing.insert(0, src)
            print("Node " + src + " has a cycle.")
            print(outgoing)
            cycle = True
        return cycle

    def stronglyConnectedMain(self):
        """strongly connected main function"""
        result = False
        while not result:       # process of repeat checking and adding random edges else show graph
            result = self.checkStronglyConnected()
            if result:              # if graph is strongly connected
                print("The graph is strongly connected. Showing resulted graph.\n")
                self.printGraph()
            else:
                self.addRandom()

    def checkStronglyConnected(self):
        """strongly connected main function"""
        visited = { x: False for x in self.graph.keys()}                # set all vertices as non-visited yet
        self.stronglyConnectedDFS(default_location[0], visited)         # use AU as vertices and start depth first search
        if any(v == False for _,v in visited.items()):                  # check if the AU cannot reach any vertices, then return False
            return False

        def reverseGraph():
            """reverse graph direction helper function"""
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

    def stronglyConnectedDFS(self, location, visited):
        """strongly connected depth first search function"""
        visited[location] = True                # set location as visited
        node = self.graph[location]
        while node:                             # check its outgoing location
            if visited[node.location] == False:     # if its outgoing location isn't visited yet, then visit it
                self.stronglyConnectedDFS(node.location, visited)
            node = node.next

    def dijkstraShortestPath(self, src, des):
        """shortest path using Dijkstra Algorithm"""
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

    def dfs(self, src, visited):
        """depth first search of locations"""
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

    def printGraph(self):
        """print the graph"""
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


def reset(default_location, default_edge):
    """reset function"""
    return Graph(default_location, default_edge)

def printcmd():
    """print commands function"""
    cmds = ["\nCommand list: ",
            "              1            :   Strong Connectivity of the graph.",
            "              2            :   Cycle Detection in the graph.",
            "              3            :   Find Shortest Path in the graph.",
            "              4            :   Reset to the default graph.",
            "              5            :   Print the graph structure.",
            "              6            :   Exit.",
            "              help         :   Show commands.\n"]
    print("\n".join(cmds))

clear = lambda : os.system('cls')

"""main body"""
# default vertices and edges
default_location = ['AU', 'EG', 'BE', 'DK', 'HK']
default_edge = [['AU', 'EG', '12'], ['AU', 'HK', '6'], ['DK', 'EG', '4'], ['DK', 'BE', '1'], ['HK', 'BE', '9']]
#store functionality
dic = {"1":"run.stronglyConnectedMain()", "2":"run.cycleMain()", "3":"run.dijkstraShortestPath", "4":"reset(default_location, default_edge)", "5":"run.printGraph()", "6":"exit()", "help":"printcmd()"}
print("Hi user, this is our CPT 212 Assignment 2: Graph Algorithms".center(120, '_'))
printcmd()
# first graph
run = reset(default_location, default_edge)
while True:
    query = input("What's your function query?\n")
    clear()
    if query in dic:                    # if query is valid in main menu
        if query == "3":                    # if query is shortest path and need arguments
            while True:
                choices = default_location[:]       # copy all locations
                src = input("\nWhich starting location ? {}\n".format(choices)).strip()
                if src in choices:
                    choices.remove(src)                 # remove selected location to avoid self finding
                    des = input("Which destination location ? {}\n".format(choices)).strip()
                    if des in choices:
                        eval(dic[query] + "(src,des)")
                        break
                    else:
                        print("Invalid location.\n")
                        break
                else:
                    print("Invalid location.\n")
                    break
        elif query == "4":              # if query is resetting graph and expect to return a graph
            run = eval(dic[query])
            print("The graph has been reset.\n")
        else:
            eval(dic[query])
    else:
        print("Usage query : number 1-6 or 'help' for commands.\n")