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


def greedy_scanner(arr,pos):
    for i in range(pos,len(arr)):
        if(i+1 != len(arr)):
            if(arr[i+1] == '*'):
                return 1
            else:
                return 0
        else:
            break

def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def print_DFA_diagram_language(prio,less_prio):
    G=pgv.AGraph()
    G=pgv.AGraph(strict=False,directed=True)
    initial = 0
    target = 1
    to_append = 'digraph G {size="4,4"; '

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
                while i < len(arr):
                    j = 0
                    start = initial
                    while j < len(arr[i]):
                        if(greedy_scanner(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                            to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                            j+=2
                        elif(greedy_scanner(arr[i],j) == 1 and arr[i][j]== ')'):
                            print "a"
                            to_append = to_append + '%s -> %s;'%(start,target)
                            to_append = to_append + '%s -> %s;'%(start-1,target)
                            to_append = to_append + '%s -> %s;'%(target,initial)

                            j+=2
                        else:
                            to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                            start = start + 1
                            target = target+1
                            j+=1
                        if(indi > 0):
                            start = target - 1
                    start = initial
                    indi = 1
                    i+=1
                initial = target
                target = target + 1
            elif ')*' in expression:
                arr = map(str,expression)
                i = 0
                while i < len(arr):
                    if(greedy_scanner(arr,i) == 1):
                        to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                        i+=2
                    else:
                        if(arr[i] == ')' and arr[i+1] == '*'):
                            i+=2
                            print "au"
                        else:
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                            initial = initial + 1
                            target = target+1
                            i+=1

            else:
                arr = map(str,expression)
                i = 0
                while i < len(arr):
                    if(greedy_scanner(arr,i) == 1):
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
                while i < len(arr):
                    j = 0
                    start = initial
                    while j < len(arr[i]):
                        if(greedy_scanner(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                            to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                            j+=2
                        else:
                            to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                            start = start + 1
                            target = target+1
                            j+=1
                        if(indi > 0):
                            start = target - 1
                    start = initial
                    indi = 1
                    i+=1
            else:
                arr = map(str,expression)
                i = 0
                while i < len(arr):
                    if(greedy_scanner(arr,i) == 1):
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

def process_regex(arr):
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
            if(greedy_scanner(arr_map,i) == 1):
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
    priority = concatenate_list_data(priority)
    less_prio = concatenate_list_data(less_prio)
    print_DFA_diagram_language(priority,less_prio)







regex = "(a+b)* (abcd*) (a+b)* ab"
process_regex(regex)
