from typing import Dict, List,  Set

type node = int

class Graph:
  def __init__(self, dic: Dict[node, List[node]]):
    if not isinstance(dic, dict):
        raise ValueError('Wrong data!')
    self.graph = dic

  def dfs(self, n : node):
    self.visited = []
    self.__visitNode(n)
    return self.visited

  def __visitNode(self,n : node):
    self.visited.append(n)
    for u in self.graph[n]:
      if u not in self.visited:
        self.__visitNode(u)
    return 

  def iscyclic(self):
    for i in self.graph:
       result = self.__search(i)
       if result:
           return True
    return False
  
  def __search(self, n: node, path: Set=None):
    if path is None:
        path = set()
    
    for neighbour in self.graph[n]:
        if neighbour in path:
            return True 
        else:
            path.add(neighbour)
            result = self.__search(neighbour, path)
            path.remove(neighbour)
            if result:
                return True 
    return False 
  
  def isconnected(self):
    for i in self.graph:
      if len(self.dfs(i)) == len(self.graph.keys()):
        return True
    return False
  

  def __str__(self):
     return self.graph.__str__()