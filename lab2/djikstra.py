from graph import Graph
# Graph jest postaci Dictionary node -> List[(neighbor, weigth)]

def djikstra(g: Graph, s=0):
  nodes = g.nodes()
  # ustaweienie odległości na nieskończoność i wierzchołka poprzedzającego na -1
  distance = {x : (None, float("inf")) for x in nodes} 
  distance[s] = None, 0
  # g[s] to lista sąsiadów wraz z wagami wierzchołka s
  unvisited = set(nodes)
  u = s

  while unvisited:
    # odwiedzamy wierzchołek u
    unvisited.remove(u)
    #sprawdzamy wszystkich jego sąsiadów
    for neighbor, weight in g[u]:
      # tylko jeżeli nie byli odwiedzeni wcześniej
      if neighbor in unvisited:
        newDistance = distance[u][1] + weight
        # jeżeli nowa droga jest krótsza niż wcześniejsza najkrótsza to ja zaktualizuj  
        if newDistance < distance[neighbor][1]:
          distance[neighbor] = u, newDistance
    # jeżeli algorytm będzie trwał dalej, to wybierz najbliższy nieodwiedzony wierzchołek
    if unvisited:
      u = min(unvisited, key=lambda node: distance[node][1])
      
  return distance
      
  



  
  