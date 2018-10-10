# DFA-implemented-python
<br />
Deterministic Finite Automaton Implemented in Python Language<br />
-> a python program that creates a DFA machine (5-tuple),generates set of language and checks if the generated language is accepted by the created DFA machine. 

A deterministic finite automaton M is a 5-tuple, ( Q , Σ , δ , q0 , F ) consisting of<br />

    a finite set of states Q
    a finite set of input symbols called the alphabet Σ 
    a transition function δ : Q × Σ → Q 
    an initial or start state q 0 ∈ Q 
    a set of accept states F ⊆ Q 


Package used:<br />
->graphviz<br />
->PrettyTable<br />
<br />
Install required package to run the program<br />
|sudo apt-get install graphviz libgraphviz-dev graphviz-dev pkg-config<br />
|pip install pygraphviz<br />
|pip install PrettyTable<br />

run the program<br />
| chmod +x dfa.py<br />
| ./dfa.py<br />

<br />
<br />
Required Input:<br />
	set of states Q<br />
		{0,1,2,3}<br />
	set of alphabet Σ <br />
		{a,b,c}<br />

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

Sample run<br />
	![alt text](screenshot/display.png)

Sample result<br />
	![alt text](screenshot/result.png)

Sample DFA Diagram Generated:<br />
	![alt text](dfa.png)