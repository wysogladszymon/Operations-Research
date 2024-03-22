
import pygame
import numpy as np
from typing import List

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
  def __init__(self, row, col, width, total_rows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.color = WHITE
    self.neighbors = []
    self.width = width
    self.total_rows = total_rows
    self.heuristic = float('inf')
    self.distance = float('inf')
    
    
  def get_pos(self):
    return self.row, self.col
  
  def draw(self, window):
    pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
  
  def get_color(self):
    return self.color
  
  def reset(self):
    self.color = WHITE
    
  def make_start(self):
    self.color = ORANGE
    
  def make_end(self):
    self.color = TURQUOISE
  
  def make_visited(self):
    self.color = RED
  
  def make_path(self):
    self.color = PURPLE
    
  def make_pending(self):
    self.color = GREEN
    
  def make_barrier(self):
    self.color = BLACK

  def is_barrier(self):
    return self.color == BLACK
  
  def is_start(self):
    return self.color == ORANGE
    
  def is_end(self):
    return self.color == TURQUOISE
  
  def is_visited(self):
    return self.color == RED  
    
  def is_pending(self):
    return self.color == GREEN 
  
  def is_blank(self):
    return self.color == WHITE
  
  def update_neighbors(self, grid):
    self.neighbors = []
    # top neighbors 
    if self.row > 0:
      mid = grid[self.row - 1][self.col]
      if mid.is_blank() or mid.is_end() or mid.is_pending():
        self.neighbors.append(mid)
      if self.col > 0:
        left = grid[self.row - 1][self.col - 1]
        if left.is_blank() or left.is_end() or left.is_pending():
          self.neighbors.append(left)
      if self.col < self.total_rows - 1:
        right = grid[self.row - 1][self.col + 1]
        if right.is_blank() or right.is_end() or right.is_pending():
          self.neighbors.append(right)
    # bottom neighbors
    if self.row < self.total_rows - 1:
      mid = grid[self.row + 1][self.col]
      if mid.is_blank() or mid.is_end() or mid.is_pending():
        self.neighbors.append(mid)
      if self.col > 0:
        left = grid[self.row + 1][self.col - 1]
        if left.is_blank() or left.is_end() or left.is_pending():
          self.neighbors.append(left)
      if self.col < self.total_rows - 1:
        right = grid[self.row + 1][self.col + 1]
        if right.is_blank() or right.is_end() or right.is_pending():
          self.neighbors.append(right)
    # left neighbor
    if self.col > 0:
      left = grid[self.row][self.col - 1]
      if left.is_blank() or left.is_end() or left.is_pending():
        self.neighbors.append(left)
    # right neighbor
    if self.col < self.total_rows - 1:
      right = grid[self.row][self.col + 1]
      if right.is_blank() or right.is_end() or right.is_pending():
        self.neighbors.append(right)
    return self.neighbors
  
  def getPath(self, grid):  
    neighbors = []
    # top neighbors 
    if self.row > 0:
      mid = grid[self.row - 1][self.col]
      if mid.is_visited() or mid.is_start() :
        neighbors.append(mid)
      if self.col > 0:
        left = grid[self.row - 1][self.col - 1]
        if left.is_visited() or left.is_start() :
          neighbors.append(left)
      if self.col < self.total_rows - 1:
        right = grid[self.row - 1][self.col + 1]
        if right.is_visited() or right.is_start() :
          neighbors.append(right)
    # bottom neighbors
    if self.row < self.total_rows - 1:
      mid = grid[self.row + 1][self.col]
      if mid.is_visited() or mid.is_start() :
        neighbors.append(mid)
      if self.col > 0:
        left = grid[self.row + 1][self.col - 1]
        if left.is_visited() or left.is_start() :
          neighbors.append(left)
      if self.col < self.total_rows - 1:
        right = grid[self.row + 1][self.col + 1]
        if right.is_visited() or right.is_start() :
          neighbors.append(right)
    # left neighbor
    if self.col > 0:
      left = grid[self.row][self.col - 1]
      if left.is_visited() or left.is_start() :
        neighbors.append(left)
    # right neighbor
    if self.col < self.total_rows - 1:
      right = grid[self.row][self.col + 1]
      if right.is_visited() or right.is_start() :
        neighbors.append(right)
    return neighbors  
  
  def __str__(self):
    return f"({self.row}, {self.col})"
  
  def __repr__(self):
    return f"({self.row}, {self.col})"
        
  
def h(node : Node, nodeEnd : Node):
  return np.sqrt((node.col - nodeEnd.col)**2 + (node.row - nodeEnd.row)**2) - 1

def d(node : Node, nodeEnd : Node):
  return np.sqrt((node.col - nodeEnd.col)**2 + (node.row - nodeEnd.row)**2)

def draw_grid(win, rows, width):
  gap = width // rows
  l = [i * gap for i in range(rows)]
  for i in l:
    pygame.draw.line(win, GREY, (i, 0), (i, width))
    pygame.draw.line(win, GREY, (0, i), (width, i))
  
  start = None
  end = None
  
def mousePos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()
 

def Astar(draw, start : Node, end : Node, grid):
  start.distance = 0
  pending = set() 
  node = start
  while node != end:
    neighbors : List[Node] = node.update_neighbors(grid) # pobieramy nieodwiedzonych sąsiadów
    for neighbor in neighbors:
      newDistance = node.distance + d(node, neighbor) #dla każdego sąsiada jego odległość od początku
      if newDistance < neighbor.distance: # zabezpieczenie, jeżeli był już pending
        # natępuje tu wpisanie odległości od startu i szacowanej odległości do końca, oraz dodanie do pending
        neighbor.distance = newDistance
        neighbor.heuristic = h(neighbor, end)
        pending.add(neighbor)
        #graficzne oznaczenie, że jest pending
        if neighbor != end:
          neighbor.make_pending()
      #narysowanie zmian, nieistotne z kwestii algorytmu
      draw()
    #kolejne oznaczenie dla grafiki, że sąsiedzi węzła zostali odwiedzeni (Czerwony kolor)
    if node != start:
      node.make_visited()

    #poszukiwanie minimum funkcji f = g + h
    min = float('inf')
    newNode = None
    minHeuristic = float('inf')
    for p in pending:
      newHeuristic = p.heuristic
      newDistance = newHeuristic + p.distance
      #jezeli znajdziemy minimum, to je przechowujemy
      if newDistance < min:
        min = newDistance
        newNode = p
        minHeuristic = newHeuristic
      # charakteryzowanie, żeby najpierw szukał węzła o mniejszej heurystyce, w przypadku gdy odległości są równe,
      # ponieważ ona szacuje koszt dotarcia   
      elif newDistance == min and newHeuristic < minHeuristic:
        min = newDistance
        newNode = p
        minHeuristic = newHeuristic
    #jeżeli nie ma już węzłów do odwiedzenia, to kończymy
    if newNode is None:
      return float('inf'), []
      
    pending.remove(newNode)
    node = newNode

  # część druga, rysowanie ścieżki i zwrot wyniku
  res = node.distance
  draw()
  
  # draw path
  path = [end]
  # pomysł - iteracyjnie prszechodzimy od końca, po wierzchołkach, które zostały odwiedzone 
  # i dodajemy do ścieżki te z minimalnym dystansem do startu
  while node != start:
    neighbors : List[Node] = node.getPath(grid)
    min = float('inf')
    p = None
    # szukamy minimum, do którego przejdziemy w następnym kroku
    for neighbor in neighbors:
      if neighbor.distance < min:
        min = neighbor.distance
        p = neighbor
    if p is None:
      break
    node = p
    if node != start:
      node.make_path()
    path.append(node)
  #zwróć długość ścieżki i ścieżkę
  return res, path[::-1]

def main():
  repeat = True
  while repeat:
    repeat = False
    WIDTH = 800
    rows = 50
    WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Pathfinding algorithm")
    grid = np.zeros((rows, rows), dtype=Node)
    for i in range(rows):
      for j in range(rows):
        grid[i][j] = Node(i, j, WIDTH // rows, rows)
    start = False
    end = False
    run = True
    while run:
      draw(WINDOW, grid, rows, WIDTH)
      # if x was clicked quit the game
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False

        # if left mouse button was clicked
        if pygame.mouse.get_pressed()[0]:
          pos = pygame.mouse.get_pos()
          row, col = mousePos(pos, rows, WIDTH)
          node : Node = grid[row][col]
          # if we dont have start yet, set start
          if not start and node != end:
            start = node
            start.make_start()
          # if we dont have end yet, set end
          elif not end and node != start:
            end = node
            end.make_end()
          #if node is not start and not end, make it a barrier
          elif node != end and node != start:
            node.make_barrier()

        # if right mouse button was clicked - reset the node
        if pygame.mouse.get_pressed()[2]:
          pos = pygame.mouse.get_pos()
          row, col = mousePos(pos, rows, WIDTH)
          node : Node = grid[row][col]
          node.reset()
          if node == start:
            start = None
          elif node == end:
            end = None

        # if space was clicked, run the algorithm
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and start and end:
          length, path = Astar(lambda: draw(WINDOW, grid, rows, WIDTH), start, end, grid)
          if length == float('inf'):
            print("Nie znaleziono ścieżki")
            pygame.display.set_caption("Nie znaleziono ścieżki")
            break
          print("Najkrótsza ścieżka ma długość: ", "{:.2f}".format(length))
          print("Ścieżka: ", path)
          pygame.display.set_caption("Najkrótsza ścieżka ma długość: {:.2f}".format(length))
    pygame.quit()
if __name__ == '__main__':
  main()