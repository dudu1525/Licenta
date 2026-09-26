from dataclasses import dataclass

@dataclass
class WordFormat:
    lemma: str
    tags: list[str]

##first get each word (tokenization part before this)

#check if already in the lexicon (en)

#apply the inverse fst to try and find its tags and from the outputs, choose an appropiate one, from the lexicon
#^need to define more rules (pl=plural, 3sg = third form singular, )

#then ambiguities this is next given to the POS TAGGER


#input: string
#Output: 
def analyze(inputString:str, outform):

    
    print("NICE")