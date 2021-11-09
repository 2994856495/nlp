import jieba
from 分词.settings import settings, readAllTxt

s=settings()
fp = readAllTxt()
words=[]
for f in fp:
    content = open(f, "r",encoding="utf-8").read().replace("\n","").replace(" ","")
    t=list(jieba.cut(content))
    print(t)
    words.extend(t)
temp = open("data/jieba.txt", "w", encoding="utf-8")
for w in words:
    print(w)
    temp.writelines(w+"\n")