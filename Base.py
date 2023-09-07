basic_words = ["begin", "call", "const", "do", "end", "if", "odd", "procedure", "read", "then", "var", "while", "write"]
operator = ["+", "-", "*", "/", ":=", "#", "<=", "<", ">=", ">", "="]
delimiter = [',', '(', '[', ']', ')', ';', '.']
codes = {"begin": "beginsym","call": "callsym","const": "constsym",
         "do": "dosym","end": "endsym","if": "ifsym","odd": "oddsym",
         "procedure": "proceduresym","read": "readsym","then": "thensym",
         "var": "varsym","while": "whilesym","write": "writesym","+": "plus",
         "-": "minus","*": "times","/": "slash",":=": "becomes","#": "neq",
         "<=": "leq","<": "lss",">=": "geq",">": "gtr",
         "=": "eql","(": "lparen","[": "llparen",")": "rparen",
         "]": "rrparen",",": "comma",";": "semicolon",".": "period"}
split_by = ["++"]+operator + delimiter
operatorname = [codes[item] for item in operator]


def isident(str_s):
    """
    :param str_s:判断的字符串
    :return: 是否为标识符
    """
    if str_s is None:
        return False
    if len(str_s) <= 0:
        return False
    if not str_s[0].isalpha():
        return False
    for i in range(1, len(str_s)):
        if not (str_s[i].isalpha() or str_s[i].isdigit or str_s[i] == '_'):
            # 数字，字母，下划线
            return False
    if str_s in delimiter:
        # 界符
        return False
    if str_s in basic_words:
        # 基本字
        return False
    return True


def isdigit(str_s):
    if str_s is None:
        return False
    return str_s.isdigit()


def split(items, i):
    """
    :param items: 从items中提取split_by[i]
    :param i:
    :return: 提取列表
    """
    res = []
    if i == len(split_by):
        return [items]
    items = items.split(split_by[i])
    for item in items:
        res += split(item, i + 1)
        res.append(split_by[i])
    if len(res) > 0:
        res.pop()
    return res


def code(str_s):
    """
    判断字符串类型
    :param str_s:判断对象
    :return: 类型结果
    """
    if isdigit(str_s):
        return "number"
    if isident(str_s):
        return "ident"
    elif codes.get(str_s) is None:
        return "error"
    else:
        return codes.get(str_s)


def split_pro(filename):
    """
    将程序分成个个单位
    :param filename:目标程序
    :return:分离单位列表
    """
    with open(filename) as f:
        f = f.read().lower().split()
        res = []
        for item in f:
            tem_res = split(item, 0)
            for it in tem_res:
                if len(it) > 0:
                    res.append(it)
    return res


def split_key(filename=None, strmeg=None):
    """
    从（ident，ABC）中，提取ident
    :param filename: 文本形式
    :param strmeg: 字符串形式
    :return:
    """
    res = []
    li = []
    if filename is not None:
        with open(filename) as f:
            f = f.read().lower().split('\n')
        li = f
    if strmeg is not None:
        li = strmeg.lower().split('\n')

    for line in li:
        line = line[1:len(line)-1]
        line = line.split(',\t')
        if len(line[0]) > 0:
            res.append(line[0])
    return res


def split_val(filename):
    """
    从（ident，ABC）中，提取ABC
    :param filename: 文本形式
    :return:
    """
    with open(filename) as f:
        f = f.read().lower().split('\n')
        res = []
        for line in f:
            line = line[1:len(line)-1]
            line = line.split(',\t')
            res.append(line[1])
    return res


def get_pair(filename):
    """
    从（ident，ABC）中，提取键值对
    :param filename: 文本形式
    :return: res
    """
    with open(filename) as f:
        f = f.read().lower().split('\n')
        a = []
        b = []

        for line in f:
            if len(line) < 5:
                continue
            line = line[1:len(line)-1]
            line = line.split(',\t')
            a.append(line[0])
            b.append(line[1])
    return zip(a, b)

def gra_error(mesg):
    return "语法错误:"+mesg

#基本函数


