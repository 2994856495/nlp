import concurrent.futures

from 分词.settings import *
import re

s = settings()
'''需要将文章分割'''


def FMM_result(fileName):
    result = ""
    sentence = readFile(fileName)
    Dict, maxLength = readDicProocess()
    sentence = re.split("，|。|：|！|？", sentence)
    for s in sentence:
        result += FMM(s, Dict, maxLength,t=0)
    # sentence=sentence.split("\n")
    return result


'''正向最大匹配算法'''


def FMM(sentence, Dict, maxLength,t=1):
    result = ""
    end = len(sentence)
    position = 0  #
    first = 0  # 第一位
    last = maxLength  # 第二位

    while first != end:
        last = maxLength + first
        if last > end:
            last = end
        tempLen = 0
        for i in range(maxLength):
            if (sentence[first:last - tempLen] in Dict) or (len(sentence[first:last - tempLen]) == 1):
                # result.append(sentence[first:last-tempLen])
                # 防止影响我调试MMSEG程序
                if t==0:
                    print(sentence[first:last - tempLen], end='/')
                result += sentence[first:last - tempLen] + "\n"
                first = last - tempLen
                break
            tempLen += 1
    return result

    # print(result)


def save():
    fp = readAllTxt()
    result = ""
    for f in fp:
        result += FMM_result(f)
    with open(".\data\FMM.txt", "w", encoding="utf-8") as f:
        f.write(result)
        f.close()


if __name__ == '__main__':
    save()
    pass
