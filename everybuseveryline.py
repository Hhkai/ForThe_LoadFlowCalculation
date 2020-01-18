import os
def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success == 1
def changeOneGen(rowNum, ori):
    mx = []
    with open('anse.txt', 'a') as f:
        f.write('#'+str(rowNum+1)+'\n')
    with open('LF.L5', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            lis = list(line)
            mx.append(lis)
    # get mx 
    name = mx[rowNum][-1]
    flag = mx[rowNum][0]
    p = mx[rowNum][3]
    deltaP = 0
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
    res = calc(deltaP, ori)
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
        res = calc(deltaP, ori)
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
        res = calc(deltaP, ori)
    
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
    with open('anse.txt', 'a') as f:
        f.write('---\n')
    return 
def calc(deltaP, ori):
    os.system("WMLFRTMsg")
    if not getflag():
        return 'not conve'
    tempStore = dict()
    with open('LF.LP2', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            if len(line) > 0:
                name = line[-1]
                if name not in ori:
                    continue
                val = line[3]
                rate = (val - ori[name]) / deltaP
                if rate > 0.00001 or rate < -0.00001:
                    tempStore[name] = rate
                
    with open('anse.txt', 'a') as f:
        for i in tempStore:
            f.write(i+', %.6f\n' % tempStore[i])
    return 'ok'
def getOriginLP2():
    Lp2s = dict()
    with open('LFori.LP2', encoding='gb2312', errors='ignore') as f:
        for line in f.readlines():
            line = eval(line.strip())
            if len(line) > 0:
                name = line[-1]
                val = line[3]
                Lp2s[name] = val
    return Lp2s
oriLp2s = getOriginLP2()
for i in range(2283):
    changeOneGen(i, oriLp2s)
