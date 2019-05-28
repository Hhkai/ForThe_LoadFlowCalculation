def findbuswithmostline():
    cnt = dict()
    with open('LF.L2') as f:
        lines = f.readlines()
        for line in lines:
            templine = eval(line.strip())
            if templine[1] != templine[2]:
                if templine[1] not in cnt:
                    cnt[templine[1]] = 0
                if templine[2] not in cnt:
                    cnt[templine[2]] = 0
                cnt[templine[1]] += 1
                cnt[templine[2]] += 1
    x = sorted(cnt.items(), key=lambda d:d[1], reverse = True)
    return [i[0] for i in x]

if __name__ == '__main__':
    print findbuswithmostline()