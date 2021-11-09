'''反向最大匹配算法'''
import os

from 分词.settings import *

s=settings()
def BMM_result(fileName):
    result=""
    sentence = readFile(fileName)
    sentence=re.split("，|。|：|！|？",sentence)
    Dict, maxLength = readDicProocess()
    for s in sentence:
        result+=BMM(s,Dict,maxLength)
    # sentence=sentence.split("\n")
    return result

def BMM(sentence,Dict,maxLength):
    result=""
    end=len(sentence)
    position=0#
    first=end#第一位
    last=end#第二位

    while last!=0:
        first=last-maxLength
        # last=maxLength+first
        if first<0:
            first=0
        tempLen=0
        for i in range(maxLength):
            if (sentence[first+tempLen:last] in Dict) or (len(sentence[first+tempLen:last]) == 1):
                # result.append(sentence[first:last-tempLen])
                print(sentence[first+tempLen:last], end='/')
                result+=sentence[first+tempLen:last]+"\n"
                last = first+tempLen
                break
            tempLen+=1
    return result


def save():
    print(os.getcwd())
    fp=readAllTxt()
    result=""
    for f in fp:
        result+=(BMM_result(f))
    with open(".\\data\\BMM.txt", "w", encoding="utf-8") as f:
        f.write(result)
        f.close()

if __name__ == '__main__':
    save()
    pass