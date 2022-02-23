# Toader George-Catalin 331CB

EPS = "EPSILON"

# clasa pentru starile automatelor, contine numele, configuratiile starilor pentru DFA,
# si lista tranzitiilor
class State:
	def __init__(self):
		self.name = ""
		self.NFA_states = []
		self.transitions = []

	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def set_NFA_states(self, NFA_states):
		self.NFA_states = NFA_states

	def get_NFA_states(self):
		return self.NFA_states

	def add_trans(self, char, next_state):
		self.transitions.append((char, next_state))

	def get_transitions(self):
		return self.transitions

	def __str__(self):
		return str(self.name)

# clasa folosita la parsarea prenex-ului, clasa parinte
class Expression:
	def __init__(self, par_num):
		self.par1 = None
		self.par2 = None
		self.par_num = par_num

	def set_par1(self, par1):
		self.par1 = par1

	def get_par1(self):
		return self.par1

	def decrease_par_num(self):
		self.par_num -= 1

	def get_par_num(self):
		return self.par_num

	def set_par2(self, par2):
		self.par2 = par2

	def get_par2(self):
		return self.par2

# cele 4 clase ce mostenesc Expression, corespunzatoare celor 4 expresii folosite
class Union(Expression):
	def __str__(self):
		return "UNION(" + str(self.par1) + "," + str(self.par2) + ")"

class Concat(Expression):
	def __str__(self):
		return "CONCAT(" + str(self.par1) + "," + str(self.par2) + ")"

class Star(Expression):
	def __str__(self):
		return "STAR(" + str(self.par2) + ")"

class Plus(Expression):
	def __str__(self):
		return "PLUS(" + str(self.par2) + ")"

# clasa NFA-ului construit folosind algoritmul lui Thompson
class NFA:
	def __init__(self, regex):
		self.alphabet = set()
		self.initial_state = None
		self.final_state = None
		self.states = []
		# verific daca este expresie sau caracter, iar in primul caz si tipul ei
		if isinstance(regex, Union):
			# am UNION deci creez cele 2 NFA-uri si cele 2 noi stari, initiala si finala
			nfa1 = NFA(regex.get_par1())
			nfa2 = NFA(regex.get_par2())
			self.alphabet = set.union(nfa1.get_alphabet(), nfa2.get_alphabet())
			self.initial_state = State()
			self.final_state = State()
			self.states.append(self.initial_state)
			self.states.append(self.final_state)
			self.states.extend(nfa1.get_states())
			self.states.extend(nfa2.get_states())
			# cele 2 tranzitii de la noua stare initiala la cele 2 NFA-uri
			self.initial_state.add_trans(EPS, nfa1.get_initial_state())
			self.initial_state.add_trans(EPS, nfa2.get_initial_state())
			# cele 2 tranzitii de la starile finale ale NFA-urilor la noua stare finala
			nfa1.get_final_state().add_trans(EPS, self.final_state)
			nfa2.get_final_state().add_trans(EPS, self.final_state)

		elif isinstance(regex, Concat):
			# am CONCAT deci creez cele 2 NFA-uri si le leg printr-o tranzitie EPS
			nfa1 = NFA(regex.get_par1())
			nfa2 = NFA(regex.get_par2())
			self.alphabet = set.union(nfa1.get_alphabet(), nfa2.get_alphabet())
			self.initial_state = nfa1.get_initial_state()
			self.final_state = nfa2.get_final_state()
			self.states.extend(nfa1.get_states())
			self.states.extend(nfa2.get_states())
			# adaug tranzitia de EPS dintre cele 2 NFA-uri
			nfa1.get_final_state().add_trans(EPS, nfa2.get_initial_state())

		elif isinstance(regex, Star):
			# am STAR deci creez 2 noi stari
			nfa = NFA(regex.get_par2())
			self.alphabet = nfa.get_alphabet()
			self.initial_state = State()
			self.final_state = State()
			self.states.append(self.initial_state)
			self.states.append(self.final_state)
			self.states.extend(nfa.get_states())
			# adaug noile tranzitii de EPS pentru STAR
			self.initial_state.add_trans(EPS, nfa.get_initial_state())
			self.initial_state.add_trans(EPS, self.final_state)
			nfa.get_final_state().add_trans(EPS, nfa.get_initial_state())
			nfa.get_final_state().add_trans(EPS, self.final_state)

		elif isinstance(regex, Plus):
			# am PLUS deci creez 2 noi stari
			nfa = NFA(regex.get_par2())
			self.alphabet = nfa.get_alphabet()
			self.initial_state = State()
			self.final_state = State()
			self.states.append(self.initial_state)
			self.states.append(self.final_state)
			self.states.extend(nfa.get_states())
			# ca la STAR dar fara tranzitia EPS dintre initial-final ca ne trebuie 1+
			self.initial_state.add_trans(EPS, nfa.get_initial_state())
			nfa.get_final_state().add_trans(EPS, nfa.get_initial_state())
			nfa.get_final_state().add_trans(EPS, self.final_state)

		else:
			# este caracter deci creez 2 stari cu 1 tranzitie pe caracterul dat
			self.alphabet.add(regex)
			self.initial_state = State()
			self.final_state = State()
			self.states.append(self.initial_state)
			self.states.append(self.final_state)
			# adaug tranzitia dintre cele 2 stari
			self.initial_state.add_trans(regex, self.final_state)

		# numerotez starile de la 0 la (len - 1)
		for i in range(len(self.states)):
			self.states[i].set_name(i)

	def get_alphabet(self):
		return self.alphabet

	def get_initial_state(self):
		return self.initial_state

	def get_final_state(self):
		return self.final_state

	def get_states(self):
		return self.states

	# afisare NFA
	def print_nfa(self):
		print("Initial state: " + str(self.initial_state.get_name()))
		print("Final state: " + str(self.final_state.get_name()))
		print("Transitions:")
		for state in self.states:
			for trans in state.get_transitions():
				print("State " + str(state.get_name()) + "->" + str(trans[0]) +
				 "->" + str(trans[1].get_name()))

# clasa DFA-ului construit conform algoritmului prezentat la curs
class DFA:
	def __init__(self, nfa):
		self.alphabet = nfa.get_alphabet()
		self.initial_state = State()
		self.initial_state.set_name(0)
		# updatez lista starilor accesibile din starea intiala prin EPS (adica E(0))
		self.initial_state.set_NFA_states(states_access([nfa.get_initial_state()], EPS))
		self.final_states = []
		self.update_final_state(nfa, self.initial_state)
		self.states = []
		self.states.append(self.initial_state)

		i = 0
		# parcurg starile noului DFA, la inceput am doar initial_state
		while i < len(self.states):
			# trebuie sa am tranzitie pe fiecare litera din alfabet
			for char in nfa.get_alphabet():
				# aplic logica algoritmului, verific in ce stari se poate ajunge,
				# iar apoi construiesc lista E(?) corespunzatoare acelor stari
				state_list = states_access(self.states[i].get_NFA_states(), char)
				state_list = states_access(state_list, EPS)

				new_state = None
				# verific daca avem deja starea construita
				for state in self.states:
					if state.get_NFA_states() == state_list:
						new_state = state
						break
				# daca nu avem starea atunci creez una noua (aici se creeaza si sinkstate-ul)
				if new_state == None:
					new_state = State()
					# numerotez starile in ordinea in care au intrat in lista
					new_state.set_name(len(self.states))
					new_state.set_NFA_states(state_list)
					self.states.append(new_state)
					self.update_final_state(nfa, new_state)

				# adaug tranzitia din starea curenta catre starea gasita/construita anterior
				self.states[i].add_trans(char, new_state)
			i += 1

	def get_alphabet(self):
		return self.alphabet

	def get_initial_state(self):
		return self.initial_state

	def get_final_states(self):
		return self.final_states

	def get_states(self):
		return self.states

	# daca contine starea finala a NFA-ului atunci este si stare finala a DFA-ului
	def update_final_state(self, nfa, state):
		if nfa.get_final_state() in state.get_NFA_states():
			self.final_states.append(state)

	# scrie DFA-ul conform formatului din fisierele de test
	def write_dfa(self, f_out):
		f_out.write("".join(str(x) for x in self.alphabet) + "\n")
		f_out.write(str(len(self.states)) + "\n")
		f_out.write(str(self.initial_state.get_name()) + "\n")
		my_list = map(lambda state: state.get_name(), self.final_states)
		f_out.write(" ".join(str(x) for x in my_list) + "\n")
		for state in self.states:
			for tran in state.get_transitions():
				f_out.write(str(state.get_name()) + ",'" + str(tran[0]) + 
					"'," + str(tran[1].get_name()) + "\n")

# returneaza starile accesibile din lista starilor data ca parametru, folosind caracterul 'char'
def states_access(initial_list, char):
	# creez copie a lui initial_list si o noua lista a rezultatelor
	stack = []
	result = []
	for state in initial_list:
		stack.append(state)
		# adaug starea curenta daca am EPS ca si 'char'
		if char == EPS:
			result.append(state)
	# parcurg cat timp mai am stari pe stiva      
	while len(stack) > 0:
		state = stack.pop()
		for trans in state.get_transitions():
			# verific tranzitiile daca au caracterul cautat si nu am vizitat deja destinatia
			if trans[0] == char and trans[1] not in result:
				stack.append(trans[1])
				result.append(trans[1])

	# returnez lista starilor gasite
	return result