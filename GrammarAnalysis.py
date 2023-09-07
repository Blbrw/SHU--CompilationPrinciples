import Base
import LexicalAnalysis


class GrammarAnalysis:
    def __init__(self, inppath=None, inopath=None):
        """
        :param inppath: PL/0输入程序文本路径
        :param inopath:程序2输出结果文件
        """
        if inppath is not None:
            self.res = Base.split_key(filename=inppath)
        if inopath is not None:
            self.res = Base.split_key(strmeg=LexicalAnalysis.SeparateAndIdentify(inopath))
        print(self.res)
        self.stack = []
        self.lp = 0
        self.llp = 0
        self.errors = True

    def solution(self):
        """
        语法分析
        :return: 语法判断结果
        """
        alen = len(self.res)
        flag = False
        for idx in range(0, alen):
            if flag:
                flag = False
                continue
            print(idx)
            item = self.res[idx]
            if item == "lparen":
                self.append_lp()
            elif item == "llparen":
                self.append_llp()
            elif item in Base.operatorname:
                self.append_op(item)
            elif item == "ident":
                if idx == alen - 1:
                    self.append_ident()
                elif self.res[idx + 1] == "lparen":
                    flag = True
                    self.append_f()
                elif self.res[idx + 1] == "llparen":
                    flag = True
                    self.append_a()
                else:
                    self.append_ident()
            elif item == "number":
                self.append_ident()
            elif item == "rparen":
                self.append_rp()
            elif item == "rrparen":
                self.append_rrp()
            else:
                self.errors = False
                Base.gra_error("未知语法错误")
            # print(lp)
            print(self.stack)
        return self.check_last()

    def list_end(self):
        """
        读取stack尾部数据
        :return: None
        """
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def append_ident(self):
        """
        添加标识符
        :return: None
        """
        if self.list_end() in Base.operatorname:
            self.stack.pop()
            if self.list_end() is None:
                self.append_ident()
            elif self.list_end() in ["ident", "number"]:
                self.stack.pop()
                self.append_ident()
        elif self.list_end() not in [None, "function", "array", "lparen", "llparen"]:
            self.errors = False
            print(self.stack)
            print(Base.gra_error("缺少运算符"))
        else:
            self.stack.append("ident")

    def append_op(self, op):
        """
        添加运算符符
        :param op: 运算符类型
        :return: None
        """
        if self.list_end() in [None, "function", "array", "lparen", "number", "ident"]:
            self.stack.append(op)
        else:
            self.errors = False
            print(Base.gra_error("运算符两边应为数字或标识符"))

    def append_f(self):
        """
        添加函数调用
        :return: None
        """
        self.lp += 1
        self.stack.append("function")

    def append_a(self):
        """
        添加数组元素
        :return:None
        """
        self.llp += 1
        self.stack.append("array")

    def append_lp(self):
        """
        添加"("
        :return:None
        """
        if self.list_end() == "number":
            self.errors = False
            print(Base.gra_error("缺少运算符"))
        else:
            self.stack.append("lparen")
            self.lp += 1

    def append_llp(self):
        """
        添加"["
        :return:None
        """
        if self.list_end() == "number":
            self.errors = False
            print(Base.gra_error("缺少运算符"))
        else:
            self.stack.append("llparen")
            self.llp += 1

    def append_rp(self):
        """
        添加")"并结算
        :return:None
        """
        if self.list_end() in ["function", "lparen"]:
            self.stack.pop()
            self.lp -= 1
            self.append_ident()
        elif self.list_end() in ["ident", "number"]:
            self.stack.pop()
            self.append_rp()
        else:
            self.errors = False
            print(Base.gra_error("缺少'('"))

    def append_rrp(self):
        """
        添加"]"并结算
        :return:None
        """
        if self.list_end() in ["array", "llparen"]:
            self.stack.pop()
            self.llp -= 1
            self.append_ident()
        elif self.list_end() in ["ident", "number"]:
            self.stack.pop()
            self.append_rrp()
        else:
            self.errors = False
            print(Base.gra_error("缺少'['"))

    def check_last(self):
        """
        运行结果检测
        :return:
        """
        ed = self.list_end()
        if (ed is None or (len(self.stack) == 1 and self.stack[0] == "ident") )and self.errors is True:
            return "语法正确"
        elif ed in Base.operatorname:
            return Base.gra_error("操作符缺少标识符或数字")
        elif self.lp > 0:
            return Base.gra_error("操作符缺少')'")
        elif self.llp > 0:
            return Base.gra_error("操作符缺少']'")
        else:
            return Base.gra_error("多余项")

#  语法分析
if __name__ == "__main__":
    # A = GrammarAnalysis(inppath="./case3/input7.txt")
    A = GrammarAnalysis(inopath="./case3/input10.txt")
    print(A.solution())

















