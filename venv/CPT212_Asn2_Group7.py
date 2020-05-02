"""CPT212_Asn2_Group7.py
    Created by Aaron at 30-Apr-20"""
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

    # add random edges at random vertices
    def rand_add(self):
        import random
        src, des=random.randit(0, len(def_location)-1), random.randit(0, len(def_location)-1)   #random of endpoints
        val=random.randit(1,20)                                                                 #random value of edge
        self.add_edge(def_location[src], def_location[des], val)

def_location=['AU','EG','BE','DK','HK']
def_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
# def_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere can detect BE in cycle
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere can detect BE in cycle
# def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all cycle

run = Graph(def_location, def_edge)
run.print_graph()
# run.traversal()
print(run.cycle())
print(run.strongly_connected())

