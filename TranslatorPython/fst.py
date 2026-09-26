from dataclasses import dataclass
from collections import defaultdict
#class that contains everything related to a fst
EPSILON="<nothing>" #nothing

#transition from a state to another state class
@dataclass
class Transition:
    start_state: int
    end_state: int
    input: str
    output: str

@dataclass
class LeftContextRule:
    leftCharacters: list[str]
    inputForTransition: str
    outputForTransition: list[str]



class FST:
    def __init__(self):
        self.transitions = defaultdict(list) #Transition type, each state has a list of transitions
        self.start_state_id = 0
        self.final_states = set() #multiple final states
        self.next_state_id = 1

    def add_transition(self, start_state, end_state, input_symbol: str, output_symbol: str):
        transition = Transition(start_state, end_state, input_symbol, output_symbol)
        self.transitions[start_state].append(transition)

    def add_new_state(self):
        state_id = self.next_state_id
        self.next_state_id += 1
        return state_id

    def set_start_state(self, state_id):
        self.start_state_id = state_id

    def add_final_state(self, state_id):
        self.final_states.add(state_id)


def perform_fst_traversal(fst:FST, input_string:str) -> list[list[str]]:
    outputs = []

    def traverse(current_state:int, string_position:int, output_so_far:list[str]):

        if string_position == len(input_string) and current_state in fst.final_states:
            if output_so_far not in outputs:
                outputs.append(output_so_far)
            return
        
        for transition in fst.transitions[current_state]:
            if transition.input == EPSILON: #on epsilon transition on input, no character consumed from the input string
                new_output = output_so_far
                if transition.output != EPSILON:
                    new_output = output_so_far + [transition.output]
                traverse(transition.end_state, string_position, new_output)
            elif(string_position < len(input_string) and input_string[string_position] == transition.input):
                new_output = output_so_far
                if transition.output != EPSILON:
                    new_output = output_so_far + [transition.output]
                traverse(transition.end_state, string_position + 1, new_output)

    traverse(fst.start_state_id, 0, [])
    return outputs

def invert(fst):
    new_fst = FST()

    new_fst.next_state_id = fst.next_state_id
    new_fst.start_state_id = fst.start_state_id
    new_fst.final_states = set(fst.final_states)

    for source, transitions in fst.transitions.items():
        for t in transitions:
            new_fst.add_transition(
                source,
                t.end_state,
                t.output,
                t.input
            )

    return new_fst 

ALPHABET = [
    "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z"
]
SPECIAL_SYMBOLS =[    "<PL>",
    "<3SG>", #for verb, 3rd person, singular (es)
    "<PAST>"]

rules = [
    #plural
    [LeftContextRule([],       "<PL>",   ["s"]),
    LeftContextRule(["x"],    "<PL>",   ["e", "s"]),
    LeftContextRule(["s"],    "<PL>",   ["e", "s"]),
    LeftContextRule(["c","h"],"<PL>",   ["e", "s"]),
    LeftContextRule(["s","h"],"<PL>",   ["e", "s"])],
    #3rd person singular
    [LeftContextRule([],       "<3SG>",  ["s"]),
    LeftContextRule(["x"],    "<3SG>",  ["e", "s"]),
    LeftContextRule(["s"],    "<3SG>",  ["e", "s"]),
    LeftContextRule(["c","h"],"<3SG>",  ["e", "s"]),
    LeftContextRule(["s","h"],"<3SG>",  ["e", "s"])],
    # past tense
    [LeftContextRule([],       "<PAST>", ["e", "d"]),
    LeftContextRule(["e"],    "<PAST>", ["d"]),
    LeftContextRule(["y"],    "<PAST>", ["i", "e", "d"])],
]



def createFST  () -> FST:
    fst = FST()
    contextRules = set([""])#empty condition added to context rules
    #first part concentrates on creating the prefixes to each special rule
    for ruleset in rules: 
        for rule in ruleset:    
            ctx_str = ""
            for character in rule.leftCharacters: #create a normal string with its chars
                ctx_str += character
            for length in range(len(ctx_str) + 1):
                prefix = ctx_str[0:length]
                contextRules.add(prefix) #forming all prefixes of a context of a rule

    #create states for the rules
    states = {}
    for context in contextRules:
        states[context] = fst.add_new_state()
    fst.set_start_state(states[""])

    #contexts 
    for context in contextRules:
        fst.add_final_state(states[context])
#aho corasick algorithm >map normal characters
    for context in contextRules:
        for letter in ALPHABET:
            supposedContext = context+letter#supposed next 'context' with a added letter
            targetContext=""
            #try to construct the best suffix (longest) from a supposed context formed with the current letter
            #if no context found ,it basically goes back and considers a normal letter
            for i in range(len(supposedContext)):
                suffix = ""
                for j in range(i, len(supposedContext)):
                    suffix+=supposedContext[j]
                if suffix in contextRules:
                    targetContext = suffix
                    break
            fst.add_transition(states[context], states[targetContext], letter, letter)
    #map special characters
    rulesByTag = defaultdict(list)
    #create a dictionary with list for each special tag
    for ruleset in rules:
        for rule in ruleset:
            rulesByTag[rule.inputForTransition].append(rule)

    for context in contextRules: #based on each context and each tag (<pl>, <3sg>,etc) choose the longest left constraint and add it as final state
        for tag, tagrules in rulesByTag.items():
            validRules = [] #list that finally will contain rules matching the current context
            for rule in tagrules:
                leftContextString = "".join(rule.leftCharacters)
                if context.endswith(leftContextString):
                    validRules.append(rule)

            if validRules: #get the rule with the most restrictions for each context
                bestRule = max(validRules, key = lambda rule: len(rule.leftCharacters))
                bestOut = bestRule.outputForTransition

                if len(bestOut)==1:# if 1, just add the transition to a final state, via the simple tag,
                    final_state = fst.add_new_state()
                    fst.add_transition(states[context], final_state, tag, bestOut[0])
                    fst.add_final_state(final_state)
                else:#else construct intermediary nodes, starting with the tag, until a final one
                    current_state = states[context]
                    intermediary = fst.add_new_state()
                    fst.add_transition(current_state, intermediary, tag, bestOut[0])
                    current_state = intermediary
                    for i in range(1, len(bestOut)):
                        next_State = fst.add_new_state()
                        fst.add_transition(current_state, next_State, EPSILON, bestOut[i])
                        current_state=next_State
                    fst.add_final_state(current_state);

    return fst

#TESING
fst = createFST()
analyzer = invert(fst)
#for state, transitions in fst.transitions.items():
 #   for t in transitions:
  #      print(
   #         f"{t.start_state} -- {t.input}/{t.output} --> {t.end_state}"
    #    )
def test(fst, input_tokens):
    results = perform_fst_traversal(fst, input_tokens)
    print(f"{''.join(input_tokens):15} -> ", end="")
    if not results:
        print("NO OUTPUT")
        return
    for result in results:
        print("".join(result))


test(analyzer, ["c", "a", "t", "s"])
test(analyzer, ["b", "o", "x", "e", "s"])
test(analyzer, ["s", "c", "h", "o", "o", "l", "s"])
test(analyzer, ["g", "r", "a", "p", "h", "s"]) 
test(analyzer, ['b', 'o', 'x'])
test(analyzer, ['c', 'h', 'u', 'r', 'c', 'h'])