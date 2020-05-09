"""test3.py
    Created by Aaron at 08-May-20"""
from pprint import pprint as pp
# node to become a list to store location name, val as value in dictionary
class AdjNode:
    def __init__(self, data, val):
        self.location = data        #store location name
        self.val=val                #store outgoing value
        self.next = None            #store next node

# graph to store each vertices as key and its outgoing vertices in a list-like object type as value
class Graph:
    # construct default graph
    def __init__(self, def_location, def_edge):
        self.graph = {x:None for x in def_location}     #creation of graph/dictionary with default vertices
        for x in range(len(def_edge)):                  #add all default edges
            src,des,val=def_edge[x]                         #creation of nodes with location name, value
            self.add_edge(src,des,int(val))
        self.getrandom()                                #generate dictionary of all possible endpoints for random edges
        # self.changes=False

    # add outgoing edge to the source location
    def add_edge(self, src, des, val):
        node = AdjNode(des, val)           # create node to be inserted
        node.next = self.graph[src]        # set recent added location to be first and its next is the previous
        self.graph[src] = node             # set all outgoing locations to the source location

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
        visited.append(src)     #insert this location as visited
        node=self.graph[src]    #get location's outgoing node
        outgoing=[]             #to store location's outgoing location0
        if not node:            #small improvement to save 1 call of dfs for location that has no outgoing edge at all
            self.reachabilty[src]=[]
            return []
        while node:             #if location has outgoing node
            outgoing.append(node.location)                  #store this outgoing node
            if node.location in self.reachabilty:           #memoization, if location that has fully dfs before
                outgoing+=self.reachabilty[node.location]
            elif node.location not in visited:              #else if location that hasn't haven't fully dfs and havent visit before yet
                outgoing+=self.dfs(node.location, visited)      #dfs
            node=node.next
        return outgoing

    # traverse each vertices
    def traversal(self):
        self.reachabilty={}
        self.changes=True
        for src, node in self.graph.items():            #traverse all vertices
            if src not in self.reachabilty:             #some location with no outgoing edge will be created during dfs in small improvement part
                self.reachabilty[src]=self.dfs(src,[])  #store all vertices' reachability
        print(self.reachabilty)            #to remove

    #check cycle graph
    def check_cycle(self):
        print('cycle')
        cycle=False
        while True:
            self.traversal()                            # traversal vertices to get each reachability
            result=[]
            for src, node in self.reachabilty.items():  #check all vertices
                if src in node:                             #if location is in its reachability
                    result.append((src, self.reachabilty[src]))
                    print(src, 'yes cycle')          #to remove
                    cycle=True
                    break
                else:                               #to remove
                    cycle=False
            if cycle==False:                            #if cycle check is false, then add edges and continue check
                self.add_random()
                # break                              #to remove
            else:                                       #else if cycle check is true, then print result
                pp(result)
                break

    # check strongly connected graph
    def check_strongly(self):
        print('connec')
        strongly=True
        while True:
            self.traversal()                            # traversal vertices to get each reachability
            result = []
            for src, node in self.reachabilty.items():  #check all vertices
                node=set([x for x in node if x is not src])     #use set to eliminate duplication and self
                if len(node)==len(def_location)-1:              #if total of reachbility is same as number of vertices except self
                    result.append((src, node))
                    strongly=True
                else:                                           #else if total of reachbility is not same as number of vertices except self
                    print(src, '1st no strongly')   #to remove
                    strongly=False
                    break
            if strongly==False:                         #if strongly connected check is false, then add edges and continue check
                self.add_random()
                # break                           # to remove
            else:                                       #else if stronlgy connected check is true, then print result
                pp(result)
                break

    #check the distance between 2 nodes
    def shortest_path(self):
        node1 = input("Enter node 1 : ")
        node2 = input("Enter node 2 : ")
        # node does not exists
        if node1 not in self.graph.keys() or node2 not in self.graph.keys():
            print("Node does not exists")
            return False
        else:
            self.traversal()
            self.getrandom()
            while node2 not in self.reachabilty.get(node1):
                self.add_random()
                self.traversal()
            #run best first search algo
            self.bestFirstSearch(node1, node2)
            return True

    # prints a list of edges
    def printQueue(self, queue):
        for x in queue:
            print(x.location + "  " + str(x.val))

    # algorithm of best first search
    def bestFirstSearch(self, node1, goal):
        # two list are created
        priority_queue = []
        traversed = []

        # create a node for the src and append it to the priority queue
        src=AdjNode(node1,0)
        priority_queue.append(src)

        # the priority queue is not empty
        while priority_queue:
            # sort the queue using their edges cost
            priority_queue.sort(key=lambda node:node.val)
            cur=priority_queue.pop(0)
            traversed.append(cur)

            # if current points towards the goal node, path is the nodes traversed to reach the destination
            if cur.location==goal:
                path=[]
                totalCost=0

                # backtrack occurs and it goes back to the src node
                while cur.location!=src.location:
                    path.insert(0, cur.location)
                    totalCost=totalCost+cur.val
                    cond=False

                    # s represents the key and nodes represent the linked list of tuples
                    for s,node in self.graph.items():
                        while node:
                            if node==cur:
                                cond=True
                                temp=s
                                break
                            else:
                                node=node.next
                        if cond:
                            break
                    for x in traversed:
                        if x.location==temp:
                            cur=x
                            break;
                path.insert(0, src.location)
                self.printQueue(traversed)
                print(path)
                print(totalCost)
                return

            # get the neighbours
            neighbour=self.graph.get(cur.location)

            # loop neighbours
            while neighbour!=None:
                # check whether it is in the traversed list
                if neighbour in traversed:
                    neighbour=neighbour.next
                else:
                    #create a node for the neighbour
                    child = AdjNode(neighbour.location, cur.val + neighbour.val)
                    # check whether it is in the priority queue
                    if self.add_to_pq(priority_queue,neighbour):
                        priority_queue.append(neighbour)
                    neighbour=neighbour.next

        # the goal node is not connected to the src node
        print("Node Not Found")
        return

    # check to see whether the node should be added to pq or not
    def add_to_pq(self,pq,neighbour):
        for node in pq:
            if neighbour==node:
                return False
        return True

    # generate random vertices with random value
    def add_random(self):
        print('can', self.can_random)                           #to remove
        from random import randint, choice
        src=choice(list(self.can_random))                                #find 1st endpoint
        des=choice(self.can_random[src])                                 #find 2nd endpoint
        print(src, des)                             #to remove
        self.add_edge(src, des, randint(1,20))                      #add random edges
        self.can_random[src].remove(des)                                 #remove the 2nd endpoint from the list of 1st endpoint
        if len(self.can_random[src]) ==0:                                #remove the 1st endpoint if no more 2nd endpoint for it
            del self.can_random[src]
        self.print_graph()

    # generate dictionary of all possible endpoints for random edges
    def getrandom(self):
        self.can_random = {}                                # to compile a dictionary of 1st endpoints and 2nd endpoints from the list
        for src, node in self.graph.items():                # find each edges existed in graph
            des_random = [x for x in def_location if x is not src]  # compute all vertices and eliminate self as 2nd endpoints(prevent self loop)
            while node:
                des_random.remove(node.location)                        # eliminate existed 2nd endpoints from the list
                node = node.next
            self.can_random[src] = des_random                       # pair up the 1st endpoints with all non-existed 2nd endpoints

def_location=['AU','EG','BE','DK','HK']
def_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
# def_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all have cycle

run = Graph(def_location, def_edge)
run.print_graph()
# run.check_cycle()
# run.check_strongly()
run.shortest_path()
