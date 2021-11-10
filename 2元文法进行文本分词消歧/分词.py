import re
from 二元文法 import *

import jieba

"""
以下代码和上次一模一样,除了save函数稍微有所变化
"""
seq = " "


def readTxt(filename="txt/1998人民日报.txt"):
    with open(filename, "r", encoding='utf-8') as f:
        reader = f.read()
        reader = reader.split("\n")
    return reader


def read_dict():
    """
    读取词典
    """
    f = open("txt/words.dic", "r", encoding="gbk").read()
    result = f.split("\n")
    maxLength = 0
    for r in result:
        if maxLength < len(r):
            maxLength = len(r)
    return dict(zip(result, range(len(result)))), maxLength


def BMM(sentence, Dict, maxLength):
    """
    和上次一模一样
    """
    result = ""
    end = len(sentence)
    last = end  # 第二位
    while last != 0:
        first = last - maxLength
        if first < 0:
            first = 0
        tempLen = 0
        for i in range(maxLength):
            if (sentence[first + tempLen:last] in Dict) or (len(sentence[first + tempLen:last]) == 1):
                print(sentence[first + tempLen:last], end='/')
                temp = sentence[first + tempLen:last]
                temp = temp[::-1]
                result += seq + temp
                last = first + tempLen
                break
            tempLen += 1

    return "@ " + result[::-1] + "@" + "\n"


def FMM(sentence, Dict, maxLength):
    """
     和上次一模一样
     """
    result = ""
    end = len(sentence)
    first = 0  # 第一位
    while first != end:
        last = maxLength + first
        if last > end:
            last = end
        tempLen = 0
        for i in range(maxLength):
            if (sentence[first:last - tempLen] in Dict) or (len(sentence[first:last - tempLen]) == 1):
                print(sentence[first + tempLen:last], end='/')
                result += sentence[first:last - tempLen] + seq
                first = last - tempLen
                break
            tempLen += 1
    return "@ " + result + "@" + "\n"


def disambiguation_result():
    """
    根据fmm.txt和bmm.txt
    单独进行消除歧义
    """
    result = read_txt()
    # word_frequency = (open("txt/词频.txt", "r", encoding="utf-8").read())
    word_frequency = json.load(open("txt/词频.json", "r", encoding="utf-8"))
    f = open("fmm.txt", "r", encoding='utf-8').readlines()
    b = open("bmm.txt", "r", encoding='utf-8').readlines()
    n = ""
    num = len(f)
    for i in range(num):
        if f[i] != b[i]:
            temp = compare_sentence_probability(f[i].strip("\n"), b[i].strip("\n"), result, word_frequency)
            n += temp + "\n"
            n_temp = str(get_sentence_probability(temp, result, word_frequency))
            print("{}:{}:{}:{}".format(i, num, n_temp, temp))
        else:
            n += f[i] + "\n"

    open("txt/消歧结果.txt", "w", encoding='utf-8').write(n)
    pass


def test():
    """
    求给定文本每段话概率，没想好函数名字
    """
    result = read_txt()
    word_frequency = json.load(open("txt/词频.json", "r", encoding="utf-8"))
    f = open("txt/test.txt", "r", encoding='utf-8').readlines()
    p = ""
    for i in f:
        i=i.strip("\n")
        p += i + "\t\t" + str(get_sentence_probability(i, result, word_frequency)) + "\n"
    open("txt/每段话概率.txt", "w", encoding='utf-8').write(p)
    pass


def save():
    """
    fmm和bmm分词
    """
    txt = readTxt("txt/1.txt")
    # result = read_txt()
    # word_frequency = json.loads(open("txt/词频.json","r",encoding="utf-8"))

    Dict, maxLength = read_dict()
    f = ""
    b = ""
    # j = ""
    # n = ""
    # p = ""
    for t in txt:
        f_temp = FMM(t, Dict, maxLength)
        b_temp = BMM(t, Dict, maxLength)
        f += f_temp
        b += b_temp
        # n += compare_sentence_probability(f_temp, b_temp, result, word_frequency)
        # p += str(get_sentence_probability(t, result, word_frequency)) + "\n"
        # temp = list(jieba.cut(t))
        # print(temp)
        # j += "@ " + seq.join(temp) + " @" + "\n"
    open("fmm.txt", "w", encoding='utf-8').write(f)
    open("bmm.txt", "w", encoding='utf-8').write(b)
    # open("txt/jieba.txt", "w", encoding='utf-8').write(j)
    # open("txt/消歧结果.txt", "w", encoding='utf-8').write(n)
    # open("txt/测试语料每段话概率.txt", "w", encoding='utf-8').write(p)
    pass


if __name__ == '__main__':
    save()
