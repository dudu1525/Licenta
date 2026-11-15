from dataclasses import dataclass
from morphAnalyzer import analyze
from sentenceParser import parseSentenceFromWordFormat, view_tree, structuralTransfer, StructuralTransferAndFlatten
from data import WordFormat
from morphGenerator import GenerateFinalSentence
from shallow_parser import shallow_transfer
#1 morph analyze

#2 structural parse

#3 structural transfer

#4 morph generate and output

def translateSentence(inp: str) -> str:
    listForm = analyze(inp, [])
    words = None

    try:
        tree = parseSentenceFromWordFormat(listForm)
        if tree is None:
            words = shallow_transfer(listForm)
        else:
            romtree = structuralTransfer(tree)
            words = StructuralTransferAndFlatten(romtree)
    except Exception as e:
        print("deep transfer failed")

    finally:
        if words is None:
            words = shallow_transfer(listForm)

    printableSent = GenerateFinalSentence(words)
    printableSent = printableSent.replace("ă", "a")
    printableSent = printableSent.replace("â", "a")
    printableSent = printableSent.replace("î", "i")
    printableSent = printableSent.replace("ș", "s")
    printableSent = printableSent.replace("ț", "t")
    print(printableSent)
    return printableSent

     




#translateSentence("He likes the big cat")
#translateSentence("he likes to eat")
translateSentence("I eat")
#translateSentence("She sees him")
#translateSentence("We want to see the big house in the small village")
#translateSentence("he does nothing")
#translateSentence("are you sure")

#shallow transfer test
translateSentence("I created the big car and the small table")