from dataclasses import dataclass
import json
import re

from fst import createFST, invert, perform_fst_traversal
from posTagger import HiddenMarkovModel, analyzeSentence,read_dataset

formatMapper={
    "ADJ": "<adj>",#adjective
    "ADV": "<adv>",#adverb
    "NOUN": "<n>",#noun
    "VERB": "<vb>",#verb
    "NUM": "<num>", #numeral
    "PRON": "<prn>", #pronoun
    "CCONJ": "<cnj>", #conjunction
    "AUX": "<vb>",#aux verb - >verb
    "DET": "<art>",#determiner, article
    "ADP": "<pr>", #preposition
    "INJ": "<intj>", #interjection
    "PART": "<pr>", #particle
    "PROPN": "<propn>", #proper noun - ill see what i do with this
    "PUNCT": "<punc>", #punctuation
    "SCONJ": "<cnj>", #subordinating conjunction
    "SYM": "<sym>", #symbol
    "X": "<??>", #other
}

@dataclass
class WordFormat:
    lemma: str
    tags: list[str]

def tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z]+', text,re.IGNORECASE)

def transformToListOfStrings(inp: str) -> list[str]:
     return list(inp)

def transformFromListToString(inp: list[str]):
    lemma =""
    tags = []
    for letter in inp:
        if letter[0]!='<':
           lemma+=letter
        else:
            tags+=letter

    return lemma

def returnTagsFromList(inp: list[str]):
    tags = []
    for letter in inp:
        if letter[0]=='<':
            tags.append(letter)
    return tags


##first get each word (tokenization part before this)

#check if already in the lexicon (en)

#apply the inverse fst to try and find its tags and from the outputs, choose an appropiate one, from the lexicon
#^need to define more rules (pl=plural, 3sg = third form singular, )

#then ambiguities this is next given to the POS TAGGER


#input: string
#Output: set of words with associated tags, in the form of a list of WordFormat objects
def analyze(inputString:str, outform):

    finalList = []#final outputed list
    #read english lexicon
    with open("en_lex.json", "r", encoding="utf-8") as file:
        englishLexicon = json.load(file)

    #split into words the sentence
    stringList = tokenize(inputString)
    #create the fst for the analyzer
    fst = createFST()
    analyzerfst = invert(fst)

    sentences = read_dataset("data/en_ewt-ud-train.conllu")
    hmm = HiddenMarkovModel() 
    hmm.computeCountsandProbabilities(sentences)
    predictedPos = hmm.viterbiAlgorithm(stringList)
    print(list(zip(stringList, predictedPos)))


    #take each word from the sentence and pass it to dictionary lookup, fst analyzer and finally pos tagger
    for word,predictedTag in zip(stringList, predictedPos):
        foundString = False
        for entry in englishLexicon.values():
            if entry["lemma"].lower() == word.lower():
                foundString = True
                finalList.append(WordFormat(entry["lemma"], entry["tags"]))    
                break
        if foundString==False:
            wordStrings = transformToListOfStrings(word)
            fstOut = perform_fst_traversal(analyzerfst, wordStrings)
            if len(fstOut)==1:#one possibility, most likely not in the lexicons, statistic information gotten from the pos tagger, so basic part of speech

                analyzedWord = fstOut[0]
                wordFormat = transformFromListToString(analyzedWord)
                finalList.append(WordFormat(wordFormat, formatMapper[predictedTag]))

            
            elif len(fstOut)>1: #more versions for the word, take the one that matches the pos tagger
                wordWithTag = False
                for i in fstOut:
                    if len(i[-1])>1:
                        wordWithTag=True
                        break
                #given a word with tag was found, it is taken as priority
                if wordWithTag==True: 
                    for i in fstOut:
                        if len(i[-1])>1:
                            normalWord = transformFromListToString(i)#transform to normal string
                            #print(normalWord)
                            foundTagForSingleWord = hmm.viterbiAlgorithm([normalWord])
                            #print(formatMapper[foundTagForSingleWord[0]] + i[-1] + predictedTag)
                            lastTag = i[-1]
                            #match between the found tag from the pos tagger, the found tag from the fst analyzer and from a second pos 
                            if lastTag == formatMapper[foundTagForSingleWord[0]] and lastTag == formatMapper[predictedTag]:
                              
                                finalList.append(WordFormat(normalWord, returnTagsFromList(i)))
                                break

    
    return finalList

   
finallist=analyze("I like cats", [])
print(finallist )