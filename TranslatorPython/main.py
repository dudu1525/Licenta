
import re

def tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z]+', text.lower())

def transformToListOfStrings(inp: str) -> list[str]:
     return list(inp)

def transformFromListToString(inp: list[str])->str:
    return "".join(inp)


#tokenize text

#send tokenized text to analyzer
#use pos tagger for disambiguation

#try to create a parse tree with current sentence

#create structure in romanian either by deep or shallow syntactic trasnfer

#generate the words via morph generator

#output translated sentence


def translateSentence(inp:str )->str:
    finalString=""
    str = "i Don't like this"
    words = tokenize(str)
    print(words)


    return finalString

translateSentence("da")