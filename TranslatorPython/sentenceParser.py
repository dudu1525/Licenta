from dataclasses import dataclass

@dataclass
class WordFormat:
    lemma: str
    tags: list[str]
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
        ("<vb>", "NP"),
        ("<vb>", "NP", "PP"),
        ("<vb>", "PP"),
        ("VP", "PP")
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

#print("=== STRUCTURED PARSE TREE VIEW ===")
#view_tree(tree)


def parseSentenceFromWordFormat(inp):
    parser = EarleyParser(grammar=tree_transforms, start_symbol="S")
    tree = parser.parse(inp)
    return tree


def structuralTransfer(inp, rules): #input tree, romanian transfer rules!
    