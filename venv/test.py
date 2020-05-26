"""test.py
    Created by Aaron at 01-May-20"""
dict1={'AU', 'EU', 'HK'}
dict2={'AU'}
dict3={'HK','EU', 'AU'}
print(dict1==dict2)
print(dict1==dict3)

import random

def_edge=[['EG','AU','12'], ['AU','HK','6'], ['DK','EG','4'], ['BE','DK','1'], ['HK','BE','9']]     #BE go everywhere then all cycle


while True:
    query = input("What's your function query?\n")
    if query.isnumeric() and 0 < int(query) < 7:
        print('yes')

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