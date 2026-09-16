from dataclasses import dataclass
from collections import defaultdict
#class that contains everything related to a fst
EPSILON='' #nothing

#transition from a state to another state class
@dataclass
class Transition:
    start_state: int
    end_state: int
    input: str
    output: str

class FST:
    def __init__(self):
        self.transitions = defaultdict(list) #Transition type, each state has a list of transitions
        self.start_state_id = 0
        self.final_states = set() #multiple final states
        self.next_state_id = 1

    def add_transition(self, start_state, end_state, input_symbol, output_symbol):
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


def perform_fst_traversal(fst:FST, input_string:str) -> list[str]:
    outputs = []

    def traverse(current_state:int, string_position:int, output_so_far:str):

        if string_position == len(input_string) and current_state in fst.final_states:
            outputs.append(output_so_far)
            return
        
        for transition in fst.transitions[current_state]:
            if transition.input == EPSILON: #on epsilon transition on input, no character consumed from the input string
                traverse(transition.end_state, string_position, output_so_far + transition.output)
            elif(string_position < len(input_string) and input_string[string_position] == transition.input):
                traverse(transition.end_state, string_position + 1, output_so_far + transition.output)

    traverse(fst.start_state_id, 0, "")
    return outputs





