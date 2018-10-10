#!/usr/bin/python

# Deterministic Finite Automata (DFA) implementation in python



import os,sys
import itertools
from itertools import product
from prettytable import PrettyTable
import pygraphviz as pgv
from IPython.display import Image, display


# DFA Function: check if language is in DFA machine
class DFA:
    current_state = None;
    #initialize all variable when calling the class DFA
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states;
        self.alphabet = alphabet;
        self.transition_function = transition_function;
        self.start_state = start_state;
        self.accept_states = accept_states;
        self.current_state = start_state;
        return;
    
    #check if input in transition function initialize
    def transition_to_state_with_input(self, input_value):
        if ((self.current_state, input_value) not in self.transition_function.keys()):
            self.current_state = None;
            return;
        self.current_state = self.transition_function[(self.current_state, input_value)];
        return;
    
    #return result
    def in_accept_state(self):
        return self.current_state in accept_states;
    
    #check each character if in transition
    def check_if_dfa(self, input_list):
        self.current_state = self.start_state;
        for inp in input_list:
            self.transition_to_state_with_input(inp);
            continue;
        return self.in_accept_state();
    pass;




# class fpr operations needed
class operations:
    # function to generate languages based on size and input word
    def generate_language(self,size,input_word):
        array_of_language = list()
        for word in itertools.product(input_word,repeat = size):   
            generated = ''.join(word)
            array_of_language.append(generated)
        return array_of_language    

    #turn list values into a single variable
    def concatenate_list_data(self,list):
        result= ''
        for element in list:
            result += str(element)
        return result

    #get states from user
    def get_states(self):
        input_user = ''
        states_arr = list()
        while input_user != 'END':
            states = raw_input("(enter end to exit) Enter states:")
            if(states == 'end'):
                input_user = 'END'
            else:
                states_arr.append(int(states))
            pass
        return states_arr
    
    #get alphabet from user
    def get_alphabet(self):
        input_user = ''
        alphabet_arr = list()
        while input_user != 'END':
            alphabet = raw_input("(enter end to exit) Enter alphabet:")
            if(alphabet == 'end'):
                input_user = 'END'
            else:
                alphabet_arr.append(str(alphabet))
            pass
        return alphabet_arr
    # get accept states from user
    def get_accept_states(self):
        input_user = ''
        states_arr = list()
        while input_user != 'END':
            states = raw_input("(enter end to exit) Enter accept states:")
            if(states == 'end'):
                input_user = 'END'
            else:
                states_arr.append(int(states))
            pass
        return states_arr
    
    #get transition function from user
    def get_transition_function(self):
        input_user = ''
        transition = dict();

        while input_user != 'end':
            input_user = raw_input("Enter 1 to initialize transition function. end to end: ")
            if(input_user == 'end'):
                input_user = 'end'
            else:
                initial = raw_input("Enter initial state value: ")
                value = raw_input("Enter value: ")
                target = raw_input("Enter target state: ")
                print(initial)
                print(value)
                print(target)
                transition[(int(initial),value)] = int(target);
                print(transition)
            pass
        return transition

    #print table
    def print_table(self,approved,denied):
        table = PrettyTable()
        table.field_names = ['accepted', 'rejected']
        for i in approved:
            table.add_row([i,' '])
        for i in denied:
            table.add_row([' ',i])
        print(table)
    def clear(self):
        os.system('cls||clear')
        print(' ----------------------------------------------')
        print('|     DETERMINISTIC FINITE AUTOMATA (DFA)      |')
        print(' ----------------------------------------------')

    def print_transition(self,states,alphabet,transition):
        table = PrettyTable()
        header = states
        header = ['Values']+header
        table.field_names = header

        print("Transition Table")
        for i in transition:
            for state in states:
                if(transition.get(i) == state):
                    num_of_index = len(states)
                    if(states.index(state) == 0):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, i[0],'',''])
                    elif(states.index(state) == 1):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '',i[0],''])
                    elif(states.index(state) == 2):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '','',i[0]])
        print(table)
    #printing DFA diagram
    def print_DFA_diagram(self,transition):
        G=pgv.AGraph()
        G=pgv.AGraph(strict=False,directed=True)

        to_append = 'digraph G {size="4,4"; ' 
        for i in transition:
            target = transition.get(i)
            initial = i[0]
            value = i[1]
            to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,value)
        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa.png')

    #the main
    def main(self):
        self.clear()

        #inialize all variable and get data from user
        
        #get states from user
        states = self.get_states()
        self.clear()
        
        #get alphabet from user
        print('states: %s\n\n'%states)
        alphabet = self.get_alphabet()
        self.clear()
        
        #get transition function from user
        print('states: %s'%states)
        print('alphabet: %s \n\n'%alphabet)
        transition = self.get_transition_function()
        self.clear()

        #get start state and accept state from user
        print('states: %s'%states)
        print('alphabet: %s'%alphabet)
        self.print_transition(states,alphabet,transition)
        start_state = raw_input("Enter start state: ");
        start_state = int(start_state)
        accept_states = self.get_accept_states();
        self.clear()

        #print all input from user
        print('states: %s'%states)
        print('alphabet: %s'%alphabet)
        self.print_transition(states,alphabet,transition)
        print('Start state: %s'%start_state)
        print('Accept States: %s \n\n'%accept_states)
        self.print_DFA_diagram(transition)

        # initialize all variable in class DFA
        dfa = DFA(states, alphabet, transition, start_state, accept_states);
        input_user_choice = '1'
        while input_user_choice != '0':
            self.clear()
            #print all input from user
            print('states: %s'%states)
            print('alphabet: %s'%alphabet)
            self.print_transition(states,alphabet,transition)
            print('Start state: %s'%start_state)
            print('Accept States: %s \n\n'%accept_states)
            input_user_choice = raw_input("Enter 1 to generate, 2 for manual input: ")
            if(input_user_choice == '1'):

                # get length of language to be generated from user
                input_user = raw_input("Enter Lenght of language to be generated: "); 

                string_alphabet = self.concatenate_list_data(alphabet)
                number_to_generate = int(input_user)

                #generate all posible combination of the string alphabet
                generated_value = self.generate_language(number_to_generate,string_alphabet)

                #initialize list for accepted and denied languages
                accepted = list()
                denied = list()

                #check if language is accepted by the DFA machine
                for i in generated_value:
                    if(dfa.check_if_dfa(i)):
                        accepted.append(i)
                    else:
                        denied.append(i)

                # print the result
                self.print_table(accepted,denied)
                stop = raw_input()
            elif(input_user_choice == '2'):
                input_user = raw_input("Enter language: ");
                accepted = list()
                denied = list()

                #check if language is accepted by the DFA machine

                if(dfa.check_if_dfa(input_user)):
                    accepted.append(input_user)
                else:
                    denied.append(input_user)
                self.print_table(accepted,denied)
                stop = raw_input()




#needed
accept_states = [0];
#inialize class
operation = operations();
#call main function
try:
    operation.main()    
except:
    print("There was an error in running the program")


