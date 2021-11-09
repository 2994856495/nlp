#-*- coding: utf-8 -*-
import string
import re

from 分词.settings import readFile, readDicProocess, readAllTxt
from 分词.FMM import FMM

sentence = readFile()
Dict, maxLength = readDicProocess()
class Word:
	def __init__(self, text = '', freq = 0):
		self.text = text
		self.freq = freq
		self.length = len(text)
class Chunk:
	def __init__(self, w1, w2 = None, w3 = None):
		self.words = []
		self.words.append(w1)
		if w2:
			self.words.append(w2)
		if w3:
			self.words.append(w3)
	# 计算chunk的总长度
	def totalWordLength(self):
		length = 0
		for word in self.words:
			length += len(word.text)
		return length
	# 计算平均长度
	def averageWordLength(self):
		return float(self.totalWordLength()) / float(len(self.words))
	# 计算标准差
	def standardDeviation(self):
		average = self.averageWordLength()
		sum = 0.0
		for word in self.words:
			tmp = (len(word.text) - average)
			sum += float(tmp) * float(tmp)
		return sum
	# 自由语素度
	def wordFrequency(self):
		sum = 0
		for word in self.words:
			sum += word.freq
		return sum
class ComplexCompare:
	def takeHightest(self, chunks, comparator):
		i = 1
		for j in range(1, len(chunks)):
			rlt = comparator(chunks[j], chunks[0])
			if rlt > 0:
				i = 0
			if rlt >= 0:
				chunks[i], chunks[j] = chunks[j], chunks[i]
				i += 1
		return chunks[0: i]

	# 以下四个函数是mmseg算法的四种过滤原则，核心算法
	def mmFilter(self, chunks):
		def comparator(a, b):
			return a.totalWordLength() - b.totalWordLength()
		return self.takeHightest(chunks, comparator)

	def lawlFilter(self, chunks):
		def comparator(a, b):
			return a.averageWordLength() - b.averageWordLength()
		return self.takeHightest(chunks, comparator)
	
	def svmlFilter(self, chunks):
		def comparator(a, b):
			return a.standardDeviation() - b.standardDeviation()
		return self.takeHightest(chunks, comparator)

	def logFreqFilter(self, chunks):
		def comparator(a, b):
			return a.wordFrequency() - b.wordFrequency()
		return self.takeHightest(chunks, comparator)
# 加载词组字典和字符字典
dictWord = {}
maxWordLength = 0
def loadDictChars(filepath):
	global maxWordLength
	f = open(filepath,encoding="utf-8",errors='ignore')
	for line in f.readlines():
		word, freq = line.split(' ')
		word = word.strip()
		dictWord[word] = (len(word), int(freq))
		maxWordLength = maxWordLength < len(word) and len(word) or maxWordLength
	f.close()
def loadDictWords(filepath):
	global maxWordLength
	f = open(filepath,encoding='gbk+')
	for line in f.readlines():
		word = line.strip()
		dictWord[word] = (len(word), 0)
		maxWordLength = maxWordLength < len(word) and len(word) or maxWordLength
	f.close()
# 判断该词word是否在字典dictWord中
def getDictWord(word):
	result = dictWord.get(word)
	if result:
		return Word(word, result[1])
	return None
# 开始加载字典
def run():
	from os.path import join, dirname
	loadDictChars("./resource/chars.dic")
	print ("loadDictChars Done!")
	loadDictWords("resource/words.dic")
	print ("loadDictWords Done!")
class Analysis:
	def __init__(self, text):
		self.text = text
		self.cacheSize = 3
		self.pos = 0
		self.textLength = len(self.text)
		self.complexCompare = ComplexCompare()
		# 控制字典只加载一次
		if not dictWord:
			run()

	def __iter__(self):
		while True:
			token = self.getNextToken()
			if token == None:
				return
				# raise StopIteration
			yield token

	def getNextChar(self):
		return self.text[self.pos]

	# 判断该字符是否是中文字符（不包括中文标点）
	def isChineseChar(self, charater):
		return 0x4e00 <= ord(charater) < 0x9fa6

	# 判断是否是ASCII码
	def isASCIIChar(self, ch):
		if ch in string.whitespace:
			return False
		if ch in string.punctuation:
			return False
		return ch in string.printable
	# 判断是否为其他字符
	def isOtherChar(self,ch):
		return not (self.isChineseChar(ch) and self.isASCIIChar(ch) )
	# 得到下一个切割结果
	def getNextToken(self):
		while self.pos < self.textLength:
			if self.isChineseChar(self.getNextChar()):
				token = self.getChineseWords()
				if token =="":
					self.pos += 1
			else:
				token = self.getASCIIWords() + '/'
			if token == "/":
				self.pos += 1
			if len(token) >= 0:
				return token
		return None

	# 切割出非中文词
	def getASCIIWords(self):
		while self.pos < self.textLength:
			ch = self.getNextChar()
			if self.isASCIIChar(ch) or self.isChineseChar(ch):
				break
			self.pos += 1
		# 得到英文单词的起始位置
		start = self.pos
		# 找出英文单词的结束位置
		while self.pos < self.textLength:
			ch = self.getNextChar()
			if not self.isASCIIChar(ch):
				break
			self.pos += 1
		end = self.pos
		# 返回英文单词
		return self.text[start: end]

	# 切割出中文词，并且做处理，用上述4种方法
	def getChineseWords(self):
		chunks = self.createChunks()
		if len(chunks) > 1:
			chunks = self.complexCompare.mmFilter(chunks)
			chunks = self.complexCompare.lawlFilter(chunks)
			chunks = self.complexCompare.svmlFilter(chunks)
			chunks = self.complexCompare.logFreqFilter(chunks)
		if len(chunks) == 0:
			return ''
		word = chunks[0].words
		token = ""
		length = 0
		for x in word:
			if x.length != -1:
				token += x.text + "/"
				length += len(x.text)
		self.pos += length
		return token

	# 三重循环来枚举切割方法，这里也可以运用递归来实现
	def createChunks(self):
		chunks = []
		originalPos = self.pos
		words1 = self.getMatchChineseWords()
		for word1 in words1:
			self.pos += len(word1.text)
			if self.pos < self.textLength:
				words2 = self.getMatchChineseWords()
				for word2 in words2:
					self.pos += len(word2.text)
					if self.pos < self.textLength:
						words3 = self.getMatchChineseWords()
						for word3 in words3:
							if word3.length == -1:
								chunk = Chunk(word1, word2)
							else:
								chunk = Chunk(word1, word2, word3)
							chunks.append(chunk)
					elif self.pos == self.textLength:
						chunks.append(Chunk(word1, word2))
					self.pos -= len(word2.text)
			elif self.pos == self.textLength:
				chunks.append(Chunk(word1))
			self.pos -= len(word1.text)

		self.pos = originalPos
		return chunks


	# 运用正向最大匹配算法结合字典来切割中文文本和其他文本
	def getMatchChineseWords(self):
		originalPos = self.pos
		words = []
		index = 0
		while self.pos < self.textLength:
			if index >= maxWordLength:
				break
			self.pos += 1
			index += 1
			text = self.text[originalPos: self.pos]
			word = getDictWord(text)
			if word:
				words.append(word)

		self.pos = originalPos
		# 没有词则放置个‘X’，将文本长度标记为-1
		if not words:
			word = Word()
			word.length = -1
			word.text = 'X'
			words.append(word)
		return words

def cuttest(text):
	wlist = [word for word in Analysis(text)]
	tmp = ""
	for w in wlist:
		tmp += w
	print(tmp)
	return "\n".join([r for r in re.split("/|//",tmp) if r!=""])
def Mmseg(fileName):
	result = ""
	sentence = readFile(fileName)
	# Dict, maxLength = readDicProocess()
	sentence = re.split("～|~|\"|，|。|;|；|：|！|？|—|丨|（|）", sentence)
	for i in range(len(sentence)):
		print(f"{i}:{sentence[i]}")
		result += cuttest(sentence[i])
	# sentence=sentence.split("\n")
	return result
def save():
	fp = readAllTxt()
	for f in fp:
		result = Mmseg(f)
	#print(result)
		with open(".\data\MMSEG.txt", "a+", encoding="utf-8") as f:
			f.write(result)
			f.close()
save()