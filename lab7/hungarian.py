import numpy as np

#step 1 O(n^2)
def reduceArray(arr : np.array):
  """
  Ta funkcja znajduje minimum w kazdym wierszu i odejmuje je od wszystkich elementów w wierszu,
  następnie robi to samo dla każdej z kolumn
  """
  reducedArr = arr[:]
  totalReduction = 0
  for row in reducedArr:
    minimum = min(row)
    row -= minimum
    totalReduction += minimum

  for col in reducedArr.T:
    minimum = min(col)
    col -= minimum
    totalReduction += minimum
  return reducedArr, totalReduction

def step1(arr : np.array):
  print("step1")
  """
  Redukcja macierzy
  """
  reducedArr, totalReduction = reduceArray(arr)
  return reducedArr, totalReduction

#step 2 O(n^2)
def findIndependentZeros(reducedArr : np.array):
  """
  znajduje niezależne zera po kolei 
  """
  rowsWithZeros = []
  colsWithZeros = []
  independentZeros = []
  for i, row in enumerate(reducedArr):
    for j, element in enumerate(row):
      if element == 0 and not (i in rowsWithZeros or j in colsWithZeros):
        independentZeros.append((i,j))
        rowsWithZeros.append(i)
        colsWithZeros.append(j)
  return independentZeros

def step2(reducedArr : np.array):
  print("step2")
  """
  Poszukiwanie niezależnych zer
  """
  independentZeros = findIndependentZeros(reducedArr)
  return independentZeros

#step 3 O(n)
def coverColumnsWithZeros(independentZeros : list, reducedArr : np.array):
  """
  ta funkcja 'wykresla' kolumny zawierające zera niezależne, 
  0 -> zaznaczona, 1 -> niezaznaczona
  """
  covered = np.ones(reducedArr.shape)
  for _, zeroX in independentZeros:
    covered[:, zeroX] = 0 #oznaczenie kolumny jako zaznaczoną 
  return covered


def step3(independentZeros : list, reducedArr : np.array):
  print("step3")
  """
  Wykreslanie kolumn zawierających zera niezależne
  """
  covered = coverColumnsWithZeros(independentZeros, reducedArr)
  if len(independentZeros) < reducedArr.shape[0]:
    return 4, covered
  return 0, independentZeros


def findUncoveredZeros(covered : np.array, reducedArr : np.array):
  """
  Znajduje zera niezakryte / zależne
  """
  uncoveredZeros = []
  for i, row in enumerate(reducedArr):
    for j, element in enumerate(row):
      if element == 0 and covered[i,j] == 1:
        uncoveredZeros.append((i,j))
  return uncoveredZeros

# funkcje pomocnicze znajdujące zera w zbiorze (zer zależnych lub niezależnych)
def findZeroInRow(zeroSet : np.array, row : int):
  for zero in zeroSet:
    if zero[0] == row:
      return zero
  return None

def findZeroInCol(zeroSet : np.array, col : int):
  for zero in zeroSet:
    if zero[1] == col:
      return zero
  return None

#step 4 O(n^2)
def step4(covered : np.array, reducedArr : np.array, independentZeros : list):
  print("step4")
  dependentZeros = findUncoveredZeros(covered, reducedArr)
  for zero in dependentZeros:
    zeroInRow = findZeroInRow(independentZeros, zero[0])
    if not zeroInRow:
      return 5, zero
    else:
      covered[:, zeroInRow[1]] = 1  #uncover column
      covered[zero[0], :] = 0       #cover row
  return 4, covered

    
def step5(z0 : tuple, independentZeros : list, dependentZeros : list):
  print("step5")
  Z1 = findZeroInCol(independentZeros, z0[1]) #zero niezależne w kolumnie
  dependentZeros.remove(z0)
  independentZeros.append(z0)
  while Z1:
    Z2 = findZeroInRow(dependentZeros, Z1[0]) #zero zależne w wierszu
    independentZeros.remove(Z1)
    dependentZeros.append(Z1)
    if not Z2:
      break
    Z1 = findZeroInCol(independentZeros, Z2[1]) #zero niezależne w kolumnie
  return 3, independentZeros
  
  
def findMinimumUncovered(arr : np.array, covered : np.array):
  """
  Finds minimum uncovered element
  """
  minimum = np.inf
  for i, row in enumerate(arr):
    for j, element in enumerate(row):
      if covered[i,j] == 1 and element < minimum:
        minimum = element
  return minimum

def step6(arr : np.array, covered : np.array, totalReduction : int):
  """
  Step 6 of the Hungarian Algorithm
  """
  print("step6")
  minimum = findMinimumUncovered(arr, covered)
  for i, row in enumerate(arr):
    for j, element in enumerate(row):
      if covered[i,j] == 1: # odejmujemy minimum od elementów nieprzykrytych
        arr[i,j] -= minimum
      elif covered[i,j] == 0 and element != 0: # dodajemy minimum do elementów pokrytych, nie 0
        arr[i,j] += minimum
  totalReduction += minimum
  return arr, totalReduction



def hungarian(arr : np.array):
  """
  Hungarian Algorithm
  """
  # algorytm wykonuje pierwsze dwa kroki, czyli redukcję macierzy i poszukiwanie zer niezależnych
  reducedArr, totalReduction = step1(arr)
  independentZeros = step2(reducedArr)
  step = 3
  while step != 0:
    #następnie zakrywa kolumny zawierające zera niezależne 
    #dopóki krok nie stanie sie 0 co znaczy ze mamy rozwiazanie
    step, covered = step3(independentZeros, reducedArr)
    if step == 0:
      return independentZeros, totalReduction
    #funkcja znajduje zera zależne
    dependentZeros = findUncoveredZeros(covered, reducedArr)
    # i pętla wykonuje się dopóki są zera nieprzykryte
    while dependentZeros:
      # krok 4 znajduje zera zależne 
      # i zwraca krok 5 jeśli znajdzie zero zależne, posiadające w wierszu zero niezależne, 
      # w przeciwnym wypadku zwraca krok 4 lub 6
      step, z0orCovered = step4(covered, reducedArr, independentZeros)
      
      if step == 5:
        step, independentZeros = step5(z0orCovered, independentZeros, dependentZeros)
        #po kroku 5 zawsze następuje weryfikacja pokrycia w kroku 3
        step, covered =  step3(independentZeros, reducedArr)
        # jeżeli krok 3 zwrócił 0 to znaczy że mamy rozwiązanie
        if step == 0:
          return independentZeros, totalReduction
      dependentZeros = findUncoveredZeros(covered, reducedArr)
      # jezeli pętla się skończyła -> tzn. że nie ma już zera nieprzykrytego,
      # szukamy minimum i odpowiednio zmniejszamy lub zwiększamy wartości w macierzy 
    reducedArr, totalReduction = step6(reducedArr, covered, totalReduction)
  return independentZeros, totalReduction
  
  
    
def tests():
  #data i data1 to przykłady z wykładu, i obydwa rozwiązania się pokrywają
  
  data = np.array([[5,2,3,2,7], [6,8,4,2,5],[6,4,3,7,2], [6,9,0,4,0], [4,1,2,4,0]])
  print(hungarian(data))
  
  data2 = np.array([[1,2,3], [2,4,6], [3,6,9]])
  print(hungarian(data2))
  
if __name__ == "__main__":
  tests()