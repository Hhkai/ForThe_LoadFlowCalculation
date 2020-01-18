import re
def main():
    outdic = dict()
    indic = dict()
    ori = {'205': 47.39572, '206': 69.68512, '10000085': 69.68512, '207': 11.022490000000001, '208': -1.3010700000000002, '305': 25.72212, '10000086': 29.337680000000002, '10000088': 69.87326000000002, '10000084': 30.53146, '10000087': 30.04978, '10000300': 0.02341, '10000301': 0.02882, '10000380': 4.78772}
    m=r'(.*?),(.*?),\{(.*?)\}'
    m = re.compile(m)
    for i in ori:
        outdic[i] = []
        indic[i] = []
    with open('ans.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            r = m.match(line)
            if r:
                name = r.group(1)
                num = int(r.group(2)) + 1
                tempdic = eval('{'+r.group(3)+'}')
                for i in tempdic:
                    if tempdic[i] - ori[i] > 0.001:
                        #outdic[i].append((num, name))
                        outdic[i].append(num)
                    if ori[i] - tempdic[i] > 0.001:
                        #indic[i].append((num, name))
                        indic[i].append(num)
            else:
                print('not conv')
    with open('ans2.txt', 'w') as f:
        for i in ori:
            f.write(i+'\n')
            f.write('#\n')
            f.write('    ' + str(outdic[i])[1:-1]+'\n')
            f.write('%\n')
            f.write('    ' + str(indic[i])[1:-1]+'\n')
            f.write('---\n')
    return 
main()