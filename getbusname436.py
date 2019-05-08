def getbusname436() -> dict:
    dic = dict()
    with open("LF.L1") as f:
        lines = f.readlines()
        for ind, line in enumerate(lines):
            _ = eval(line.strip())
            _ = _[0]
            if _[:3] == "BUS":
                # print(_, len(_))
                dic[ind + 1] = eval(_[3:])
    # print(dic)
    # the next three lines output a file
    with open("busname.txt", 'w') as f:
        for i in dic:
            f.write("%d, %d\n" % (i, dic[i]))
    #
    return dic
#
if __name__ == "__main__":
    getbusname436()