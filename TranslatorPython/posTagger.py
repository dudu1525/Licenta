from collections import Counter
import math


#read connlu file
def read_dataset(filestr:str):
    sentences = []
    current_sentence = []
    file = open(filestr, encoding="utf-8")
    for current_line in file:
        if current_line.startswith('#'):
            continue
        if not current_line.strip():
            if current_sentence:
                sentences.append(current_sentence)
                current_sentence=[]
            continue

        columns =current_line.rstrip().split("\t")
        if len(columns) == 10 and "-" not in columns[0] and "." not in columns[0]:
            current_sentence.append((columns[1].lower(), columns[3]))
    file.close()
    return sentences

#sents =read_dataset("dataset.conllu")

class HiddenMarkovModel:
    def __init__(self):
        #tags from the corpus
        self.tags = set()
        #words in the corpus
        self.words = set()

        #counter for C(ti-1, ti) or C(ti) tag preceedence counter
        self.transitionCount = Counter()
        #counter for C(wi|ti), for a given word, how many times its each tag
        self.wordTagCount = Counter()
        #count nr of individual tags
        self.tagCount=Counter()
        #probability P(ti|ti-1)
        self.transitionProb = {}
        #probability P(wi|ti)
        self.wordtagProb = {}

    def computeCountsandProbabilities(self, sentences):
        #compute counts
        for sentence in sentences:
            prevTag='<S>'
            self.tagCount['<S>'] += 1
            for word,tag in sentence:
                self.tags.add(tag)
                self.words.add(word)
                self.transitionCount[(prevTag,tag)]+=1
                self.wordTagCount[(tag,word)]+=1
                self.tagCount[tag]+=1
                prevTag=tag
        self.transitionCount[(prevTag,'<E>')]+=1

        #compute probabilities (take log for each probability to avoid underflow)
        #emission prob ( P(wi|ti) )
        for (tag, word), count in self.wordTagCount.items():
            prob = count / self.tagCount[tag]
            self.wordtagProb[(tag, word)] = math.log(prob)
        #transition prob ( P(ti|ti-1) )
        for (prevTag, tag), count in self.transitionCount.items():
            prob = count / self.tagCount[prevTag]
            self.transitionProb[(prevTag, tag)] = math.log(prob)

    def getEmissionProbability(self, tag, word):
        word = word.lower()
        if (tag, word) in self.wordtagProb:
            return self.wordtagProb[(tag, word)]
        #if not found
        return math.log(1e-8)

    def getTransitionProbability(self, prev_tag, tag):
        if (prev_tag, tag) in self.transitionProb:
            return self.transitionProb[(prev_tag, tag)]


    def viterbiAlgorithm(self, sentence):
