import Base

if __name__ == "__main__":
    identifier = []
    count = {}
    res = Base.split_pro("./input.txt")
    for item in res:
        if Base.isident(item):
            if count.get(item) is None:
                count[item] = 1
                identifier.append(item)
            else:
                count[item] += 1

    with open("output.txt", "w") as f:
        for iden in identifier:
            print("("+iden+": "+str(count.get(iden))+")", file=f)
# 样例
# 输入
# Const num=100;
# Var a1,b2;
# Begin
# Read(A1);
# b2:=a1+num;
# write(A1,B2);
# End.
# 输出
# (num: 2)
# (a1: 4)
# (b2: 3)




