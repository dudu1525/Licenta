from data import WordFormat
import os
from typing import Callable
import json
from typing import List


Rule = tuple[list[set[str]], Callable[[list[WordFormat]], list[WordFormat]]] #map, kind of between a set of consecuvite must be tags and a associated function to it

#########################################RULE FUNCTIONS

#RULE 1
def rule_det_adj_noun(matched: list[WordFormat]) -> list[WordFormat]:
    det, adj, noun = matched[0], matched[1], matched[2]
    passedtags = [t for t in noun.tags if t in {"<m>", "<f>", "<nt>", "<sg>", "<pl>"}]
    adj.tags.extend(t for t in passedtags if t not in adj.tags)

    if det.lemma.lower() == "the":
        if "<def>" not in noun.tags:
            noun.tags.append("<def>")
        return [noun, adj] #GET RID OF THE
    
    det.tags.extend(t for t in passedtags if t not in det.tags)
    return [det, noun, adj]

#RULE 2
def rule_adj_noun(matched: list[WordFormat]) -> list[WordFormat]:
    adj, noun = matched[0], matched[1]
    passedtags = [t for t in noun.tags if t in {"<m>", "<f>", "<nt>", "<sg>", "<pl>"}]
    adj.tags.extend(t for t in passedtags if t not in adj.tags)
    return [noun, adj]

#RULE 3
def rule_det_noun(matched: list[WordFormat]) -> list[WordFormat]:
    det, noun = matched[0], matched[1]
    if det.lemma.lower() == "the":
        if "<def>" not in noun.tags:
            noun.tags.append("<def>")
        return [noun]
    passedtags = [t for t in noun.tags if t in {"<m>", "<f>", "<nt>", "<sg>", "<pl>"}]
    det.tags.extend(t for t in passedtags if t not in det.tags)
    return [det, noun]



#defined rules
RULES: list[Rule] = [
    (["<art>", "<adj>", "<n>"], rule_det_adj_noun), #the+adj+n
    (["<adj>", "<n>"],      rule_adj_noun), #adj + n
    (["<art>","<n>"],      rule_det_noun), #the+n

]

#open lexicons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
en_lex_path = os.path.join(BASE_DIR, "lexicons/en_lex.json")
with open(en_lex_path, "r", encoding="utf-8") as f:
    EN_LEX = json.load(f)
ro_lex_path = os.path.join(BASE_DIR, "lexicons/ro_lex.json")
with open(ro_lex_path, "r", encoding="utf-8") as f:
    RO_LEX = json.load(f)
bill_lex_path = os.path.join(BASE_DIR, "lexicons/bilingual_map.json")
with open(bill_lex_path, "r", encoding="utf-8") as f:
    BILINGUAL_MAP = json.load(f)

EN_LEMMA_TO_ID = {entry["lemma"].lower(): en_id for en_id, entry in EN_LEX.items()}

def translate_lex_entry(en_wf: WordFormat) -> WordFormat:
    if "<ro>" in en_wf.tags:
        return en_wf    
    lemma_clean = en_wf.lemma.lower().strip()
    
    en_id = EN_LEMMA_TO_ID.get(lemma_clean)
    if not en_id:
        return WordFormat(en_wf.lemma, list(en_wf.tags))

    ro_id = BILINGUAL_MAP.get(en_id)
    if not ro_id or ro_id not in RO_LEX:
        return WordFormat(en_wf.lemma, list(en_wf.tags))

    ro_entry = RO_LEX[ro_id]
    ro_lemma = ro_entry["lemma"]
    ro_tags = list(ro_entry["tags"])+ ["<ro>"]

    for tag in en_wf.tags:
        if tag not in ro_tags:
            ro_tags.append(tag)
    return WordFormat(ro_lemma, ro_tags)



#custom checker of a rule

def matches(words: list[WordFormat], i: int, pattern: list[str]) -> bool:
    if i + len(pattern) > len(words):
        return False

    for offset in range(len(pattern)):
        expected_tag = pattern[offset]
        current_word = words[i + offset]

        if expected_tag not in current_word.tags:
            return False

    return True


##########################################shallow transfer function, greedy approach
def shallow_transfer(en_words: list[WordFormat]) -> list[WordFormat]:

    words = [translate_lex_entry(w) for w in en_words]
    
    result: list[WordFormat] = []
    i = 0

    while i < len(words):

        matched_rule = False

        for pattern, action in RULES: #take each set of rules from all the rules
            if matches(words, i, pattern): #see if it matches for a set of words from the input
                setOfwords = words[i : i + len(pattern)]
                result.extend(action(setOfwords)) #apply the transformation function of the set of words
                i += len(pattern) #once matched, skip those words
                matched_rule = True
                break

        if not matched_rule:#fallback, just send as it is the word
            result.append(words[i]) 
            i += 1

    return result