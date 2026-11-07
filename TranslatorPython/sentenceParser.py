
import json
from typing import List
from data import WordFormat

tree_transforms = {
    "S": [
        ("NP", "VP"),
        ("Aux", "NP", "VP"),
        ("VP",)
    ],
    "NP": [
        ("<art>", "NOM"), 
        ("NOM",),
        ("<prn>",),             
        ("<pn>",)
    ],
    "NOM": [
        ("<n>",),
        ("<adj>", "<n>"),
        ("<n>", "NOM"),
        ("NOM", "PP")
    ],
    "VP": [
        ("<vb>",),
        ("<vb>", "INF"),
        ("<vb>", "NP"),
        ("<vb>", "NP", "PP"),
        ("<vb>", "PP"),
        ("VP", "PP")
    ],
    "INF": [
        ("<pr>", "VP")   #infinitive of a verb (pr = to, preposition)
    ],
    "PP": [
        ("<pr>", "NP")
    ]
}
#ones with <> are terminals, other are non terminals, S is start

#Node in parse tree
class Node:
    def __init__(self, label, children=None):
        self.label = label        # word format type of terminal node, or a simple string thats non-terminal
        self.children = children or []

    def is_leaf(self):
        if isinstance(self.label, WordFormat):
            return True
        elif len(self.children) == 0:
            return True
        else:
            return False

#generated
def view_tree(node, indent="", is_last=True):
    if node is None:
        return

    marker = "└── " if is_last else "├── "

    if isinstance(node.label, WordFormat):
        wf = node.label
        tags_str = "".join(wf.tags)
        print(f'{indent}{marker}"{wf.lemma}" {tags_str}')
    elif node.is_leaf():
        print(f'{indent}{marker}"{node.label}"')
    else:
        print(f'{indent}{marker}[{node.label}]')
        new_indent = indent + ("    " if is_last else "│   ")
        count = len(node.children)
        for i, child in enumerate(node.children):
            view_tree(child, new_indent, i == count - 1)



class State:
    def __init__(self, lhs, rhs, dot=0, start=0, tree_children=None):
        self.lhs = lhs #left hand side of a rule
        self.rhs = tuple(rhs) #right hand side of a rule
        self.dot = dot #dot, as in the book, 0 before first word, 1 between first 2, and so on.
        self.start = start #holds the index (from the chart) when a rule started to analyze a word, used then for backtracking
        self.tree_children = tree_children or [] #holds children from a node in the parse tree

    def next_symbol(self): #returns the symbol (from the right hand side) right of the dot 'position'
        if self.dot < len(self.rhs):
            return self.rhs[self.dot]
        return None

    def is_complete(self): #when dot reaches the right side of the last right hand side symbol, finished
        return self.dot >= len(self.rhs)

    def __eq__(self, other):#equality between 2 states
        return (self.lhs == other.lhs and 
                self.rhs == other.rhs and 
                self.dot == other.dot and 
                self.start == other.start)

    def __hash__(self): #hash function for the set of states that will be storedd
        return hash((self.lhs, self.rhs, self.dot, self.start))


class EarleyParser: #grammar is the set of rules (up above)
    def __init__(self, grammar, start_symbol="S"):
        self.grammar = grammar
        self.start_symbol = start_symbol

    def parse(self, wordlist: list[WordFormat]):
        N = len(wordlist)
        chart = [] 
        chart_sets = []
        for i in range(N + 1):
            chart.append([])
            chart_sets.append(set())

        #adding a state to the current k iteration of the earley algorithm
        def add_state(state, k):
            if state not in chart_sets[k]:
                chart_sets[k].add(state)
                chart[k].append(state)
        # first state is the start rule
        add_state(State("S'", ["S"], dot=0, start=0), 0)



        for i in range(N + 1):
            j = 0
            while j < len(chart[i]):
                state = chart[i][j]

                if not state.is_complete():
                    next_sym = state.next_symbol()

                    #predict phase -> if next symbol is not terminal, add state to current iteration of the chart
                    if next_sym in self.grammar:
                        for rhs in self.grammar[next_sym]:
                            add_state(State(next_sym, rhs, dot=0, start=i), i)

                    #scanner phase -> try to match the part of speech tag
                    elif i < N:
                        word_obj = wordlist[i]
                        wordpos = word_obj.tags[0] #first part of the tags is the POS

                        if next_sym == wordpos:
                            leaf_val = Node(word_obj)#add as leaf the word format 
                            pos_node = Node(next_sym, [leaf_val]) #add as direct child to a node, that word format
                            new_children = state.tree_children + [pos_node]
                            add_state(State(state.lhs, state.rhs, dot=state.dot + 1, start=state.start, tree_children=new_children), i + 1)
                                #when adding this state, advance the dot, given it 'consumed' an input, other parts of state are inherited
                                #this is added to the next iteration, scanner always adds to the next iteration of the chart

                #completer part, 
                else:
                    completed_node = Node(state.lhs, state.tree_children)
                    for parent in chart[state.start]:#backtracking through the chart
                        if parent.next_symbol() == state.lhs:
                            new_children = parent.tree_children + [completed_node]
                            add_state(State(parent.lhs, parent.rhs, dot=parent.dot + 1, start=parent.start, tree_children=new_children), i)
                
                
                j += 1

        #returning the finally parsed tree from the final constructed chart
        for state in chart[N]:
            if state.lhs == "S'" and state.is_complete():
                return state.tree_children[0]

        return None  



# finallist = [
#     WordFormat(lemma="the", tags=["<art>"]),
#     WordFormat(lemma="cat", tags=["<n>", "<sg>"]),
#     WordFormat(lemma="walk", tags=["<vb>", "<3sg>"])
# ]

#parser = EarleyParser(grammar=tree_transforms, start_symbol="S")
#tree = parser.parse(finallist)

#view_tree(tree)


def parseSentenceFromWordFormat(inp):
    parser = EarleyParser(grammar=tree_transforms, start_symbol="S")
    tree = parser.parse(inp)
    return tree

############################################################################################ structural transfer with lexicons

with open("lexicons/en_lex.json", "r", encoding="utf-8") as f:
    EN_LEX = json.load(f) 

with open("lexicons/ro_lex.json", "r", encoding="utf-8") as f:
    RO_LEX = json.load(f)  

with open("lexicons/bilingual_map.json", "r", encoding="utf-8") as f:
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

def get_dative_clitic(pronoun_wf: WordFormat) -> WordFormat:

    person = next((t for t in pronoun_wf.tags
                   if t in ["<p1>", "<p2>", "<p3>"]), None)

    number = next((t for t in pronoun_wf.tags
                   if t in ["<sg>", "<pl>"]), None)

    clitics = {
        ("<p1>", "<sg>"): "îmi",
        ("<p2>", "<sg>"): "îți",
        ("<p3>", "<sg>"): "îi",
        ("<p1>", "<pl>"): "ne",
        ("<p2>", "<pl>"): "vă",
        ("<p3>", "<pl>"): "le"
    }

    lemma = clitics.get((person, number), "îmi")

    return WordFormat( lemma,["<prn>", person, number, "<dat>", "<cl>"])
def find_head_verb(vp):
#function to descend down a 'VP' path until a <vb> is found
    first = vp.children[0]
    if first.label == "<vb>":
        return first.children[0].label
    if first.label == "VP":
        return find_head_verb(first)
    return None

def propagate_person(node, person_tags):
    #this is needed to pass, from a subject
    if node.is_leaf():
        wf = node.label
        if isinstance(wf, WordFormat) and "<vb>" in wf.tags and "<conj>" in wf.tags:
            wf.tags.extend(t for t in person_tags if t not in wf.tags)
        return
    for child in node.children:
        propagate_person(child, person_tags)



def structuralTransfer(node:Node)->Node: #input tree, returns romanian tree,
    if node.is_leaf():
        if isinstance(node.label, WordFormat):
            return Node(translate_lex_entry(node.label))
        return node

    #the approach is relatively simple, searching for the patterns of the rules
    #idea is to start from the bottom up with the tree, and return the children recursively to the root
    transformedInputChildren = []
    for child in node.children:
        transformedInputChildren.append(structuralTransfer(child))

    node.children = transformedInputChildren#passing transformed children

    #applying the rules on the current node
    #rule 1 -> getting rid of 'the'
    if node.label == "NP" and len(node.children) == 2:
        if node.children[0].label == "<art>" and node.children[1].label == "NOM":
            nom_node = node.children[1]
            if len(nom_node.children) == 2 and nom_node.children[0].label == "<adj>":
                adj_node, noun_node = nom_node.children[0], nom_node.children[1]

                
                ro_noun_wf = translate_lex_entry(noun_node.children[0].label)
                ro_adj_wf = translate_lex_entry(adj_node.children[0].label)

                
                if "<def>" not in ro_noun_wf.tags: #devine articulat substantivul
                    ro_noun_wf.tags.append("<def>")

                # passing gender and counter to adj
                for tag in ro_noun_wf.tags:
                    if tag in ["<f>", "<m>", "<nt>", "<sg>", "<pl>"] and tag not in ro_adj_wf.tags:
                        ro_adj_wf.tags.append(tag)

                # swap adj and noun order
                return Node("NP", [Node("<n>", [Node(ro_noun_wf)]), Node("<adj>", [Node(ro_adj_wf)])])
            elif  len(nom_node.children) == 1 and nom_node.children[0].label == "<n>":
                noun_node = nom_node.children[0]
                ro_noun_wf = translate_lex_entry(noun_node.children[0].label)
                if "<def>" not in ro_noun_wf.tags: #devine articulat substantivul
                    ro_noun_wf.tags.append("<def>")
                return Node("NP", [Node("<n>", [Node(ro_noun_wf)])])


            
#rule 2, in a verb sentence, where there is for example she sees him -> ea IL vede (so clitic pronoun appears before the verb)
    if node.label == "VP" and len(node.children) == 2:
        if node.children[0].label == "<vb>" and node.children[1].label == "NP":
            np_child = node.children[1]
            if len(np_child.children) == 1 and np_child.children[0].label == "<prn>":
                verb_wf = node.children[0].children[0].label
                pron_wf = np_child.children[0].children[0].label
                ro_verb_wf = translate_lex_entry(verb_wf)
                ro_clitic_wf = translate_lex_entry(pron_wf)  
                ro_clitic_wf.tags.append("<cl>") #add clitic
                return Node("VP", [Node("<prn>", [Node(ro_clitic_wf)]), Node("<vb>", [Node(ro_verb_wf)])])


            
#rule 3 - for context: I want to eat -> sa appears and eat gets accorded with the subject
    if node.label == "VP" and len(node.children) == 2:
        if node.children[0].label == "<vb>" and node.children[1].label == "INF":
            main_v_node, inf_branch = node.children[0], node.children[1]
            ro_main_wf = translate_lex_entry(main_v_node.children[0].label)
           # print (inf_branch.children[0].label)
            if len(inf_branch.children) == 2 and inf_branch.children[0].label =="<pr>":
               # print("o intrat in al doilea")
                ro_second_verb_search = inf_branch.children[1].children[0].children[0] #inf->vp->vb->verb itself
                inner_vp = inf_branch.children[1]

                ro_translated_second_verb = translate_lex_entry(ro_second_verb_search.label)
            #give context to the secodn verb person/number tags
            #if verb contains 3sg -> third person = <p3>
                person_tags = [t for t in ro_main_wf.tags if t in ["<p1>", "<p2>", "<p3>", "<sg>", "<pl>"]]
                if "<3SG>" in ro_main_wf.tags:
                    person_tags.append("<p3>")
                    person_tags.append("<sg>")
                ro_translated_second_verb.tags.append("<conj>") #add conjunctive clause to the verb
                ro_translated_second_verb.tags.extend([t for t in person_tags if t not in ro_translated_second_verb.tags])

                sa_wf = WordFormat(lemma="să", tags=[ "<cnj>"])
                
                inf_branch.children[1].children[0].children[0].label = ro_translated_second_verb #attaching back the transalted verb from children
                return Node("VP", [
                    Node("<vb>", [Node(ro_main_wf)]),
                    Node("<cnj>", [Node(sa_wf)]),
                    inner_vp
                ])


    #rule 4 -> handle clitic verb that needs to go before the verb itself
    if node.label == "S" and len(node.children) == 2:

        subj_np, vp_node = node.children

        if (vp_node.label == "VP" and len(vp_node.children) >= 2 and vp_node.children[0].label == "<vb>"):
            verb_wf = vp_node.children[0].children[0].label
          
            if verb_wf.lemma.lower() in ["plăcea", "trebui"]:
           
                subj_wf = subj_np.children[0].children[0].label
                person_tags = [t for t in subj_wf.tags if t in ["<p1>", "<p2>", "<p3>", "<sg>", "<pl>"]]
                ro_verb_wf = translate_lex_entry(verb_wf)
                ro_verb_wf.tags.extend(t for t in person_tags if t not in ro_verb_wf.tags)

            
                dative_clitic_wf = get_dative_clitic(subj_wf)

                clitic_branch = Node("<prn>", [Node(dative_clitic_wf)])

                verb_branch = Node("<vb>", [Node(ro_verb_wf)])

                rest = vp_node.children[1:] #there can be more children, thus take all, 0 being the like or need word

                return Node("S", [Node("VP", [clitic_branch, verb_branch] + rest)])

#rule 5 drop the subject of the proposition (pronoun)

    if node.label == "S" and len(node.children) == 2:
        subj_np, vp_node = node.children[0], node.children[1]
        if subj_np.label == "NP" and len(subj_np.children) == 1 and subj_np.children[0].label == "<prn>":
            prn_wf = subj_np.children[0].children[0].label #get the pronoun itself
            person_tags = [t for t in prn_wf.tags if t in ["<p1>", "<p2>", "<p3>", "<sg>", "<pl>", "<3SG>"]]
            # give the person number to the verb following the pronoun
            verb_wf = find_head_verb(vp_node)
            if verb_wf is not None:
                verb_wf.tags.extend([t for t in person_tags if t not in verb_wf.tags])
                propagate_person(vp_node, person_tags)
                #translated_verb = translate_lex_entry(vp_node.children[0].children[0].label)
            #drop the np node
                return Node("S", [vp_node])



#also normal nodes need direct translate, no rules, if not of type NOM, VP, NP, ETC
    return node




def StructuralTransferAndFlatten(node:Node) ->List[WordFormat]:

    if len(node.children)==0: #child
        label = node.label
        if isinstance(label, WordFormat):
            wf = label
        translated_wf = translate_lex_entry(wf)
        return [translated_wf]
    
    finalList =  []#final list with all nodes, parent node
    for child in node.children:
        finalList.extend(StructuralTransferAndFlatten(child))
    return finalList


