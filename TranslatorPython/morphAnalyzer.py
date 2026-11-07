
import json
import re

from fst import createFST, invert, perform_fst_traversal
from posTagger import HiddenMarkovModel, analyzeSentence,read_dataset
from data import WordFormat
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

##########################################################LOADINGS FOR ANALYZER
with open("lexicons/en_lex.json", "r", encoding="utf-8") as f:
    englishLexicon = json.load(f)

lemmaEntries = {}
for entry in englishLexicon.values():
    lemmaEntries.setdefault(entry["lemma"].lower(), []).append(entry)

analyzerfst = invert(createFST())

hmm = HiddenMarkovModel()
hmm.computeCountsandProbabilities(read_dataset("data/en_ewt-ud-train.conllu"))
###################################################################################

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
        #print(letter)
        if letter[0]=='<':
            tags.append(letter)
    tags[0],tags[-1] = tags[-1], tags[0]
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


    stringList = tokenize(inputString)

    predictedPos = hmm.viterbiAlgorithm(stringList)
   # print(list(zip(stringList, predictedPos)))


    #take each word from the sentence and pass it to dictionary lookup, fst analyzer and finally pos tagger
    for word,predictedTag in zip(stringList, predictedPos):
        foundString = False
        entries = lemmaEntries.get(word.lower())
        if entries:
            entry = entries[0]
            foundString = True
            finalList.append(WordFormat(entry["lemma"], list(entry["tags"])))  
            

        #not a base word in the lexicon, continue with fst analyzer and pos tagger
        if foundString==False:
            wordStrings = transformToListOfStrings(word)
            fstOut = perform_fst_traversal(analyzerfst, wordStrings) #last part of the tags is the part of speech predicted
            #print(fstOut)
            if len(fstOut)==1:#one possibility, most likely not in the lexicons, statistic information gotten from the pos tagger, so basic part of speech

                analyzedWord = fstOut[0]
                wordFormat = transformFromListToString(analyzedWord)
                finalList.append(WordFormat(wordFormat, [formatMapper[predictedTag]]))

            
            elif len(fstOut)>1: #more versions for the word, take the one that matches the pos tagger
                wordWithTag = False
                for i in fstOut:
                    if len(i[-1])>1: #means the last part of the word is with a tag (more chars than 1 last one)
                        wordWithTag=True
                        break
                #given a word with tag was found, it is taken as priority
                foundWithoutLexicon = False #if you find a word that was not in the lexicon, true
                addedAlready = False # if found one with lexicon and was added, marked as true
                if wordWithTag==True: 
                    for i in fstOut:
                       # print (i)
                        if len(i[-1])>1: #this means the last part is a tag
                            normalWord = transformFromListToString(i)#transform to normal string
                           # print(normalWord)
                            foundTagForSingleWord = hmm.viterbiAlgorithm([word]) #check single word, without contex!!!!!!! CHECK THE INITIAL WORD, NOT the one from the fst!!!
                            #print(formatMapper[foundTagForSingleWord[0]] + i[-1] + predictedTag)
                            lastTag = i[-1]
                            #match between the found tag from the pos tagger, the found tag from the fst analyzer and from a second pos 
                            if  lastTag == formatMapper[foundTagForSingleWord[0]] and lastTag == formatMapper[predictedTag]:
                                foundWithoutLexicon=True
                                entries = lemmaEntries.get(normalWord.lower())
                                if entries: #check if the cut word is in the lexicon
                                        addedAlready = True
                                        entry = entries[0]       
                                        finalList.append(WordFormat(normalWord, returnTagsFromList(i)))
                                    

                    if foundWithoutLexicon == True and addedAlready == False: #after inspecting all words, if found some word, but without lexicon, add it
                        analyzedWord = fstOut[0]
                        wordFormat = transformFromListToString(analyzedWord)
                        finalList.append(WordFormat(wordFormat, [formatMapper[predictedTag]]))
    
    return finalList

   
