#morph generator using lexicons and suffix rules, no fst as it would take too many rules
#given how nuanced romanian is

from typing import List

from data import WordFormat
IRREGULAR_VERBS = {
    "fi":     {"<p1>": "sunt", "<p2>": "ești", "<p3>": "este", "<conj>": "fie"},
    "vrea":   {"<p1>": "vreau", "<p2>": "vrei", "<p3>": "vrea", "<conj>": "vrea"},
    "vedea":  {"<conj>": "vadă"},
    "mânca":  {"<conj>": "mănânce"},
    "plăcea": {"<3pl>": "plac", "<conj>": "placă"}
}

#rules:

#prepositions, conjunctions,  remain the same

#handling <def> (definite) article by adding desired suffixes

#verbs in the conjunctive case rules

#different rules for time of verbs, based on mood

#adjectives must match corresponding noun
def generate_noun(wf: WordFormat) -> str:
    lemma = wf.lemma
    tags = set(wf.tags)

    if "<def>" in tags: #definite noun rule
        if "<f>" in tags and "<sg>" in tags:
            if lemma.endswith("ă"):
                return lemma[:-1] + "a" #change the last letter to 'a'
            elif lemma.endswith("e"):
                return lemma + "a" #add 'a'
        if ("<m>" in tags or "<nt>" in tags) and "<sg>" in tags:
            if lemma.endswith("e"):
                return lemma + "le"
            return lemma + "ul"
        if "<pl>" in tags:
            return lemma + "le"

    return lemma

def generate_verb(wf: WordFormat) -> str:
    lemma = wf.lemma 
    tags = set(wf.tags)

    #irregular check
    if lemma in IRREGULAR_VERBS:
        iregform = IRREGULAR_VERBS[lemma]
        if "<conj>" in tags and "<conj>" in iregform:
            return iregform["<conj>"]
        if "<3pl>" in tags and "<3pl>" in iregform:
            return iregform["<3pl>"]
        for p in ["<p1>", "<p2>", "<p3>"]:
            if p in tags and p in iregform:
                return iregform[p]

    #normal verbs
    

    #subjonctive rules:
    if "<conj>" in tags:
        if lemma.endswith("a"):
            return lemma[:-1] + "e"  
        elif lemma.endswith("i"):
            return lemma[:-1] + "ească" 
        elif lemma.endswith("e"):
            return lemma[:-1] + "ă"  
    #kind of fall back for now
    return lemma


def GenerateFinalSentence(inputWords: List[WordFormat])->str:

    finalSentence = []
    for word in inputWords:
        wordTags = word.tags

        if "<cnj>" in wordTags or "<pr>" in wordTags or "<art>" in wordTags:
            finalSentence.append(word.lemma)
        elif "<n>" in wordTags: 
            finalSentence.append(generate_noun(word))
        elif "<vb>" in wordTags:
            finalSentence.append(generate_verb(word))
        else:
            finalSentence.append(word)

    return finalSentence