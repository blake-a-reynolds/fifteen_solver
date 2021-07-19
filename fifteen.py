import sys
import argparse
from collections import namedtuple
from functools import partial
import heapq

'''----------------------------------------------------------------------------

STATES

----------------------------------------------------------------------------'''

Point = namedtuple('Point', ['x', 'y'])

class Node:
  def __init__(self, state, blank, opname, parent, g):
    self.state = state
    self.blank = blank
    self.opname = opname
    self.parent = parent
    self.g = g
    self.f = self.g + self.heuristic()

  def __eq__(self, other):
    return self.state == other.state

  def __hash__(self):
    return hash(self.state)

  def goal(self):
    GS = (
      1,  2,  3,  4,
      5,  6,  7,  8,
      9,  10, 11, 12,
      13, 14, 15, 0)
    return self.state == GS

  def heuristic(self):
    GOAL_COORDINATES = (
      Point(3,3), Point(0,0), Point(1,0), Point(2,0),
      Point(3,0), Point(0,1), Point(1,1), Point(2,1),
      Point(3,1), Point(0,2), Point(1,2), Point(2,2),
      Point(3,2), Point(0,3), Point(1,3), Point(2,3)) 
    to_coords = lambda i: (i % 4, i // 4)
    h = 0
    for i in range(16):
      if (self.state[i] == 0): continue
      xc,yc = to_coords(i)
      xg,yg = GOAL_COORDINATES[self.state[i]]
      dx = abs(xg - xc)
      dy = abs(yg - yc)
      m = dx + dy
      if (m == 0): continue
      d = 0 if (abs(dx - dy) == 0) else abs(dx - dy) - 1
      md = 0 if (m - d == 0) else m - d - 1
      h += 1 + 5 * d + 3 * md
    return h


'''----------------------------------------------------------------------------

OPERATORS:

----------------------------------------------------------------------------'''

def move(node, name, f):
  to_index = lambda point : point.x + 4 * point.y
  x, y = f(node.blank)
  if (x < 0 or x > 3 or y < 0 or y > 3):
    return None
  new_blank = Point(x, y)
  oldindex = to_index(node.blank)
  newindex = to_index(new_blank)
  state = list(node.state)
  state[oldindex], state[newindex] = state[newindex], state[oldindex]
  state = tuple(state)
  return Node(state, new_blank, name, node, node.g+1)

OPERATORS = (
  partial(move, name = 'left', f = lambda p : (p.x-1, p.y)),
  partial(move, name = 'right',f = lambda p : (p.x+1, p.y)),
  partial(move, name = 'up', f = lambda p : (p.x, p.y-1)),
  partial(move, name = 'down', f = lambda p : (p.x, p.y+1)))


'''----------------------------------------------------------------------------

priorityq

----------------------------------------------------------------------------'''

class priorityq:
  def __init__(self):
    self.pq = []
    self.items = {}
    self.counter = 0

  def enqueue(self, obj, priority):
    item = [priority, self.counter, obj]
    self.items[obj] = item
    heapq.heappush(self.pq, item)
    self.counter += 1

  def update_key(self, obj, priority):
    old_item = self.items.pop(obj)
    old_item[2] = None
    self.enqueue(obj, priority)

  def dequeue(self):
    while (self.pq):
      *_, item = heapq.heappop(self.pq)
      if (item):
        del self.items[item]
        return item
    raise KeyError('priorityq Underflow')

  def __contains__(self, key):
    return key in self.items

  def __len__(self):
    return len(self.items)

  def get(self, key):
    *_, item = self.items[key]
    return item

  def empty(self):
    return not self.pq


'''----------------------------------------------------------------------------

print_state(node)
solution(node)
get_initial_state()

-----------------------------------------------------------------------------'''

def print_state(node):
  state = ['[]' if (x == 0) else x for x in node.state]
  for i in range(0,16,4):
    print('\t{:2} {:2} {:2} {:2}'.format(*(state[i:i+4])))
  print()

def solution(node):
  solution = []
  while (node):
    solution.append(node)
    node = node.parent
  print('Solution({}):'.format(len(solution)-1))
  i = 0
  for node in reversed(solution):
    print('{}.\t{}'.format(i, node.opname))
    print_state(node)
    i += 1

def get_initial_state():
  #prompt = 'Enter puzzle as a sequence of tile numbers (0 for blank): '
  #ins = tuple([int(x) for x in input(prompt).split() if x.isdigit()])
  #i = 0
  #while (i < len(ins) and ins[i] != 0):
  #   i += 1
  #p = Point(i%4, i//4)
  #return Node(ins, p, 'start', None, 0)

  parser = argparse.ArgumentParser(description='15 puzzle solver: '
    'enter tile numbers from top-left to bottom-right, with 0 for space')
  parser.add_argument('tiles', metavar='N', type=int, nargs=16,
    help='0 <= N <= 15')
  tiles = parser.parse_args().tiles
  encountered = [False for i in range(16)]
  for tile in tiles:
    if tile < 0 or tile > 15:
      parser.error('invalid tile')
    if encountered[tile]:
      parser.error('duplicate tiles')
    encountered[tile] = True
  i = 0
  while (i < len(tiles) and tiles[i] != 0):
     i += 1
  p = Point(i%4, i//4)
  return Node(tuple(tiles), p, 'start', None, 0)


'''----------------------------------------------------------------------------

A* search

-----------------------------------------------------------------------------'''

start = get_initial_state()
closed = set()
openq = priorityq()
openq.enqueue(start, start.f)
while (not openq.empty()):
  node = openq.dequeue()
  if (node.goal()):
    closed_nodes = len(closed)
    open_nodes = len(openq)
    total_nodes = closed_nodes + open_nodes
    print('Nodes generated: {} ({} open, {} closed)'.format(
      total_nodes, open_nodes, closed_nodes))
    solution(node)
    sys.exit(0)

  closed.add(node)
  for op in OPERATORS:
    child = op(node)
    if (not child): continue
    if (child not in closed and child not in openq):
      openq.enqueue(child, child.f)
    elif (child in openq and child.f < openq.get(child).f):
      openq.update_key(child, child.f)

print('No solution found')
