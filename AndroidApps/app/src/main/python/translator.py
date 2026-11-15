from dataclasses import dataclass
from morphAnalyzer import analyze
from sentenceParser import parseSentenceFromWordFormat, view_tree, structuralTransfer, StructuralTransferAndFlatten
from data import WordFormat
from morphGenerator import GenerateFinalSentence

#1 morph analyze

#2 structural parse

#3 structural transfer

#4 morph generate and output

def translateSentence(inp: str):
    listForm = analyze(inp, [])
    #print(listForm)
    tree =parseSentenceFromWordFormat(listForm)
    if tree==None:#unsucessful, shallow transfer then morph transfer and generation
         print("parse failed!!!!")
    
    #also need to put a catch block here to do shallow analyzing
    else:#continue with structural morph transfer then generation
         #view_tree(tree) 
         romtree =structuralTransfer(tree)
        # view_tree(romtree)
        # print("NOW TRANSFORMED TREE")
         words = StructuralTransferAndFlatten(romtree)
        # for wf in words:
         #   print(wf)
         #print("generated")
         printableSent = GenerateFinalSentence(words)
         printableSent.replace("ă", "a")
         printableSent.replace("â", "a")
         printableSent.replace("î", "i")
         printableSent.replace("ș", "s")
         printableSent.replace("ț", "t")
         printableSent.replace("Ă", "A")
         printableSent.replace("Â", "A")
         printableSent.replace("Î", "I")
         printableSent.replace("Ș", "S")
         printableSent.replace("Ț", "T")
         return printableSent
         #print(finalSentt)

     




#translateSentence("He likes the big cat")
#translateSentence("he likes to eat")
#translateSentence("I eat")
#translateSentence("She sees him")
#translateSentence("We want to see the big house in the small village")
#translateSentence("he does nothing")