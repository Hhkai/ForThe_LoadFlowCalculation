import queue
import math
import sys
import heapq

# python3

# P read from the LF.L5 and LF.L6

SIZE = 5000
nodes = [0] * SIZE

def readfile(filename, coding='utf-8'):
    mx = []
    with open(filename, 'r', encoding=coding) as f:
        lines = f.readlines()
        for line in lines:
            line = list(eval(line.strip()))
            mx.append(line)
    return mx
#

class Edge:
    def __init__(u_node : int, v_node : int, val):
        self.u = u_node
        self.v = v_node
        self.val = val
#
class Node:
    def __init__(self, ind):
        self.nbrs = set()
        self.ind = ind
        self.w = 0
        self.name = '-'
    def addNbr(self, node):
        self.nbrs.add(node)
    def annex(self, node):
        global nodes
        self.nbrs = self.nbrs | nodes[node].nbrs
        self.w += nodes[node].w 
        for i in nodes[node].nbrs:
            if i != node:
                nodes[i].nbrs.remove(node)
                nodes[i].nbrs.add(self.ind)
#
class Cut:
    def __init__(self, left, val):
        self.left = left 
        self.val = val 
    def __lt__(self, other):
        return abs(self.val) < abs(other.val)
    def mstr(self):
        return str(self.left) + '  ' + str(self.val) + '\n'
#
def readGraph():
    global nodes
    busname = [0]
    maxid = 0
    trans = dict()
    enodeset = set()
    # read BUS, nodes
    with open("LF.L1") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            busname.append(_[0])
        maxid = len(lines)
        for i in range(1, maxid + 1):
            nodes[i] = Node(i)
            nodes[i].name = busname[i]
    #
    with open("LF.L2") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            mark, left, right, id, R, X = _[:6]
            if mark == 1:
                nodes[left].addNbr(right)
                nodes[right].addNbr(left)
                enodeset.add(left)
                enodeset.add(right)
    #
    realbus = maxid
    with open("LF.L3") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            mark, left, right = _[:3]
            if mark == 1:
                if left > 0:
                    nodes[left].addNbr(right)
                    nodes[right].addNbr(left)
                    enodeset.add(left)
                    enodeset.add(right)
                else:
                    if left not in trans:
                        maxid += 1
                        nodes[maxid] = Node(maxid)
                        trans[left] = maxid
                        enodeset.add(maxid)
                        busname.append("v")
                    nodes[trans[left]].addNbr(right)
                    nodes[right].addNbr(trans[left])
                    enodeset.add(right)
    #
    mx5 = readfile('LF.L5')
    for i in mx5:
        nodes[i[1]].w = i[3]
    mx6 = readfile('LF.L6')
    for i in mx6:
        nodes[i[1]].w = -i[4]
    return busname, maxid, realbus, enodeset
#
def checkM(graph):
    global nodes
    Q = queue.Queue()
    canvis = set()
    for i in graph:
        Q.put(i)
        canvis.add(i)
        break
    # bfs
    while not Q.empty():
        u = Q.get()
        for i in nodes[u].nbrs:
            if i not in canvis:
                canvis.add(i)
                Q.put(i)
    #
    for i in graph:
        if i in canvis:
            continue
        else:
            return False
    return True
#
def main():
    global nodes
    print("read files ...")
    busname, nodecnt, realbus, enodeset = readGraph()
    print(nodecnt)
    for i in range(1, nodecnt + 1):
        print(nodes[i].nbrs)
    #
    h = []
    hcnt = 0
    maxhcnt = 20
    nodesleft = enodeset
    while True:
        curval = None
        curcut = None
        for i in nodesleft:
            ns = nodesleft - set([i])
            if checkM(ns):
                newcut = Cut(ns, nodes[i].w)
                heapq.heappush(h, newcut)
                hcnt += 1
                if hcnt > maxhcnt:
                    heapq.heappop(h)
            # merge two points
            for j in nodes[i].nbrs:
                if j in nodesleft:
                    ns = nodesleft - set([i, j])
                    if checkM(ns):
                        nw = nodes[i].w + nodes[j].w
                        newcut = Cut(ns, nw)
                        heapq.heappush(h, newcut)
                        hcnt += 1
                        if hcnt > maxhcnt:
                            heapq.heappop(h)
                        if curval == None or abs(nw) > abs(curval):
                            curval = nw 
                            curcut = (i, j)
        # 
        if curval == None:
            break
        nodesleft.remove(curcut[1])
        nodes[i].annex(j)
    with open('out1.txt', 'w') as f:
        for i in h:
            f.write(i.mstr())
            '''
            f.write('(')
            for j in i.left:
                f.write('%s:%s,'%(j,nodes[j].name))
            f.write(')        %s\n'%i.val)
            '''
#
if __name__ == "__main__":
    main()
