import Base
from LexicalAnalysis import SeparateAndIdentify


class Four:
    def __init__(self, op, num1, num2, res):
        self.op = op
        self.num1 = num1
        self.num2 = num2
        self.res = res

    def __str__(self):
        return "({},{},{},{})".format(self.op, self.num1, self.num2, self.res)


class SA:
    def __init__(self, inpath=None):
        SeparateAndIdentify(inpath, './output.txt')
        self.s = Base.get_pair('./output.txt')  # (ident,abc)
        self.s = list(self.s)
        self.s.append(("#", "#"))
        print(self.s)
        self.now = tuple()
        self.ans = 0
        self.p = -1
        self.errors = False
        self.opin = []  # 符号栈
        self.statein = []  # 状态栈
        self.fours = []
        self.next()
        self.count = {"T": 0, "X": 0, "Y": 0, "E": 0}  # 变量#项#因子#表达式
        self.words = {}
        self.finish = False
        self.res = {}

    def next(self):
        self.p += 1
        self.now = self.s[self.p]

    def newtemp(self, st):
        self.count[st] += 1
        return st + str(self.count[st])

    def newemit(self, op, num1, num2, res):
        self.fours.append(Four(op, num1, num2, res))

    def gy(self, mf):
        self.statein.pop()
        intop = self.opin[len(self.opin) - 1]
        self.opin.pop()
        # name = self.newtemp(mf)
        # self.opin.append(name)
        if mf == "Y":
            name = self.newtemp(mf)
            self.opin.append(name)
            self.words.__setitem__(name, intop)
        else:
            name = self.newtemp(mf)
            self.opin.append(name)
            # print(name, self.words[intop])
            self.words.__setitem__(name, self.words[intop])
        self.Analy_goto()

    def Analy_action(self):
        state = self.statein[len(self.statein) - 1]
        if state == 0:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "-":
                self.statein.append(2)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 1:
            if self.now[1] == "+":
                self.statein.append(8)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "-":
                self.statein.append(9)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "#":
                self.finish = True
                self.p += 1
            else:
                self.errors = True
        elif state == 2:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 3:
            if self.now[1] == "*":
                self.statein.append(12)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "/":
                self.statein.append(13)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] in ["#", "+", "-", ")"]:
                self.gy("E")
            else:
                self.errors = True
        elif state == 4:
            if self.now[1] in [")", "+", "-", "*", "/", "#"]:
                self.gy("X")
            else:
                self.errors = True
        elif state == 5:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "-":
                self.statein.append(2)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 6:
            if self.now[1] in [")", "+", "-", "*", "/", "#"]:
                self.gy("Y")
            else:
                self.errors = True
        elif state == 7:
            if self.now[1] in [")", "+", "-", "*", "/", "#"]:
                self.statein.pop()
                intop = self.opin[len(self.opin) - 1]
                self.opin.pop()
                name = self.newtemp("Y")
                self.opin.append(name)
                res = self.newtemp("T")
                self.newemit("=", "_", intop, res)
                self.words[name] = res
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 8:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 9:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 10:
            if self.now[1] == "*":
                self.statein.append(12)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "/":
                self.statein.append(13)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] in ["#", "+", "-", ")"]:
                self.statein.pop()
                self.statein.pop()
                intop = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                name = self.newtemp("E")
                self.opin.append(name)
                res = self.newtemp("T")
                self.newemit("-", "_", self.words[intop], res)
                self.words[name] = res
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 11:
            if self.now[1] in [")", "+", "-", "*", "/", "#"]:
                self.gy("X")
            else:
                self.errors = True
        elif state == 12:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 13:
            if self.now[0] == "ident":
                self.statein.append(6)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[0] == "number":
                self.statein.append(7)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "(":
                self.statein.append(5)
                self.opin.append(self.now[1])
                self.next()
            else:
                self.errors = True
        elif state == 14:
            if self.now[1] == ")":
                self.statein.append(19)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "+":
                self.statein.append(8)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "-":
                self.statein.append(9)
                self.opin.append(self.now[1])
                self.next()
            else:
                print("error")
                self.errors = True
        elif state == 15:
            if self.now[1] == "*":
                self.statein.append(12)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "/":
                self.statein.append(13)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] in ["#", "+", "-", ")"]:
                self.statein.pop()
                self.statein.pop()
                self.statein.pop()
                intop1 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                intop2 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                sname = self.newtemp("E")
                self.opin.append(sname)
                name = self.newtemp("T")
                self.newemit("+", self.words[intop2], self.words[intop1], name)
                self.words[sname] = name
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 16:
            if self.now[1] == "*":
                self.statein.append(12)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] == "/":
                self.statein.append(13)
                self.opin.append(self.now[1])
                self.next()
            elif self.now[1] in ["#", "+", "-", ")"]:
                self.statein.pop()
                self.statein.pop()
                self.statein.pop()
                intop1 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                intop2 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                sname = self.newtemp("E")
                self.opin.append(sname)
                name = self.newtemp("T")
                self.newemit("-", self.words[intop2], self.words[intop1], name)
                self.words[sname] = name
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 17:
            if self.now[1] in ["#", "+", "-", "*", "/", ")"]:
                self.statein.pop()
                self.statein.pop()
                self.statein.pop()
                intop1 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                intop2 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                sname = self.newtemp("X")
                self.opin.append(sname)
                name = self.newtemp("T")
                self.newemit("*", self.words[intop2], self.words[intop1], name)
                self.words[sname] = name
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 18:
            if self.now[1] in ["#", "+", "-", ")", "*", "/"]:
                self.statein.pop()
                self.statein.pop()
                self.statein.pop()
                intop1 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                intop2 = self.opin[len(self.opin) - 1]
                self.opin.pop()
                sname = self.newtemp("X")
                self.opin.append(sname)
                name = self.newtemp("T")
                self.newemit("/", self.words[intop2], self.words[intop1], name)
                self.words[sname] = name
                self.Analy_goto()
            else:
                self.errors = True
        elif state == 19:
            if self.now[1] in ["#", "+", "-", ")", "*", "/"]:
                self.statein.pop()
                self.statein.pop()
                self.statein.pop()
                self.opin.pop()
                intop = self.opin[len(self.opin) - 1]
                self.opin.pop()
                self.opin.pop()
                sname = self.newtemp("Y")
                self.opin.append(sname)
                self.words[sname] = self.words[intop]
                self.Analy_goto()
            else:
                self.errors = True
        else:
            self.errors = True

    def Analy_goto(self):
        state = self.statein[len(self.statein) - 1]
        si = self.opin[len(self.opin) - 1]
        sii = si[0]
        if state == 0:
            if sii == "E":
                self.statein.append(1)
            elif sii == "X":
                self.statein.append(3)
            elif sii == "Y":
                self.statein.append(4)
            else:
                self.errors = True
        elif state == 2:
            if sii == "X":
                self.statein.append(10)
            elif sii == "Y":
                self.statein.append(11)
            else:
                self.errors = True
        elif state == 5:
            if sii == "E":
                self.statein.append(14)
            elif sii == "X":
                self.statein.append(3)
            elif sii == "Y":
                self.statein.append(11)
            else:
                self.errors = True
        elif state == 8:
            if sii == "X":
                self.statein.append(15)
            elif sii == "Y":
                self.statein.append(11)
            else:
                self.errors = True
        elif state == 9:
            if sii == "X":
                self.statein.append(16)
            elif sii == "Y":
                self.statein.append(11)
            else:
                self.errors = True
        elif state == 12:
            if sii == "Y":
                self.statein.append(17)
            else:
                self.errors = True
        elif state == 13:
            if sii == "Y":
                self.statein.append(18)
            else:
                self.errors = True
        else:
            self.errors = True

    def express(self):
        self.opin.append("#")
        self.statein.append(0)
        while self.p < len(self.s) and self.errors is False:
            self.Analy_action()

        if self.finish:
            flage = 1
            print(self.words)
            for four in self.fours:
                print(four)
                arg1 = 0
                arg2 = 0
                if flage == 0 or \
                        (str.isalpha(four.num1[0]) and four.num1[0] != 'T'
                         or str.isalpha(four.num2[0]) and four.num2[0] != 'T'):
                    flage = 0
                    print(four)
                else:
                    if four.op[0] == "-" and four.num1[0] == "_":
                        # print(four.res+"="+str(-int(self.res[four.num2])))
                        self.res[four.res] = -(self.res[four.num2])
                        continue
                    elif four.op[0] == "=":
                        self.res[four.res] = float(four.num2)
                        continue
                    if str.isalpha(four.num1[0]):
                        arg1 = self.res[four.num1]
                    else:
                        arg1 = int(four.num1)
                    if str.isalpha(four.num2[0]):
                        arg2 = self.res[four.num2]
                    else:
                        arg2 = int(four.num2)
                    op = four.op
                    result = eval("arg1 {} arg2".format(op))
                    print(four.res+":"+str(result))
                    self.res[four.res] = result
            if flage == 1:
                print(self.res["T" + str(self.count["T"])])
                # print(self.res["T7"])
        else:
            print(self.p)
            print(self.opin)
            print(self.statein)
            for four in self.fours:
                print(four)
            print("Wrong!")

# 四元式
if __name__ == "__main__":
    A = SA(inpath="./case4/input1.txt")
    A.express()
