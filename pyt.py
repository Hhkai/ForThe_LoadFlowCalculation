import queue

class Node(object):
    def __init__(self, name):
        self.name = name
        self.neighbors = set()
        self.marks = dict()
        self.itype = 0
        return
    def addNeighbor(self, busLineNum):
        self.neighbors.add(busLineNum)
        return
    def addDevLine(self, name, bus):
        if name not in self.marks:
            self.marks[name] = set()
        self.marks[name].add(bus)
class L2(object):
    def __init__(self, name, Ibus, Jbus):
        self.name = name 
        self.Ibus = Ibus 
        self.Jbus = Jbus
class Dev(object):
    def __init__(self, name):
        self.name = name
        self.L2s = set()
    def addL2(self, num):
        self.L2s.add(num)
class Graph(object):
    def __init__(self, nodeSize = 15000, edgeSize = 50000):
        self.nodeSize = nodeSize
        self.edgeSize = edgeSize
        node = Node('sss')
        self.nodes = [node]
        tempL2 = L2('sss', 0, 0)
        self.L2s = [tempL2]
        self.busNameDict = dict()
        self.L2NameDict = dict()
    def readGraph(self):
        # 默认从当前路径读入图
        nodecnt = 0
        with open('LF.L1', encoding = 'gb2312', errors = 'ignore') as f:
            for line in f.readlines():
                line = eval(line.strip())
                if len(line) > 0:
                    node = Node(line[0])
                    self.nodes.append(node)
                    nodecnt += 1
        # 
        print(nodecnt,'=',len(self.nodes)-1)
        print(self.nodes[2].name)
        L2cnt = 0
        with open('LF.L2', encoding = 'gb2312', errors = 'ignore' ) as f:
            for line in f.readlines():
                line = eval(line.strip())
                if len(line) > 0:
                    name = line[-1]
                    Ibus = line[1]
                    Jbus = line[2]
                    if Ibus > nodecnt or Jbus > nodecnt:
                        print('warning')
                        continue
                    L2cnt += 1
                    self.nodes[Ibus].addNeighbor(Jbus)
                    self.nodes[Jbus].addNeighbor(Ibus)
                    l2 = L2(name, Ibus, Jbus)
                    self.L2s.append(l2)
                    self.L2NameDict[name] = L2cnt
        #
        with open('LF.L3', encoding = 'gb2312', errors = 'ignore') as f:
            for line in f.readlines():
                line = eval(line.strip())
                if len(line) > 0:
                    '''
                    if line[0] == 0:
                        # 无效
                        continue
                    '''
                    Ibus = line[1]
                    Jbus = line[2]
                    if Ibus > nodecnt or Jbus > nodecnt:
                        print('warning2')
                        continue
                    if Ibus <= 0 and (str(Ibus) not in self.busNameDict):
                        node = Node(str(Ibus))
                        self.nodes.append(node)
                        nodecnt += 1
                        self.busNameDict[str(Ibus)] = nodecnt
                        Ibus = nodecnt 
                    self.nodes[Ibus].addNeighbor(Jbus)
                    self.nodes[Jbus].addNeighbor(Ibus)
        print(nodecnt)
        with open('LF.L5', encoding = 'gb2312', errors = 'ignore') as f:
            for line in f.readlines():
                line = eval(line.strip())
                if len(line) > 0:
                    '''
                    if line[0] == 0:
                        # 无效
                        continue
                    '''
                    bus = line[1]
                    name = line[-1]
                    self.nodes[bus].itype = 'L5'
                    self.nodes[bus].itypename = name
        with open('LF.L6', encoding = 'gb2312', errors = 'ignore') as f:
            for line in f.readlines():
                line = eval(line.strip())
                if len(line) > 0:
                    '''
                    if line[0] == 0:
                        # 无效
                        continue
                    '''
                    bus = line[1]
                    name = line[-1]
                    self.nodes[bus].itype = 'L6'
                    self.nodes[bus].itypename = name
        return
    def readDev(self):
        self.devs = []
        self.devNameDict = dict()
        self.devcnt = 0
        with open('DEV.SECTIONDEV', encoding='ANSI') as f:
            for line in f.readlines():
                line = line.strip().split(',')
                name = line[0]
                l2name = line[2][2:-2]
                # print(name,l2name)
                if l2name not in self.L2NameDict:
                    print('L2name not in L2')
                tpL2num = self.L2NameDict[l2name]
                Ibus = self.L2s[tpL2num].Ibus 
                Jbus = self.L2s[tpL2num].Jbus 
                self.nodes[Ibus].addDevLine(name, Jbus)
                self.nodes[Jbus].addDevLine(name, Ibus)
                if name not in self.devNameDict:
                    tpdev = Dev(name)
                    self.devNameDict[name] = self.devcnt
                    self.devcnt += 1
                    self.devs.append(tpdev)
                self.devs[self.devNameDict[name]].addL2(tpL2num)
        return self.devs
    def checkGra(self):
        colors = [0] * len(self.nodes)
        curcolor = 1
        colorcnt = []
        for i in range(len(self.nodes)):
            if colors[i] != 0:
                continue 
            if self.nodes[i].itype == 0:
                continue
            colors[i] = curcolor 
            curcolorcnt = 1
            curcolor += 1
            q = queue.Queue()
            q.put(i)
            while not q.empty():
                h = q.get()
                for j in self.nodes[h].neighbors:
                    if colors[j] == 0:
                        q.put(j)
                        colors[j] = curcolor
                        curcolorcnt += 1
            colorcnt.append(curcolorcnt)
        print(curcolor)
        print('========')
        lessthan10 = 0
        for i in colorcnt:
            if i >= 10:
                print(i)
            if i < 10:
                lessthan10 += 1
        print('lessthan10:',lessthan10)
    def colorDev(self, dev):
        name = dev.name
        colors = [0] * len(self.nodes)
        curcolor = 0
        for i in dev.L2s:
            tpL2 = self.L2s[i]
            Ibus = tpL2.Ibus
            Jbus = tpL2.Jbus
            curcolor += 1
            q = queue.Queue()
            q.put(Ibus)
            colors[Ibus] = curcolor
            while not q.empty():
                h = q.get()
                for j in self.nodes[h].neighbors:
                    if (name not in self.nodes[h].marks) or (j not in self.nodes[h].marks[name]):
                        if colors[j] != curcolor:
                            q.put(j)
                            colors[j] = curcolor
            curcolor += 1
            q = queue.Queue()
            q.put(Jbus)
            colors[Jbus] = curcolor
            while not q.empty():
                h = q.get()
                for j in self.nodes[h].neighbors:
                    if (name not in self.nodes[h].marks) or (j not in self.nodes[h].marks[name]):
                        if colors[j] != curcolor:
                            q.put(j)
                            colors[j] = curcolor
        return colors
    def checkDev(self, dev):
        colors = self.colorDev(dev)
        twocolor = set()
        for i in dev.L2s:
            tpL2 = self.L2s[i]
            Icolor = colors[tpL2.Ibus] 
            Jcolor = colors[tpL2.Jbus]
            if Icolor == Jcolor:
                print('Icolor == Jcolor:',tpL2.Ibus,tpL2.Jbus)
            twocolor.add(Icolor)
            twocolor.add(Jcolor)
        print(twocolor)
        with open('ans.txt', 'a') as f:
            f.write('断面交流线：\n')
            for i in dev.L2s:
                tpL2 = self.L2s[i]
                f.write('交流线名称：'+tpL2.name + '\t 交流线行号：'+str(i)+'\t交流线两端母线行号：'+str(tpL2.Ibus)+',' + str(tpL2.Jbus) + '\n')
            f.write('从断面两端母线搜索拓展所得两分区包含发电机：\n')
            for i in twocolor:
                f.write('分区编号:' + str(i) + '\n')
                if i == 0:
                    continue
                for j in range(len(colors)):
                    if colors[j] == i:
                        if self.nodes[j].itype == 'L5':
                            f.write('母线：'+str(j)+'\t发电机  '+self.nodes[j].itypename + '\n')
                        '''
                        else:
                            f.write('母线：'+str(j) + '\n')
                        '''
    def findWay(self, Ibus, Jbus, name):
        vis = [0] * len(self.nodes)
        path = [0] * len(self.nodes)
        lenth = 0
        path[0] = Ibus
        find = 0
        while True:
            h = path[lenth]
            flag = 0
            for j in self.nodes[h].neighbors:
                if (name not in self.nodes[h].marks) or (j not in self.nodes[h].marks[name]):
                    if j == Jbus:
                        print('h',h)
                        find = 1
                    if vis[j] == 0:
                        lenth += 1
                        path[lenth] = j
                        flag = 1
                        vis[j] = 1
                if find == 1:
                    break
            if find == 1:
                break
            if flag == 0:
                lenth -= 1
            if lenth == -1:
                print('no way')
                break
        print(find)
        print(path[:lenth])
def main():
    g = Graph()
    g.readGraph()
    devs = g.readDev()
    g.checkGra()
    print(g.nodes[1563].neighbors)
    g.findWay(1832,1535,'208')
    return 
    for dev in devs:
        print(dev.name,'...')
        with open('ans.txt', 'a') as f:
            f.write('断面编号：' + dev.name + '\n')
        g.checkDev(dev)
if __name__ == '__main__':
    main()