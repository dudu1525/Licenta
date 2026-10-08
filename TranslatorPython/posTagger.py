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
        return math.log(1e-8)

    def viterbiAlgorithm(self, sentence):
        sentence = [word.lower() for word in sentence]
        if sentence[-1] != ".":
            sentence.append(".")

        word_tags_table = []
        backpointer_table = []
        #compute the table with the scores for the first word in the sentence that should be preceeded by <S>
        first_word_scores = {}
        first_word_backpointer = {}
        for tag in self.tags:
            transition_prob = self.getTransitionProbability('<S>', tag)
            emission_prob = self.getEmissionProbability(tag, sentence[0])
            #addition because of the way the probabilites are stored, as log form
            first_word_scores[tag] = transition_prob + emission_prob
            first_word_backpointer[tag] = '<S>' #Visualized as a graph, from the S, it goes forward for each tag, with its computed probability and backpointer to S
        
        word_tags_table.append(first_word_scores)
        backpointer_table.append(first_word_backpointer)
        #computing best scores for the rest of the words.
        for i in range(1, len(sentence)):
            current_word_scores = {}
            current_word_backpointer = {}
            for tag in self.tags:
                best_score = float('-inf')
                best_prev_tag = None
                for prev_tag in self.tags:
                    transition_prob = self.getTransitionProbability(prev_tag, tag) #probability of ti-1, ti given the previous tag
                    emission_prob = self.getEmissionProbability(tag, sentence[i])#probability for a tag, given the word
                    score = word_tags_table[i - 1][prev_tag] + transition_prob + emission_prob
                    if score > best_score:
                        best_score = score
                        best_prev_tag = prev_tag
                #for each tag, store the best score and the backpointer to the previous tag that gave that score
                current_word_scores[tag] = best_score
                current_word_backpointer[tag] = best_prev_tag
            #store for each new word, the scores and backpointers for each tag
            word_tags_table.append(current_word_scores)
            backpointer_table.append(current_word_backpointer)

        #final tag with <E> transition
        best_final_score = float('-inf')
        best_final_tag = None
        for tag in self.tags:
            score = word_tags_table[-1][tag] + self.getTransitionProbability(tag, '<E>')
            if score > best_final_score:
                best_final_score = score
                best_final_tag = tag

        #reconstructing the path
        best_path = [best_final_tag]
        for i in range(len(sentence) - 1, 0, -1):
            best_prev_tag = backpointer_table[i][best_path[-1]]
            best_path.append(best_prev_tag)

        best_path.reverse()
        del best_path[-1]#remove added punctuation
        return best_path

def analyzeSentence(sentence):
    sentences = read_dataset("data/en_ewt-ud-train.conllu")
    hmm = HiddenMarkovModel() 
    hmm.computeCountsandProbabilities(sentences)
    return hmm.viterbiAlgorithm(sentence)



def test_hmm():
    sentences = read_dataset("data/en_ewt-ud-train.conllu")
    hmm = HiddenMarkovModel()

    hmm.computeCountsandProbabilities(sentences)
   # print (hmm.tags)
   # print("sentence")
    test_sentence = ["boxe"]
    predicted_tags = hmm.viterbiAlgorithm(test_sentence)
    print(list(zip(test_sentence, predicted_tags)))

#test_hmm()