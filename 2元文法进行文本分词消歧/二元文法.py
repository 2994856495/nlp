# EOS   BOS
import re
import json

seq = " "


def read_txt(fileName="txt/1998人民日报（分词）.txt"):
    """
    具体内容参照jieba库结果
    读取文件，并按照换行，除去开头结尾的@相当于EOS BOS
    """
    result = []
    f = open(fileName, "r", encoding='utf-8')
    for line in f:
        result.extend(line.replace("\n", "").replace("@", "").split(" "))
    f.close()
    return result


def get_word_probability(result):
    """
    求word在res出现次数，默认加一法,并且存入相关文件
    word 词语
    res 为jieba分词结果，为一维列表
    temp 存储已经出现过的词语,key为词，value为词频数（str）
    """
    list_res = seq.join(result)
    temp = {}
    count = len(result)
    for i in range(1, count):
        if result[i] == "" or result[i] == "\n":
            continue
        if result[i] not in temp:
            temp[result[i]] = str(len(re.findall(result[i], list_res)) + 1)
        temp_word = (str(result[i - 1]) + seq + str(result[i]))
        if temp_word not in temp:
            temp[temp_word] = str(len(re.findall(temp_word, list_res)) + 1)
        print("{}:{}:{}".format(result[i], i, count))
    f = open("txt/词频.json", "w", encoding="utf-8")
    p_one = json.dumps(temp)
    f.write(p_one)


def get_sentence_probability(sentence, result, word_frequency):
    """
    sentence 默认为列表,表示一段话、一句话
    res 为jieba分词结果，为一维列表
    word_num 表示文本词语总数
    求某一个句子分出的结果概率
    其中的总数目为jieba分词的结果，也是老师给的文本的结果
    """
    # print(type(word_frequency), type(result))
    sentence = sentence.split(" ")
    word_num = len(set(result))
    P = 1
    for i in range(1, len(sentence)):
        # 预防词语不在json里
        temp_word = (str(sentence[i - 1]) + seq + str(sentence[i]))
        if temp_word not in word_frequency:
            word_frequency[temp_word] = 1
        if sentence[i] not in word_frequency:
            word_frequency[sentence[i]] = 1
        P *= float(word_frequency[temp_word]) / (float(word_frequency[sentence[i]]) + float(word_num))
    return P


def compare_sentence_probability(sentence_1, sentence_2, result, word_frequency):
    """
    比较歧义的两个句子的概率，选最好的一个
    """
    return sentence_1 if get_sentence_probability(sentence_1, result, word_frequency) > get_sentence_probability(
        sentence_2,
        result, word_frequency) else sentence_2

# res = read_txt("txt/jieba.txt")
# get_word_probability(res)
