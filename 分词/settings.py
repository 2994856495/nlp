import re
import os

def readAllTxt(fileName="train_txt"):
    fp=os.listdir(fileName)
    for i in range(len(fp)):
        fp[i]=fileName+"\\"+fp[i]
    # print(fp)
    return fp
# readAllTxt()
def is_Chinese(word):
    # return True
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
'''除去标点符号只留中文'''
def readTxt(fileName):
    f=open(fileName,"r",encoding="utf-8").read()
    result_=f.split("\n")
    result=[]
    for s in result_:
        if is_Chinese(s):
            result.append(s)
    return set(result)
def readDicProocess(fileName="./resource/wordlist.Dic",encoding="gbk"):
    '''用字典或者set，不要用列表元组，因为太慢了
    字典几秒钟，列表几小时
    '''
    result = {}
    maxLength=0
    RE = re.compile(r"[0-9 ]+")
    with open(fileName, "r", encoding=encoding) as f:
        res = f.readlines()
        for i in range(1, len(res)):
            temp=res[i].replace("\n", "").split(" ")[-1]
            le_temp=len(temp)
            if le_temp>maxLength:
                maxLength=le_temp
            result[temp]=1
    f.close()
    return result,maxLength

def readFile(fileName="./train_txt/[犬夜叉]奈落夫人的穿越记事-扶华.1772167.txt"):
    with open(fileName,"r",encoding="utf-8") as f:
        sentence=f.read().replace("\n",",").replace(" ","")
        f.close()
    return sentence
class settings():

    filePath="G:\\19040127路琪\\各科作业以及其余要求文档\\自然语言处理\\实验\\实验一\\代码\\result_txt\\"
    fileName=filePath+"(灌高同人)17岁的柠檬茶-夏光明媚的麦田.37925.train_txt"
    resultPath="result\\"
    DicName="wordlist.Dic"
