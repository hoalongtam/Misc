from Tkinter import *
import random

def get_num(msg):
  while True:
    response = raw_input(msg).strip()
    try: return int(response)
    except ValueError: pass

def get_resp(msg, legal):
  msg = msg % "/".join(legal)
  while True:
    response = raw_input(msg).strip().lower()
    if response in legal: return response

class GraphicSort(object):
  def __init__(self):
    self.size = get_num("How many elements should I sort? ")
    order = get_resp("How sorted should it start out [%s]? ",
                     ["random", "sorted", "reverse", "mostly"])
    self.init_data(order)
    self.actions = []

  def init_data(self, order):
    self.data = range(1,self.size+1)
    if order == "sorted": return
    elif order == "reverse": self.data.reverse()
    elif order == "random": random.shuffle(self.data)
    else:
      for i in xrange(self.size/5):
        j, k = random.randrange(self.size), random.randrange(self.size)
        self.data[j], self.data[k] = self.data[k], self.data[j]

  def draw(self):
    self.window = Tk()
    self.window.resizable(0,0)
    self.canvas = Canvas(self.window, width=self.size*2, height=self.size*2,
                         bg="white")
    self.canvas.pack()
    for x, y in enumerate(self.data):
      if self.dots:
        self.canvas.create_rectangle(2*x, 2*(self.size-y), 2*(x+1),
                                     2*(self.size-y+1), fill="black", tag=y)
      else:
        self.canvas.create_rectangle(2*x, 2*(self.size), 2*(x+1),
                                     2*(self.size-y+1), fill="black", tag=y)
    
  dots = False
  def update(self):
    for x, y in enumerate(self.data):
      if self.dots:
        self.canvas.coords(y, (2*x, 2*(self.size-y), 2*(x+1), 2*(self.size-y+1)))
      else:
        self.canvas.coords(y, (2*x, 2*(self.size), 2*(x+1), 2*(self.size-y+1)))
    self.canvas.update()

  compares = 0
  swaps = 0

  def compare(self, a, b, array):
    self.actions.append(("compare", a, b))
    self.compares += 1
    return array[a].__cmp__(array[b])

  def swap(self, x, y, array):
    self.swaps += 1
    array[x], array[y] = array[y], array[x]
    self.actions.append(("swap", x, y))

  def sort(self):
    ## selection sort
    cp = self.data[:]
    for i in xrange(len(cp)):
      m = cp[i]
      for j in xrange(i,len(cp)):
        if self.compare(j, m, cp) < 0: m = j
      self.swap(i, m, cp)

  redSlots = []

  def makeRed(self, alpha, beta):
    a, b = self.data[alpha], self.data[beta]
    for slot in self.redSlots:
      self.canvas.itemconfig(slot, fill="black", outline="black")
    self.redSlots = [a, b]
    self.canvas.itemconfig(a, fill="red", outline="red")
    self.canvas.itemconfig(b, fill="blue", outline="blue")
    self.canvas.update()
    
  def animate(self, index = 0):
    if index >= len(self.actions): return
    a, x, y = self.actions[index]
    if a == "swap":
      self.data[x], self.data[y] = self.data[y], self.data[x]
      self.update()
    elif a == "compare":
      self.makeRed(x, y)
    self.window.after(1, self.animate, index+1)

class GraphicInsert(GraphicSort):
  def sort(self):
    cp = self.data[:]
    for i in xrange(1, len(cp)):
      j = i
      while j > 0:
        if self.compare(j, j-1, cp) < 0:
          self.swap(j, j-1, cp)
        else: break
        j -= 1

class GraphicBubble(GraphicSort):
  def sort(self):
    cp = self.data[:]
    n = len(cp)
    while n > 1:
      newn = 0
      for i in xrange(n-1):
        if self.compare(i, i+1, cp) > 0:
          self.swap(i, i+1, cp)
          newn = i+1
      n = newn

class GraphicHeap(GraphicSort):
  def sort(self):
    cp = self.data[:]
    def heapify():
      i = len(cp)/2
      while i >= 0:
        bubbleDown(i, len(cp))
        i -= 1
    def bubbleDown(start, length):
      while start < length:
        left = start*2 + 1
        maximum = start
        if left < length:
          if self.compare(left, start, cp) > 0: maximum = left
          right = start*2 + 2
          if right < length:
            if self.compare(right, maximum, cp) > 0: maximum = right
        if start != maximum:
          self.swap(start, maximum, cp)
        else: break
        start = maximum
    heapify()
    for i in xrange(len(cp), 0, -1):
      self.swap(0, i-1, cp)
      bubbleDown(0, i-1)


class GraphicQuick(GraphicSort):
  def sort(self):
    cp = self.data[:]
    def partition(start, end):
      cp2 = sorted(cp[start:end])
      pivot = cp2[len(cp2)/2]
      for i in xrange(start, end):
        if cp[i] == pivot:
          pivot = i
          break
      self.swap(start, pivot, cp)
      i = start
      for j in xrange(start, end):
        if self.compare(start, j, cp) > 0:
          i += 1
          self.swap(i, j, cp)
      self.swap(i, start, cp)
      return i
    def qsort(p, q):
      if p < q:
        r = partition(p, q)
        qsort(p, r)
        qsort(r+1, q)
    qsort(0, len(cp))

class GraphicShell(GraphicSort):
  def sort(self):
    cp = self.data[:]
    gap = len(cp) / 2
    while gap > 0:
      for i in xrange(gap, len(cp)):
        j = i
        while j >= gap and self.compare(j - gap, j, cp) > 0:
          self.swap(j, j-gap, cp)
          j -= gap
      gap /= 2


class GraphicShaker(GraphicSort):
  def sort(self):
    a = self.data[:]
    i = 0
    k = len(a) - 1
    while i < k:
      min = i
      max = i
      for j in xrange(i+1, k+1):
        if self.compare(j, min, a) < 0: min = j
        if self.compare(j, max, a) > 0: max = j
      self.swap(i, min, a)
      if max == i: self.swap(min, k, a)
      else: self.swap(max, k, a)
      i += 1
      k -= 1

class GraphicMerge(GraphicSort):
  def sort(self):
    A = self.data[:]
    def lower(start, end, val):
      length = end - start
      while length > 0:
        half = length / 2
        mid = start + half
        if (self.compare(mid, val, A) < 0):
          start = mid + 1
          length = length - half - 1
        else: length = half
      return start

    def upper(start, end, val):
      length = end - start
      while length > 0:
        half = length / 2
        mid = start + half
        if self.compare(val, mid, A) < 0:
          length = half
        else:
          start = mid + 1
          length = length - half - 1
      return start

    def insert_sort(start, end):
      if end > start + 1:
        for i in xrange(start+1, end):
          for j in xrange(i, start, -1):
            if self.compare(j, j - 1, A) < 0:
              self.swap(j, j - 1, A)
            else: break
    
    def gcd(m, n):
      while n: m, n = n, m % n
      return m

    def reverse(start, end):
      while start < end:
        swap(start, end)
        start += 1
        end += 1

    def rotate(start, mid, end):
      if start == mid or mid == end: return
      n = gcd(end - start, mid - start)
      while n:
        n -= 1
        val = A[start + n]
        shift = mid - start
        p1 = start + n
        p2 = start + n + shift
        while p2 != start + n:
          self.swap(p1, p2, A) # right? (think so)
          p1 = p2
          if end - p2 > shift: p2 += shift
          else: p2 = start + (shift - (end - p2))
      n -= 1

    def merge(start, pivot, end, len1, len2):
      if len1 == 0 or len2 == 0: return
      if len1 + len2 == 2:
        if self.compare(pivot, start, A) < 0:
          self.swap(pivot, start, A)
        return
      if len1 > len2:
        len11 = len1/2
        first_cut = start + len11
        second_cut = lower(pivot, end, first_cut)
        len22 = second_cut - pivot
      else:
        len22 = len2/2
        second_cut = pivot + len22
        first_cut = upper(start, pivot, second_cut)
        len11 = first_cut - start
      rotate(first_cut, pivot, second_cut)
      new_mid = first_cut + len22
      merge(start, first_cut, new_mid, len11, len22)
      merge(new_mid, second_cut, end, len1 - len11, len2 - len22)
      
    def helper(start, end):
      if end - start < 12: insert_sort(start, end)
      else:
        middle = (start + end) / 2
        helper(start, middle)
        helper(middle, end)
        merge(start, middle, end, middle - start, end - middle)

    helper(0, len(A))

class GraphicComb(GraphicSort):
  SHRINKFACTOR = 1.3
  def sort(self):
    a = self.data[:]
    flipped = False
    gap = len(a)
    while flipped or gap > 1:
      gap = int(gap/self.SHRINKFACTOR)
      if gap == 0:
        gap = 1
      elif gap == 9 or gap == 10:
        gap = 11
      flipped = False
      top = len(a) - gap
      for i in xrange(top):
        j = i + gap
        if self.compare(i, j, a) > 0:
          self.swap(i, j, a)
          flipped = True

class GraphicCounting(GraphicSort):
  def sort(self):
    # cheat, not actually graphic sort
    cp = self.data[:]
    targets = range(len(cp))
    for elem in sorted(self.data):
      i = cp.index(elem)
      self.swap(i, targets[elem-1], cp)

class GraphicRadix(GraphicSort):
  def sort(self):
    cp = self.data[:]
    for i, elem in enumerate(sorted(self.data, key=lambda n: n % 10)):
      j = cp.index(elem)
      self.swap(i, j, cp)
    for i, elem in enumerate(sorted(self.data, key=lambda n: (n % 100))):
      j = cp.index(elem)
      self.swap(i, j, cp)
    for i, elem in enumerate(sorted(self.data, key=lambda n: (n % 1000))):
      j = cp.index(elem)
      self.swap(i, j, cp)

if __name__ == "__main__":
  sorts = {"bubble": GraphicBubble,
           "selection": GraphicSort,
           "radix": GraphicRadix,
           "insertion": GraphicInsert,
           "heap": GraphicHeap,
           "quick": GraphicQuick,
           "shell": GraphicShell,
           "shaker": GraphicShaker,
           "merge": GraphicMerge,
           "comb": GraphicComb,
           "counting": GraphicCounting
           }
  algo = get_resp("What sorting algorithm should I use [%s]? ", sorted(sorts.keys()))
  window = sorts[algo]()
  window.draw()
  window.sort()
  window.animate()
  print "Sorting complete."
  print "Comparisons:", window.compares
  print "Swaps:", window.swaps
  print "Total:", window.compares + window.swaps
  mainloop()
