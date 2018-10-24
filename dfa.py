#!/usr/bin/python
# -*- coding: latin-1 -*-

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
from PIL import Image


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

# class for processing file data
class process_file_data:
    # preprocess data: removal of new line, spaces, tabs and comments from data file
    def preprocess_data(self,data):
        data = data.split(';')
        data_arr = list()
        for word in data:
            word_to = ""
            i=0
            while i < len(word):
                if word[i] == '\n' or word[i] == '\t' or word[i] == ' ':
                    i = i + 1
                elif word[i] == '#':
                    i = i + 1
                    while word[i] != '\n':
                        i = i + 1
                else:
                    word_to = word_to + word[i]
                    i = i + 1
            data_arr.append(word_to)
        return self.process_data(data_arr)
    #process input to get data and check if valid
    def process_data(self,data_arr):
        operation = operations()
        for word in data_arr:
            if '->' in word:
                process = word.split('->')
                if(process[0] == 'states'):
                    states = self.check_data(process[1],process[0])
                elif(process[0] == 'alphabet'):
                    alphabet = self.check_data(process[1],process[0])
                elif(process[0] == 'accept_states'):
                    accept_states = self.check_data(process[1],process[0])
                elif(process[0] == 'start_state'):
                    start_state = self.check_data(process[1],process[0])
                elif(process[0] == 'transition'):
                    transition = self.check_data(process[1],process[0])
                else:
                    operation.error_msg("illegal DFA tuple declaration: %s"%process[0])
            else:
                pass
        return states,alphabet,accept_states,start_state,transition
    # check data from file if valid. includes: tokenize,lexical analysis and type checking
    def check_data(self,data,type):
        data_arr = list()
        operation = operations()
        if(type == "states" or type == "accept_states"):
            data = data.split(',')
            # limit states to 3
            if len(data) > 4:
                operation.error_msg("number of states must be less than 5 ")
            for token in data:
                if re.match('^[0-9]',token):
                    data_arr.append(int(token))
                else:
                    operation.error_msg("%s must be an integer"%type)
        elif(type == "start_state"):
            data_arr = int(data)
        elif(type == "alphabet"):
            data = data.split(',')
            for token in data:
                if re.match('^[A-Z,a-z]',token):
                    data_arr.append(str(token))
                else:
                    operation.error_msg("%s must be an alphabet"%type)
        elif(type == "transition"):
            data_arr = dict()
            #split transition data
            data = data.split(':')
            data_list = list()
            for transition in data:
                #split transition data using ',' to get initialize data
                transition_list = list()
                transition = transition.split(',')
                for transition_data in transition:
                    #split again to seperate name and value
                    transition_data = transition_data.split('=')
                    transition_data_list= list()
                    for transition_data_value_name in transition_data:
                        #turn name and value into array to check for errors and eliminate some characters
                        transition_data_value_name_map = map(str,transition_data_value_name)
                        array_token_list = ""
                        if '{' in transition_data_value_name_map or '}' in transition_data_value_name_map:
                            array_token = ""
                            for transition_data_value_name_array in transition_data_value_name_map:
                                if(transition_data_value_name_array == '{' or transition_data_value_name_array == '}'):
                                    pass
                                else:
                                    array_token = array_token + transition_data_value_name_array
                            array_token_list = array_token_list + array_token
                        else:
                            array_token_list =array_token_list + transition_data_value_name
                        transition_data_list.append(array_token_list)
                    transition_list.append(transition_data_list)
                data_list.append(transition_list)
            #build dict to create transition function
            for word in data_list:
                initial = word[0][1]
                value = word[1][1]
                target = word[2][1]
                data_arr[(int(initial),value)] = int(target);

        return data_arr

# class for operations needed
class operations:
    # function to generate languages based on size and input word
    def generate_language(self,size,input_word):
        array_of_language = list()
        for word in itertools.product(input_word,repeat = size):
            generated = ''.join(word)
            array_of_language.append(generated)
        return array_of_language
    #turn list values into a string
    def concatenate_list_data(self,list):
        result= ''
        for element in list:
            result += str(element)
        return result
    # scan list return true if var has *
    def greedy_scanner(self,arr,pos):
        for i in range(pos,len(arr)):
            if(i+1 != len(arr)):
                if(arr[i+1] == '*'):
                    return 1
                else:
                    return 0
            else:
                break
    #todo: convert DFA to regular expression
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
    def error_msg(self,msg):
        print "\n\n%s"%msg
        sys.exit()
    #print truth table
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
        print('|       (generator, checker, converter)        |')
        print('|                                              |')
        print('| DFA DATA: data.txt                           |')
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
        to_append = to_append + 'rankdir=LR'
        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa.png')
        a = Image.open('dfa.png')
        a.show()
    #----- regex to DFA functions -------
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
            elif word == '(' or word == ')':
                tokenize_all = tokenize_all + "(parenthesis,'%s') "%word
            else:
                self.error_msg("Error in parsing: illegal character: %s "%word)
        print(tokenize_all)
        stop = raw_input("Press any key to continue...(except poweroff!)")
    # print DFA diagram from language
    def print_DFA_diagram_language(self,prio,less_prio,title):
        G=pgv.AGraph()
        G=pgv.AGraph(strict=False,directed=True)
        initial = 0
        target = 1
        to_append = 'digraph G {size="4,4"; label="%s";'%title
        #print the dfa of priority expression
        prio = prio.split('(')
        for expression in prio:
            if expression == '':
                pass
            else:
                if '+' in expression:
                    arr = expression.split('+')
                    for i in range(0,len(arr)):
                        arr[i] = map(str,arr[i])
                    i = 0
                    indi = 0
                    start_f = list()
                    while i < len(arr):
                        j = 0
                        start = initial
                        while j < len(arr[i]):
                            if(self.greedy_scanner(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                                j+=2
                            elif(self.greedy_scanner(arr[i],j) == 1 and arr[i][j]== ')'):
                                to_append = to_append + '%s -> %s;'%(start,target)
                                k=0
                                while k < len(start_f):
                                    to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                    k+=1
                                to_append = to_append + '%s -> %s;'%(target,initial)
                                to_append = to_append + '%s -> %s;'%(initial,target)
                                j+=2
                            elif( arr[i][j] == ')'):
                                to_append = to_append + '%s -> %s;'%(start,target)
                                k=0
                                while k < len(start_f):
                                    to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                    k+=1
                                to_append = to_append + '%s -> %s;'%(target,initial)
                                j+=1

                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                                start = start + 1
                                target = target+1
                                j+=1
                            if(indi > 0):
                                start = target - 1

                        start_f.append(start)
                        start = initial
                        indi = 1
                        i+=1
                    initial = target
                    target = target + 1
                elif ')*' in expression:
                    arr = map(str,expression)
                    i = 0
                    start_in = initial
                    while i < len(arr):
                        if(self.greedy_scanner(arr,i) == 1 and re.match('^[a-z,A-Z]',arr[i])):
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                            i+=2
                        else:
                            if(arr[i] == ')' and arr[i+1] == '*'):
                                to_append = to_append + '%s -> %s;'%(initial,start_in)
                                to_append = to_append + '%s -> %s;'%(start_in,initial)
                                i+=2
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                                initial = initial + 1
                                target = target+1
                                i+=1

                else:
                    arr = map(str,expression)
                    i = 0
                    while i < len(arr):
                        if(self.greedy_scanner(arr,i) == 1):
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                            i+=2
                        else:
                            if(arr[i] == ')'):
                                i+=1
                                pass
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                                initial = initial + 1
                                target = target+1
                                i+=1

        less_prio = less_prio.split('(')
        for expression in less_prio:
            if expression == '':
                pass
            else:
                if '+' in expression:
                    arr = expression.split('+')
                    for i in range(0,len(arr)):
                        arr[i] = map(str,arr[i])
                    i = 0
                    indi = 0
                    start_f = list()
                    while i < len(arr):
                        j = 0
                        start = initial
                        while j < len(arr[i]):
                            if(self.greedy_scanner(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                                j+=2
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                                start = start + 1
                                target = target+1
                                j+=1
                            if(indi > 0):
                                start = target - 1
                        if (i+1 == len(arr) ):
                            to_append = to_append + '%s -> %s;'%(start,target)
                            k=0
                            while k < len(start_f):
                                to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                k+=1
                        start_f.append(start)
                        start = initial
                        indi = 1
                        i+=1
                    initial = target
                    target = target + 1
                else:
                    arr = map(str,expression)
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

        to_append = to_append + 'rankdir=LR{ %s [shape=doublecircle]'%initial
        to_append = to_append + '}'
        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa-language.png')
        a = Image.open('dfa-language.png')
        a.show()
    #process regular expression, determine priorities
    def process_regex(self,arr):
        self.tokenize(arr)
        arr_map = map(str,arr)
        i = 0
        priority = list()
        less_prio = list()
        paren = -1
        while i < len(arr_map):
            if arr_map[i] == '(':
                paren = 1
            elif arr_map[i] == ')':
                paren = 0
                priority.append(')')

            if paren == 1:
                priority.append(arr_map[i])
                i +=1
            elif re.match('^[a-z,A-Z,0-9]',arr_map[i]) or arr_map[i] == '+':
                if(self.greedy_scanner(arr_map,i) == 1):
                    less_prio.append(arr_map[i]+'*')
                    i+=2
                else:
                    less_prio.append(arr_map[i])
                    i+=1
            elif arr_map[i] == '*' and arr_map[i-1] == ')':
                priority.append(arr_map[i])
                i+=1
            else:
                i+=1
        priority = self.concatenate_list_data(priority)
        less_prio = self.concatenate_list_data(less_prio)
        self.print_DFA_diagram_language(priority,less_prio,arr)

    #the main
    def main(self):
        self.clear()
        choice = 0
        while choice != '3':
            self.clear()
            choice = raw_input("Select Option \n\n1: Inialize DFA and check accepted and denied Languages;\n2: Convert Regular Expression to DFA diagram\n3: exit program\n\n: ")
            if(choice == '2'):
                regex = raw_input("Enter Language: ")
                self.process_regex(regex)
            elif(choice == '1'):
                get_input_user_class = process_file_data();
                # get data from file
                data = open("data.txt", "r")
                data = data.read()
                # process data retrieved from file: data.txt
                data = get_input_user_class.preprocess_data(data)
                #inialize all variable
                states = data[0]
                alphabet = data[1]
                accept_states = data[2]
                start_state = data[3]
                transition = data[4]
                # create a DFA diagram based on transition function
                self.print_DFA_diagram(transition)
                # initialize all variable in class DFA
                dfa = DFA(states, alphabet, transition, start_state, accept_states);
                input_user_choice = '1'
                # loop for choosing
                while input_user_choice != '3':
                    self.clear()
                    #print all input from user
                    print('states: %s'%states)
                    print('alphabet: %s'%alphabet)
                    self.print_transition(states,alphabet,transition)
                    print('Start state: %s'%start_state)
                    print('Accept States: %s '%accept_states)
                    print("Converted DFA to Regular Expression: %s \n\n"%self.DFA_to_REGEX(transition))
                    input_user_choice = raw_input("1 to generate random language\n2 for manual input \n3 go back\n\n: ")
                    if(input_user_choice == '1'):
                        # get length of language to be generated from user
                        input_user = raw_input("Enter Lenght of language to be generated: ");
                        # initialize data for generating language
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
                        # print truth table
                        self.print_table(accepted,denied)
                        stop = raw_input("Press any key to continue...(except poweroff!)")
                    # for manual input of language
                    elif(input_user_choice == '2'):
                        input_user = raw_input("Enter language: ");
                        accepted = list()
                        denied = list()
                        #check if language is accepted by the DFA machine
                        if(dfa.check_if_dfa(input_user,accept_states)):
                            accepted.append(input_user)
                        else:
                            denied.append(input_user)
                        # print truth table
                        self.print_table(accepted,denied)
                        stop = raw_input("Press any key to continue...(except poweroff!)")

#main
#inialize class
operation = operations();
#call main function
try:
    operation.main()
except:
    # if error encountered display error message
    print("There was an error in running the program.\n")
