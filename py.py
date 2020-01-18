import os
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
    name = mx[rowNum][-1]
    flag = mx[rowNum][0]
    p = mx[rowNum][3]
    if flag == 0:
        mx[rowNum][0] = 1
        mx[rowNum][3] = 1.0
    else:
        mx[rowNum][3] = p + 0.5
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
        else:
            mx[rowNum][3] = p + 0.2
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
        else:
            mx[rowNum][3] = p + 0.1
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
    with open('ans.txt', 'a') as f:
        f.write(name+','+str(rowNum)+','+str(res)+'\n')
    return 
def calc(devDict):
    os.system("WMLFRTMsg")
    if not getflag():
        return 'not conve'
    flows = dict()
    for l2name in devDict:
        for i in devDict[l2name]:
            flows[i[0]] = 0
    with open('LF.LP2', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            if len(line) > 0:
                name = line[-1]
                val = line[3]
                if name in devDict:
                    for i in devDict[name]:
                        devName = i[0]
                        flag = i[1]
                        flows[devName] += val * flag
    return flows
def getDev():
    devDict = dict()
    with open('DEV.SECTIONDEV', encoding='ANSI') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            name = line[0]
            l2name = line[2][2:-2]
            # print(name,l2name)
            flag = 1 if int(line[3]) == 1 else -1
            if l2name not in devDict:
                devDict[l2name] = []
            devDict[l2name].append((name, flag))
    #
    return devDict
origin = {'205': 47.39572, '206': 69.68512, '10000085': 69.68512, '207': 11.022490000000001, '208': -1.3010700000000002, '305': 25.72212, '10000086': 29.337680000000002, '10000088': 69.87326000000002, '10000084': 30.53146, '10000087': 30.04978, '10000300': 0.02341, '10000301': 0.02882, '10000380': 4.78772}
devDict = getDev()
print(calc(devDict))

for i in range(2283):
    changeOneGen(i, devDict)
