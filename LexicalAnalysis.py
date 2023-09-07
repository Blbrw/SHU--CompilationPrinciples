import Base


def SeparateAndIdentify(inpath, outpath=None):
    """
    :param inpath: PL/0输入程序文本路径
    :param outpath: 结果输出路径
    :return:结果(ident,abc)
    """
    res = Base.split_pro(inpath)
    alt = ""
    for item in res:
        alt += "(" + Base.code(item) + ",\t" + item + ")\n"
    if outpath is not None:
        with open(outpath, "w") as f:
            # print(alt)
            print(alt, file=f)
    return alt

# 词法分析
if __name__ == "__main__":
    SeparateAndIdentify("./case2/input2.txt", "./output.txt")







