# from 二元文法 import read_txt


class caculate():
    """
    和上次一模一样
    """

    def __init__(self, filename):
        #
        # jieba分词的结果
        self.true_correct_txt = self.read_txt("./txt/jieba.txt")
        self.true_correct_num = sum([len(i) for i in self.true_correct_txt])
        # len(self.true_correct_txt)
        # 样本信息条数
        self.sample_num_txt = self.read_txt(filename)
        self.sample_num = sum([len(i) for i in self.sample_num_txt])
        self.my_correct_txt = self.getMyCorrectNum()
        self.my_correct_num = sum([len(i) for i in self.my_correct_txt])
        self.Precision = self.caculatePrecision()
        self.Recall = self.caculateRecall()
        self.FScore = self.caculateFScore()

        pass

    def read_txt(self, filename):
        result = []
        f = open(filename, "r", encoding='utf-8')
        for line in f:
            result.append(line.replace("@", "").split("\n"))
        result = [i[0].split(" ") for i in result]
        result = [i[1:-1] for i in result]
        f.close()
        return result

    def changeIntoDic(self, txt):
        result = {}
        for t in txt:
            result[t] = 1
        return result

    def getMyCorrectNum(self):
        result = []
        for i in range(len(self.true_correct_txt)):
            temp = []
            for x in self.sample_num_txt[i]:
                if x in self.true_correct_txt[i]:
                    temp.append(x)
            result.append(temp)
        return result

    def caculatePrecision(self):
        return self.my_correct_num / self.true_correct_num

    def caculateRecall(self):
        return self.my_correct_num / self.sample_num

    def caculateFScore(self):
        return (2 * self.Precision * self.Recall) / (self.Precision + self.Recall)


if __name__ == '__main__':
    print("FMM：")
    fmm = caculate("./txt/fmm.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (fmm.Precision, fmm.Recall, fmm.FScore))
    print("BMM：")
    bmm = caculate("./txt/bmm.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (bmm.Precision, bmm.Recall, bmm.FScore))
    print("消除歧义后的：")
    two_way = caculate("./txt/消歧结果.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (two_way.Precision, two_way.Recall, two_way.FScore))
