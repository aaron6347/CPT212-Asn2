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

    def print_graph(self):
        for src, node in self.graph.items():
            if not node:
                print('Source {0} :- /'.format(src))
            else:
                str='Source {0} :- '.format(src)
                while node:
                    str+='{0} {1}, '.format(node.location, node.val)
                    node=node.next
                str=str[:len(str)-2]+'/'
                print(str)

def_location=['AU','EG','BE','DK','HK']
def_edge=[['AU','EG','12'], ['AU','HK','6'], ['DK','EG','4'], ['DK','BE','1'], ['HK','BE','9']]
run = Graph(def_location, def_edge)
run.print_graph()
