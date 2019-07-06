import queue
import math
import sys

# python3

SIZE = 50000
edgeList = [0] * SIZE
head = [0] * SIZE # the ``first'' edge of nodes
ecnt = 0

class edge:
    def __init__(self, v, nxt, val):
        self.v = v 
        self.nxt = nxt # the next edge. Actually, it is a Linked List
        self.val = val 
def addEdge(u, to, val, edgeList):
    global ecnt
    global head
    ecnt += 1
    edgeList[ecnt] = edge(to, head[u], val)
    head[u] = ecnt
def dijkstra(u, nodecnt):
    global ecnt
    global head
    dis = [999999999] * (nodecnt + 1) 
    vis = [0] * (nodecnt + 1) 
    q = queue.PriorityQueue()
    dis[u] = 0
    q.put((0, u)) # push a tuple
    while not q.empty():
        flag = q.get()
        v = flag[1]
        if vis[v] != 0:
            continue
        vis[v] = 1
        i = head[v]
        while i != 0:
            to = edgeList[i].v 
            if dis[to] > dis[v] + edgeList[i].val:
                dis[to] = dis[v] + edgeList[i].val 
                q.put((dis[to], to))
            i = edgeList[i].nxt
    return dis 
#

def readEdge():
    busname = [0]
    maxid = 0
    trans = dict()
    with open("LF.L1") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            busname.append(_[0])
        maxid = len(lines)
    #
    with open("LF.L2") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            mark, left, right, id, R, X = _[:6]
            if mark == 1:
                dis = math.sqrt(R * R + X * X)
                addEdge(left, right, dis, edgeList)
                addEdge(right, left, dis, edgeList)
    #
    realbus = maxid
    with open("LF.L3") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            mark, left, right = _[:3]
            if mark == 1:
                if left > 0:
                    addEdge(left, right, 0, edgeList)
                    addEdge(right, left, 0, edgeList)
                else:
                    if left not in trans:
                        maxid += 1
                        trans[left] = maxid
                        busname.append("v")
                    addEdge(trans[left], right, 0, edgeList)
                    addEdge(right, trans[left], 0, edgeList)
    return busname, maxid, realbus
def readGen():
    genlist = []
    with open("LF.L5") as f:
        lines = f.readlines()
        for n, line in enumerate(lines):
            _ = eval(line.strip())
            mark, id = _[:2]
            if mark == 1:
                genlist.append(id)
    return genlist
class bus:
    def __init__(self):
        self.genDis = dict()
    def addGen(self, genid, dis):
        self.genDis[genid] = dis
    def mysort(self):
        self.genList = sorted(self.genDis.items(), key=lambda d:d[1], reverse = False)
def main():
    print("read files ...")
    busname, nodecnt, realbus = readEdge()
    genList = readGen()
    buses = []
    for i in range(nodecnt):
        buses.append(bus())
    for i in genList:
        sys.stdout.write("\r%d/%d" % (i, nodecnt))
        dis = dijkstra(i, nodecnt)
        for busid, val in enumerate(dis):
            buses[busid - 1].addGen(i, val)
    sys.stdout.write("\r------end------\n")
    for i in buses:
        i.mysort()
    #
    with open("out.txt", "w") as f:
        for i in buses[:realbus]:
            for j in i.genList:
                # f.write("%d:%f, " % (j[0], j[1]))
                f.write("%d, " % j[0])
            f.write("\n")
    '''
    with open("nameout.dis", "w") as f:
        for n, i in enumerate(buses):
            f.write("%s:" % busname[n + 1])
            for j in i.genList:
                f.write("%s, " % busname[j[0]])
            f.write("\n")
    '''
if __name__ == "__main__":
    main()
