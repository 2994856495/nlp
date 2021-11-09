'''
双向最大匹配算法 消除歧义
因为单独的正向或者反向存在歧义，所以使用双向来分词，
思路：对同一句话进行正向和反向分词得到结果，比较取得的结果，长度较短的。比较两者在词典中的词的数目，取较多的那种
但计算CRF时,效果不大
'''
from 分词.settings import *
from 分词.FMM import FMM
from 分词.BMM import BMM
s=settings()
def two_way_result(fileName):
    result=""
    sentence = readFile(fileName)
    sentence=re.split("，|。|：|！|？",sentence)
    Dict, maxLength = readDicProocess()
    for s in sentence:
        result+=two_way(s,Dict, maxLength)
    # sentence=sentence.split("\n")
    return result
def two_way(sentence,Dict, maxLength):
    FMM_word=FMM(sentence,Dict, maxLength)
    BMM_word=BMM(sentence,Dict, maxLength)
    if len(FMM_word) < len(BMM_word):
        return FMM_word
    elif len(FMM_word) > len(BMM_word):
        return BMM_word
    else:
        if count_single_char(FMM_word) < count_single_char(BMM_word):
            return FMM_word
        else:
            return BMM_word
def count_single_char(words):
    cnt = 0
    for word in words:
        if len(word) == 1:
                   cnt += 1
    return cnt
def save():
    fp = readAllTxt()
    result = ""
    for f in fp:
        result+=two_way_result(f)
    with open("./data/two_way.txt", "w", encoding="utf-8") as f:
        f.write(result)
        f.close()

if __name__ == '__main__':
    save()
    pass