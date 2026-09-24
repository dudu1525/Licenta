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
def createFSTNodes()->FST:
    fst =FST()

    states = {"start": fst.start_state_id} #dictionary of letter to number
    fst.add_final_state(fst.start_state_id)

    for s in ALPHABET:
        states[s] = fst.add_new_state()
        fst.add_final_state(states[s])
    for s in ALPHABET:
        fst.add_transition(fst.start_state_id, states[s], s, s)
    for s in SPECIAL_SYMBOLS:
        states[s] = fst.add_new_state()

    for firstChar in ALPHABET:
        for secondChar in ALPHABET:
            fst.add_transition(states[firstChar], states[secondChar],secondChar, secondChar )

    #for each letter, from A-B, add potential transitions to special characters
    potentialRulesPerChar =defaultdict( lambda:defaultdict(list)) #for each char, list of [set of rules[specific rules]]
    for secondChar in ALPHABET:
        for firstChar in ALPHABET:  
            for ruleset_index, setRules in enumerate(rules):
                for specificRule in setRules:
                    if specificRule.leftCharacters == [firstChar, secondChar]:
                        potentialRulesPerChar[secondChar][ruleset_index].append(specificRule)
    
    
        for ruleset_index, setRules in enumerate(rules):
            for specificRule in setRules:
                if specificRule.leftCharacters == [secondChar] or specificRule.leftCharacters == []:
                    potentialRulesPerChar[secondChar][ruleset_index].append(specificRule)


    for char in ALPHABET:
        for ruleset_index, possibleRules in potentialRulesPerChar[char].items():
            orderedRules = sorted(possibleRules, key=lambda r: len(r.leftCharacters), reverse=True)
            bestRule = orderedRules[0]
            outputs = bestRule.outputForTransition
            tag = bestRule.inputForTransition

            if len(outputs) == 1:
  
                fst.add_transition(states[char], states[tag], tag, outputs[0])
                fst.add_final_state(states[tag])
            else:

                mid = fst.add_new_state()
                fst.add_transition(states[char], mid, tag, outputs[0])
                current_state = mid
                for i in range(1, len(outputs)):
                    next_state = fst.add_new_state()
                    fst.add_transition(current_state, next_state, EPSILON, outputs[i])
                    current_state = next_state
                fst.add_final_state(current_state)\
                #TESTING
    print("States:", states)
    print("Transitions out of states['t']:")
    for t in fst.transitions[states["t"]]:
        print(f"  {t.input} -> {t.output} -> state {t.end_state}")
    print("Final states:", fst.final_states)
    return fst



#TESING
fst = createFSTNodes()
analyzer = invert(fst)
for state, transitions in fst.transitions.items():
    for t in transitions:
        print(
            f"{t.start_state} -- {t.input}/{t.output} --> {t.end_state}"
        )
def test(fst, input_tokens):
    results = perform_fst_traversal(fst, input_tokens)
    print(f"{''.join(input_tokens):15} -> ", end="")
    if not results:
        print("NO OUTPUT")
        return
    for result in results:
        print("".join(result))

test(fst, ["c", "a", "t", "<PL>"])
test(fst, ["b", "o", "x", "<PL>"])
print("INVERTED FST")

test(analyzer, ["c", "a", "t", "s"])
test(analyzer, ["b", "o", "x", "e", "s"])
test(analyzer, ["s", "c", "h", "o", "o", "l", "s"])
