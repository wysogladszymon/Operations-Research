from typing import Any, Dict, List,  Set, Tuple

node = int

class Graph:
  def __init__(self, dic: Dict[node, List[Tuple]]):
    if not isinstance(dic, dict):
        raise ValueError('Wrong data!')
    self.graph = dic

  def nodes(self) -> List[node]:
    return [x for x in self.graph.keys()]
  
  def dfs(self, n : node):
    self.visited = []
    self.__visitNode(n)
    return self.visited

  def __visitNode(self,n : node):
    self.visited.append(n)
    for u in self.graph[n]:
      if u[0] not in self.visited:
        self.__visitNode(u[0])
    return 

  def iscyclic(self):
    for i in self.graph:
       result = self.__search(i[0])
       if result:
           return True
    return False
  
  def __search(self, n: node, path: Set=None):
    if path is None:
        path = set()
    
    for neighbour in self.graph[n]:
        if neighbour[0] in path:
            return True 
        else:
            path.add(neighbour[0])
            result = self.__search(neighbour[0], path)
            path.remove(neighbour[0])
            if result:
                return True 
    return False 
  
  def isconnected(self):
    for i in self.graph:
      if len(self.dfs(i)) == len(self.graph.keys()):
        return True
    return False
  
  def __getitem__(self, index:int) -> Any:
     return self.graph[index]

  def __str__(self):
     return self.graph.__str__()