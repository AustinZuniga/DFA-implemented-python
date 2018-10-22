# DFA: generator,converter,checker python

## Deterministic Finite Automaton Generator and converter Python
>  a python program that reads data from a file and creates a DFA machine (5-tuple),generates set of language and checks if the generated language is accepted by the created DFA machine and converts Regular Expression to DFA. <br /><br />

A deterministic finite automaton M is a 5-tuple, ( Q , Σ , δ , q0 , F ) consisting of<br />

    a finite set of states Q
    a finite set of input symbols called the alphabet Σ
    a transition function δ : Q × Σ → Q
    an initial or start state q 0 ∈ Q
    a set of accept states F ⊆ Q


##### Package used:
> graphviz<br />
> PrettyTable<br />
<br />

##### Install required package to run the program
> sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config<br />
> pip install pygraphviz<br />
> pip install PrettyTable<br />

##### run the program
> chmod +x dfa.py<br />
> ./dfa.py<br />

<br />

##### Required Input(Initialize DFA):
	set of states Q
		{0,1,2,3}

<br/>

	set of alphabet Σ
		{a,b,c}


<br/>

	transition function δ : Q × Σ → Q
		current state: {0}
		value: {a}
		Target state: {1}

<br />

	initial or start state q 0 ∈ Q
		{0}

<br />

	a set of accept states F ⊆ Q
		{1,0}

##### Sample Input from file "data.txt":
![alt text](screenshot/file.png)

##### required Input(Regular Expression to DFA)

	Regular Expression
		ab*+cd

##### Sample run
![alt text](screenshot/display.png)

##### Sample result
![alt text](screenshot/result.png)

##### Sample DFA Diagram Generated:
![alt text](dfa.png)
