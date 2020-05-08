"""CPT212_Asn2_Group7.py
    Created by Aaron at 30-Apr-20"""
from random import seed
from random import  randint
seed(1)

class AdjNode:
    def __init__(self, data, val):
        self.location = data
        self.val=val
        self.next = None

class Graph:
    # construct default graph
    def __init__(self, def_location, def_edge):
        self.graph = {x:None for x in def_location}
        for x in range(len(def_edge)):
            src,des,val=def_edge[x]
            self.add_edge(src,des,int(val))

    # add outgoing edge to the source location
    def add_edge(self, src, des, val):
        node = AdjNode(des, val)           # create node to be inserted
        node.next = self.graph[src]        # set recent added location to be first and its next is the previous
        self.graph[src] = node             # set all outgoing locations to the source location

    # print the graph
    def print_graph(self):
        for src, node in self.graph.items():    #source, locations
            if not node:    #if no outgoing edge, no location
                print('Source {0} :- /'.format(src))
            else:           #if there is outgoing edge, show locations
                str='Source {0} :- '.format(src)
                while node:
                    str+='{0} {1}, '.format(node.location, node.val)
                    node=node.next
                str=str[:len(str)-2]+'/'
                print(str)

    # depth first search of locations
    def dfs(self, location, outgoing, traversed):
        if location in traversed:   #if depth first search before then quit
            return
        node=self.graph[location]
        traversed.append(location)
        while node:                 #depth first search each outgoing locations
            outgoing.append(node.location)      #allow previously traversed node to be added        !!might contain bug
            # print(node.location, outgoing, traversed)
            self.dfs(node.location, outgoing, traversed)
            node=node.next

    # traverse each source
    def traversal(self):
        self.reachable = {}     #store all sources'reachbility in dictionary
        for src, node in self.graph.items():     #source, locations
            outgoing = []       #store this source reachbility in list
            traversed = [src]   #store traversed locations for stopping depth first search
            while node:
                outgoing.append(node.location)
                self.dfs(node.location, outgoing, traversed)    #depth first search
                node = node.next
            self.reachable[src] = outgoing      #store all outgoing locations to this source
            # print(self.reachable)
        print(self.reachable)

    # check if graph is cycle
    def cycle(self):
        self.traversal()        #initiate traversal of the graph
        for src, des in self.reachable.items(): #starting location, reachable locations
            print('cycle', src,des)
            if src in des:            #if any starting location can reach to itself then return True
                return True
        return False                  #if none starting location is reachable to itself then return False

    # check if graph is strongly connected
    def strongly_connected(self):
        self.traversal()        #initiate traversal of the graph
        copy=self.reachable.items()
        for src, des in copy:
            des=set([x for x in des if x!= src])  #use set to eliminate duplicate and if condition to eliminate cycle
            print('con', src, des)
            if len(des)!=len(def_location)-1:     #if any location cannot reach any location then return False
                return False
        return True                             #if all location can reach any location then return True

    #check the distance between 2 nodes
    def shortest_path(self):
        node1 = input("Enter node 1 : ")
        node2 = input("Enter node 2 : ")
        # node does not exists
        if node1 not in self.graph.keys() or node2 not in self.graph.keys():
            print("Node does not exists")
            return False
        else:
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
                print(path)
                print(totalCost)
                return

            # get the neighbours
            neighbour=self.graph.get(cur.location)

            # loop neighbours
            while neighbour!=None:
                # check whether it is in the traversed list
                if neighbour in traversed:
                    continue
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

def_location=['AU','EG','BE','DK','HK']
def_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
# def_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere can detect BE in cycle
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere can detect BE in cycle
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all cycle

run = Graph(def_location, def_edge)
run.print_graph()
# run.traversal()
# print(run.cycle())
# print(run.strongly_connected())
print(run.shortest_path())


