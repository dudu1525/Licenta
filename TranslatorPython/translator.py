from dataclasses import dataclass
from morphAnalyzer import analyze
from sentenceParser import parseSentenceFromWordFormat, view_tree, structuralTransfer
@dataclass
class WordFormat:
    lemma: str
    tags: list[str]


#1 morph analyze

#2 structural parse

#3 structural transfer

#4 morph generate and output

def translateSentence(inp: str):
    listForm = analyze(inp, [])
    print(listForm)
    tree =parseSentenceFromWordFormat(listForm)
    if tree==None:#unsucessful, shallow transfer then morph transfer and generation
         print("parse failed!!!!")
    else:#continue with structural morph transfer then generation
         view_tree(tree) 
         romtree =structuralTransfer(tree)
         view_tree(romtree)


     




translateSentence("I like the good cat")