"""test2.py
    Created by Aaron at 07-May-20"""
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
        self.reachabilty = {}

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
    def dfs(self, location, outgoing, traversed):
        if location in traversed:
            return
        traversed.append(location)
        node=self.graph[location]
        node_outgoing=[]
        while node:
            node_outgoing.append(node.location)
            outgoing.append(node.location)
            if node.location in self.reachabilty:
                node_outgoing+=self.reachabilty[node.location]
                outgoing+=self.reachabilty[node.location]
            elif node.location not in traversed:
                node_outgoing+=self.dfs(node.location, outgoing, traversed)
            node=node.next
        self.reachabilty[location]=node_outgoing
        print('a', self.reachabilty)
        return node_outgoing

    # traverse each source
    def traversal(self):
        self.reachabilty={}
        for src, node in self.graph.items():
            outgoing=[]
            traversed=[src]
            while node:
                outgoing.append(node.location)
                if node.location in self.reachabilty:
                    outgoing+=self.reachabilty[node.location]
                else:
                    outgoing+=self.dfs(node.location, outgoing, traversed)
                node=node.next
            self.reachabilty[src]=outgoing
            print('b', self.reachabilty)
        print(self.reachabilty)

def_location=['AU','EG','BE','DK','HK']
def_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
# def_edge=[['AU','EG','12'], ['AU','HK','6'], ['EG','DK','4'], ['DK','BE','1'], ['HK','BE','9']]   #AU go everywhere can detect BE in cycle
def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]     #DK go everywhere can detect BE in cycle
def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all cycle

run = Graph(def_location, def_edge)
run.print_graph()
run.traversal()