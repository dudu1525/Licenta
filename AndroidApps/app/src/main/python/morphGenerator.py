#morph generator using lexicons and suffix rules, no fst as it would take too many rules
#given how nuanced romanian is

from typing import List

from data import WordFormat
IRREGULAR_VERBS = {
    "vrea": {
        "ind":  {"<p1><sg>": "vreau", "<p2><sg>": "vrei",   "<p3><sg>": "vrea",
                 "<p1><pl>": "vrem",  "<p2><pl>": "vreți",  "<p3><pl>": "vor"},
        "conj": {"<p1><sg>": "vreau", "<p2><sg>": "vrei",   "<p3><sg>": "vrea",
                 "<p1><pl>": "vrem",  "<p2><pl>": "vreți",  "<p3><pl>": "vrea"}
    },
    "fi": {
        "ind":  {"<p1><sg>": "sunt", "<p2><sg>": "ești",   "<p3><sg>": "este",
                 "<p1><pl>": "suntem","<p2><pl>": "sunteți","<p3><pl>": "sunt"},
        "conj": {"<p1><sg>": "fiu",  "<p2><sg>": "fii",    "<p3><sg>": "fie",
                 "<p1><pl>": "fim",  "<p2><pl>": "fiți",   "<p3><pl>": "fie"}
    },
    "vedea": {
        "ind":  {"<p1><sg>": "văd",  "<p2><sg>": "vezi",   "<p3><sg>": "vede",
                 "<p1><pl>": "vedem","<p2><pl>": "vedeți", "<p3><pl>": "văd"},
        "conj": {"<p1><sg>": "văd",  "<p2><sg>": "vezi",   "<p3><sg>": "vadă",
                 "<p1><pl>": "vedem","<p2><pl>": "vedeți", "<p3><pl>": "vadă"}
    },
    "mânca": {
        "ind":  {"<p1><sg>": "mănânc", "<p2><sg>": "mănânci", "<p3><sg>": "mănâncă",
                 "<p1><pl>": "mâncăm", "<p2><pl>": "mâncați", "<p3><pl>": "mănâncă"},
        "conj": {"<p1><sg>": "mănânc", "<p2><sg>": "mănânci", "<p3><sg>": "mănânce",
                 "<p1><pl>": "mâncăm", "<p2><pl>": "mâncați", "<p3><pl>": "mănânce"}
    },
    "plăcea": {
        "ind":  {"<p3><sg>": "place", "<p3><pl>": "plac"},
        "conj": {"<p3><sg>": "placă", "<p3><pl>": "placă"}
    }
}

#rules:

#prepositions, conjunctions,  remain the same

#handling <def> (definite) article by adding desired suffixes

#verbs in the conjunctive case rules

#different rules for time of verbs, based on mood

#adjectives must match corresponding noun


def generate_adjective(wf: WordFormat) -> str:
    lemma = wf.lemma
    tags = set(wf.tags)

    if "<f>" in tags and "<sg>" in tags:
        if lemma.endswith("ic") or not lemma.endswith(("ă", "e")):
            return lemma + "ă"      
        if lemma.endswith("u"): 
            return lemma[:-1] + "ă" 

    if "<f>" in tags and "<pl>" in tags:
        if lemma.endswith("ic"):
            return lemma + "i" 
        return lemma + "e"                                

    if "<m>" in tags and "<pl>" in tags:
        if lemma.endswith("c"): 
            return lemma + "i" 
        return lemma + "i"                               

    return lemma

def generate_noun(wf: WordFormat) -> str:
    lemma = wf.lemma
    tags = set(wf.tags)

    base_form = lemma
    if "<pl>" in tags and not lemma.endswith(("i", "e", "uri")):
        if "<m>" in tags:
            base_form = lemma + "i"
        elif "<f>" in tags:
            base_form = lemma[:-1] + "e" if lemma.endswith("ă") else lemma + "i"
        elif "<nt>" in tags:
            base_form = lemma + "uri"

    if "<def>" in tags:
        if "<f>" in tags and "<sg>" in tags:
            if base_form.endswith("ă"):
                return base_form[:-1] + "a"  
            if base_form.endswith("e"):
                return base_form + "a"       
            if base_form.endswith("ie"):
                return base_form[:-1] + "a" 

        if "<m>" in tags or "<nt>" in tags:
            if base_form.endswith("e"):
                return base_form + "le"      
            if base_form.endswith("i"):
                return base_form + "ul"      
            return base_form + "ul"                                  

        if "<pl>" in tags:
            if base_form.endswith("i"): 
                return base_form + "lor"
            if "<gen>" in tags or "<dat>" in tags:
                return   base_form + "le" 
            if base_form.endswith("e") or base_form.endswith("le"):
                return base_form + "le"      

    return base_form

def generate_verb(wf: WordFormat) -> str:
    lemma = wf.lemma
    tags = wf.tags

    mood = "ind"

    if "<conj>" in tags:
        mood = "conj"

    person = None
    if "<p1>" in tags:
        person = "<p1>"
    elif "<p2>" in tags:
        person = "<p2>"
    elif "<p3>" in tags:
        person = "<p3>"


    number = None
    if "<sg>" in tags:
        number = "<sg>"
    elif "<pl>" in tags:
        number = "<pl>"

    if person is None or number is None:
        return lemma

    if lemma in IRREGULAR_VERBS:
        forms = IRREGULAR_VERBS[lemma][mood]
        key = person + number
        if key in forms:
            return forms[key]

    #conj
    if "<conj>" in tags:
        if lemma.endswith("a"):
            if person == "<p3>":
                ending = "e"
            elif person == "<p2>":
                ending = "i"
            elif number == "<pl>" and person == "<p1>":
                ending = "ăm"
            elif number == "<pl>":
                ending = "ați"
            else:
                ending = ""
            return lemma[:-1] + ending
        elif lemma.endswith("e"):
            if person == "<p3>":
                ending = "ă"
            elif person == "<p2>":
                ending = "i"
            elif person == "<p1>" and number == "<pl>":
                ending = "em"
            elif number == "<pl>":
                ending = "eți"
            else:
                ending = ""
            return lemma[:-1] + ending
        elif lemma.endswith("i") or lemma.endswith("î"):
            if person == "<p3>":
                ending = "ească"
            elif person == "<p2>":
                ending = "i"
            elif person == "<p1>" and number == "<pl>":
                ending = "im"
            elif number == "<pl>":
                ending = "iți"
            else:
                ending = ""
            return lemma[:-1] + ending

    #present
    if "<past>" not in tags:
        if lemma.endswith("a"):
            endings = ["", "i", "ă", "ăm", "ați", "ă"]
        elif lemma.endswith("e"):
            endings = ["", "i", "e", "em", "eți", ""]
        elif lemma.endswith("i"):
            endings = ["", "i", "e", "im", "iți", ""]
        else:
            return lemma

        if person == "<p1>" and number == "<sg>":
            index = 0
        elif person == "<p2>" and number == "<sg>":
            index = 1
        elif person == "<p3>" and number == "<sg>":
            index = 2
        elif person == "<p1>" and number == "<pl>":
            index = 3
        elif person == "<p2>" and number == "<pl>":
            index = 4
        else:
            index = 5

        return lemma[:-1] + endings[index]

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
            if "<3SG>" in wordTags:
                wordTags.extend(["<p3>", "<sg>"])
            finalSentence.append(generate_verb(word))
        elif "<adj>" in wordTags:
            finalSentence.append(generate_adjective(word))
        else: #pronouns, conj, others have their own
            finalSentence.append(word.lemma)

    return " ".join(finalSentence)