#!/usr/bin/python

# Deterministic Finite Automata (DFA) implementation in python

#Author: Earl Austin Zuniga
#Bicol University


import os,sys
import itertools
from itertools import product
from prettytable import PrettyTable
import pygraphviz as pgv
from IPython.display import Image, display
import re

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
    def in_accept_state(self,accept_states):
        return self.current_state in accept_states;

    #check each character if in transition
    def check_if_dfa(self, input_list,accept_states):
        self.current_state = self.start_state;
        for inp in input_list:
            self.transition_to_state_with_input(inp);
            continue;
        return self.in_accept_state(accept_states);
    pass;

# class for getting input from user
class get_input_user:
    #get states from user
    def get_states(self):
        operation = operations()
        states_arr = list()
        states = raw_input(" Enter states: ")
        states = states.split(',')

        # limit states to 3
        if len(states) > 4:
            operation.error_msg()

        for token in states:
            if re.match('^[0-9]',token):
                states_arr.append(int(token))
            else:
                operation.error_msg()
        return states_arr

    #get alphabet from user
    def get_alphabet(self):
        alphabet_arr = list()
        alphabet = raw_input(" Enter alphabet: ")
        alphabet = alphabet.split(',')
        for token in alphabet:
            if re.match('^[A-Z,a-z]',token):
                alphabet_arr.append(str(token))
            else:
                operation = operations()
                operation.error_msg()
        return alphabet_arr

    # get accept states from user
    def get_accept_states(self):
        states_arr = list()
        states = raw_input(" Enter Accept states: ")
        states = states.split(',')
        for token in states:
            if re.match('^[0-9]',token):
                states_arr.append(int(token))
            else:
                operation = operations()
                operation.error_msg()
        return states_arr

    #get transition function from user
    def get_transition_function(self):
        input_user = ''
        transition = dict();

        while input_user != 'end':
            input_user = raw_input("Enter 1 to initialize transition function. end to exit: ")
            if(input_user == 'end'):
                input_user = 'end'
            else:
                initial = raw_input("Enter initial state value: ")
                value = raw_input("Enter value: ")
                target = raw_input("Enter target state: ")
                if re.match('^[0-9]',initial) and re.match('^[0-9]',target) and re.match('^[a-z,A-Z]',value):
                    transition[(int(initial),value)] = int(target);
                    print(transition)
                else:
                    operation = operations()
                    operation.error_msg()
            pass
        return transition


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

    # scan list
    def greedy_scanner(self,arr,pos):
        for i in range(pos,len(arr)):
            if(i+1 != len(arr)):
                if(arr[i+1] == '*'):
                    return 1
                else:
                    return 0
            else:
                break

    #print table
    def print_table(self,approved,denied):
        table = PrettyTable()
        table.field_names = ['accepted', 'rejected']
        for i in approved:
            table.add_row([i,' '])
        for i in denied:
            table.add_row([' ',i])
        print(table)

    #clear screen for Linux
    def clear(self):
        os.system('cls||clear')
        print(' ----------------------------------------------')
        print('|     DETERMINISTIC FINITE AUTOMATA (DFA)      |')
        print(' ----------------------------------------------')

    #printing transition table
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
                                table.add_row([j, i[0],'','',''])
                    elif(states.index(state) == 1):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '',i[0],'',''])
                    elif(states.index(state) == 2):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '','',i[0],''])
                    elif(states.index(state) == 3):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '','','',i[0]])
        print(table)

    #printing DFA diagram: output image
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

    # to do
    def DFA_to_REGEX(self,transition):
        concat = ""
        for word in sorted(transition.iterkeys()):
            target = transition.get(word)
            initial = word[0]
            value = word[1]
            if(target == initial):
                concat = concat + value+"*"
            else:
                concat = concat + value
        return concat

    # error message
    def error_msg(self):
        print('\n\nError parsing input')
        exit()

    #tokenize input of user and check if correct
    def tokenize(self,arr):
        tokenize = map(str,arr)
        tokenize_all = ''
        for word in tokenize:
            if re.match('^[a-z,A-Z]',word):
                tokenize_all = tokenize_all + "(String,%s) "%word
            elif re.match('^[1-9]',word):
                tokenize_all = tokenize_all + "(Integer,%s) "%word
            elif word == '+':
                tokenize_all = tokenize_all + "(Plus,%s) "%word
            elif word == '*':
                tokenize_all = tokenize_all + "(Epsilon,%s) "%word
            else:
                self.error_msg()
        print(tokenize_all)
        stop = raw_input()

    # print DFA diagram from language
    def print_DFA_diagram_language(self,arr):
        self.tokenize(arr)
        G=pgv.AGraph()
        G=pgv.AGraph(strict=False,directed=True)
        initial = 0
        target = 1
        to_append = 'digraph G {size="4,4"; '

        if '+' in arr:
            #split
            arr = arr.split('+')
            #turn into list each
            for i in range(0,len(arr)):
                arr[i] = map(str,arr[i])
            i = 0
            indi = 0
            while i < len(arr):
                j = 0
                while j < len(arr[i]):
                    if(self.greedy_scanner(arr[i],j) == 1):
                        to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i][j])
                        j+=2
                    else:
                        to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i][j])
                        initial = initial + 1
                        target = target+1
                        j+=1
                    if(indi > 0):
                        initial = target - 1
                initial = 0
                indi = 1
                target = target
                i+=1
        else:
            arr = map(str,arr)
            i = 0
            while i < len(arr):
                if(self.greedy_scanner(arr,i) == 1):
                    to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                    i+=2
                else:
                    to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                    initial = initial + 1
                    target = target+1
                    i+=1

        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa-language.png')


    #the main
    def main(self):
        self.clear()
        choice = 0
        while choice != '3':
            self.clear()
            choice = raw_input("Select Option \n\n1: Inialize DFA and check accepted and denied Languages;\n2: Convert Regular Expression to DFA diagram\n\n: ")
            if(choice == '2'):
                a = raw_input("Enter Language: ")
                self.print_DFA_diagram_language(a)
            elif(choice == '1'):
                get_input_user_class = get_input_user();
                #inialize all variable and get data from user

                #get states from user
                states = get_input_user_class.get_states()
                self.clear()

                #get alphabet from user
                print('states: %s\n\n'%states)
                alphabet = get_input_user_class.get_alphabet()
                self.clear()

                #get transition function from user
                print('states: %s'%states)
                print('alphabet: %s \n\n'%alphabet)
                transition = get_input_user_class.get_transition_function()
                self.clear()

                #get start state and accept state from user
                print('states: %s'%states)
                print('alphabet: %s'%alphabet)
                self.print_transition(states,alphabet,transition)
                start_state = raw_input("Enter start state: ");
                start_state = int(start_state)
                accept_states = get_input_user_class.get_accept_states();
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
                while input_user_choice != '3':
                    self.clear()
                    #print all input from user
                    print('states: %s'%states)
                    print('alphabet: %s'%alphabet)
                    self.print_transition(states,alphabet,transition)
                    print('Start state: %s'%start_state)
                    print('Accept States: %s '%accept_states)
                    print("Converted DFA to Regular Expression: %s \n\n"%self.DFA_to_REGEX(transition))
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
                            if(dfa.check_if_dfa(i,accept_states)):
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

                        if(dfa.check_if_dfa(input_user,accept_states)):
                            accepted.append(input_user)
                        else:
                            denied.append(input_user)
                        self.print_table(accepted,denied)
                        stop = raw_input()




#inialize class
operation = operations();
#call main function
try:
    operation.main()
except:
    # if error encountered display error message
    print("\n\nThere was an error in running the program. Please enter correct Input")
