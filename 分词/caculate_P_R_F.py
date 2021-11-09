
from 分词.settings import readTxt
class test():
    def __init__(self):
        pass
    def prepare(self):
        pass
    pass
class caculate():
    def __init__(self,filename):
        #
        # jieba分词的结果
        self.true_correct_txt = readTxt("./data/jieba.txt")
        self.true_correct_num =len(self.true_correct_txt)
        # 这一步将列表转为字典，因为字典查询较快
        self.true_correct_dic=self.changeIntoDic(self.true_correct_txt)
        # 样本信息条数（除去标点符号，只保留中文）
        self.sample_num_txt=readTxt(filename)
        self.sample_num=len(self.sample_num_txt)

        self.my_correct_txt = self.getMyCorrectNum()
        self.my_correct_num = len(self.my_correct_txt)

        self.Precision= self.caculatePrecision()
        self.Recall= self.caculateRecall()
        self.FScore= self.caculateFScore()
        pass

    def changeIntoDic(self,txt):
        result={}
        for t in txt:
            result[t]=1
        return result

    def getMyCorrectNum(self):
        result=[]
        for s in self.sample_num_txt:
            if s in self.true_correct_dic:
                result.append(s)
        return result

    def caculatePrecision(self):
        return self.my_correct_num/self.true_correct_num

    def caculateRecall(self):
        return self.my_correct_num / self.sample_num

    def caculateFScore(self):
        return (2*self.Precision*self.Recall)/(self.Precision+self.Recall)
if __name__ == '__main__':
    print("FMM：")
    fmm=caculate("./data/FMM.txt")
    print("Precision:%f,Recall:%f,FScore:%f"%(fmm.Precision,fmm.Recall,fmm.FScore))
    print("BMM：")
    bmm=caculate("./data/BMM.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (bmm.Precision, bmm.Recall, bmm.FScore))
    print("双向最大匹配：")
    two_way=caculate("./data/two_way.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (two_way.Precision, two_way.Recall, two_way.FScore))
    print("mmseg：")
    mmseg = caculate("./data/MMSEG.txt")
    print("Precision:%f,Recall:%f,FScore:%f" % (mmseg.Precision, mmseg.Recall, mmseg.FScore))
