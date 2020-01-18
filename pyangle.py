import os

class Dev:
    def __init__(self, name):
        self.name = name
        self.lines = dict()
        self.buses = dict()
    def addLine(self, lineName, flag):
        self.lines[lineName] = flag
def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success == 1
def changeOneGen(rowNum, devDict):
    mx = []
    with open('LF.L5', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            lis = list(line)
            mx.append(lis)
    # get mx 
    deltaP = 0
    name = mx[rowNum][-1]
    flag = mx[rowNum][0]
    p = mx[rowNum][3]
    if flag == 0:
        mx[rowNum][0] = 1
        mx[rowNum][3] = 1.0
        deltaP = 1.0
    else:
        mx[rowNum][3] = p + 0.5
        deltaP = 0.5
    # change mx 
    with open('LF.L5', mode = 'w', encoding = 'gb2312', errors = 'ignore') as f:
        for row in mx:
            templine = []
            for j in row:
                templine.append(j)
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 4)
            f.write(str(templine)[1:-1] + ',\n')
    # write 
    res = calc(devDict)
    if res == 'not conve':
        if flag == 0:
            mx[rowNum][0] = 1
            mx[rowNum][3] = 0.5
            deltaP = 0.5
        else:
            mx[rowNum][3] = p + 0.2
            deltaP = 0.2
        # change mx 
        with open('LF.L5', mode = 'w', encoding = 'gb2312', errors = 'ignore') as f:
            for row in mx:
                templine = []
                for j in row:
                    templine.append(j)
                for ind, iii in enumerate(templine):
                    if type(iii) == type(0.0):
                        templine[ind] = round(iii, 4)
                f.write(str(templine)[1:-1] + ',\n')
        res = calc(devDict)
    if res == 'not conve':
        if flag == 0:
            mx[rowNum][0] = 1
            mx[rowNum][3] = 0.2
            deltaP = 0.2
        else:
            mx[rowNum][3] = p + 0.1
            deltaP = 0.1
        # change mx 
        with open('LF.L5', mode = 'w', encoding = 'gb2312', errors = 'ignore') as f:
            for row in mx:
                templine = []
                for j in row:
                    templine.append(j)
                for ind, iii in enumerate(templine):
                    if type(iii) == type(0.0):
                        templine[ind] = round(iii, 4)
                f.write(str(templine)[1:-1] + ',\n')
        res = calc(devDict)
    
    # write back
    mx[rowNum][0] = flag
    mx[rowNum][3] = p 
    with open('LF.L5', mode = 'w', encoding = 'gb2312', errors = 'ignore') as f:
        for row in mx:
            templine = []
            for j in row:
                templine.append(j)
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 4)
            f.write(str(templine)[1:-1] + ',\n')
    # write back
    with open('ans0118.txt', 'a') as f:
        f.write('%d,%s,%s,\n' % (rowNum, str(deltaP), str(res)))
    return 
def calc(devDict):
    os.system("WMLFRTMsg")
    if not getflag():
        return 'not conve'
    
    ###
    angels = dict()
    with open('LF.LP1', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            if len(line) > 3:
                num = line[0]
                val = line[2]
                angels[num] = val
    #
    res = dict()
    for i in devDict:
        res[i] = 0
        dd = devDict[i]
        cnt = 0
        for l2name in dd.lines:
            Ibus = dd.buses[l2name][0]
            Jbus = dd.buses[l2name][1]
            if (Ibus not in angels) or (Jbus not in angels):
                continue
            
            val1 = angels[Ibus]
            val2 = angels[Jbus]
            res[i] += (val1 - val2) * dd.lines[l2name]
        if cnt != 0:
            res[i] = res[i] / cnt
    return res
def getDev():
    devDict = dict()
    with open('DEV.SECTIONDEV', encoding='ANSI') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            name = line[0]
            l2name = line[2][2:-2]
            # print(name,l2name)
            flag = 1 if int(line[3]) == 1 else -1
            if name not in devDict:
                devDict[name] = Dev(name)
            devDict[name].addLine(l2name, flag)
    #
    with open('LF.L2', encoding = 'gb2312', errors = 'ignore' ) as f:
        for line in f.readlines():
            line = eval(line.strip())
            if len(line) > 0:
                name = line[-1]
                Ibus = line[1]
                Jbus = line[2]
                for i in devDict:
                    if name in devDict[i].lines:
                        devDict[i].buses[name] = (Ibus, Jbus)
    #
    return devDict
origin = {'205': 14.7519242764, '206': 27.885202960900006, '207': 9.9450243565, '208': -0.3654502055000002, '305': 15.2797509766, '10000084': 26.0418735994, '10000085': 27.885202960900006, '10000086': 21.3427491183, '10000087': 15.678826287599998, '10000088': 47.31264708020001, '10000300': -0.06629934400000081, '10000301': -0.07864156260000144, '10000380': 8.6641441182}
devDict = getDev()
print(calc(devDict))
#exit()
for i in range(2283):
    changeOneGen(i, devDict)
