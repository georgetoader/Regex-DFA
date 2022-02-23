# Toader George-Catalin 331CB

import sys
from header import *

def parse_prenex(prenex_list):
    stack = []
    regex = None
    i = 0
    # daca am ajuns la finalul listei inseamna ca am terminat de parsat prenex-ul
    while i < len(prenex_list):
        # verific daca este expresie sau caracter, iar in primul caz si tipul ei
        # folosesc clase pentru reprezentarea interna asa cum este sugerat in cerinta
        if prenex_list[i] == "UNION":
            stack.append(Union(2))
        elif prenex_list[i] == "CONCAT":
            stack.append(Concat(2))
        elif prenex_list[i] == "STAR":
            stack.append(Star(1))
        elif prenex_list[i] == "PLUS":
            stack.append(Plus(1))
        else:
            # nu este expresie, deci este caracter
            # verific numarul de parametrii necesari ai expresiei din varful stivei
            if stack[-1].get_par_num() == 2:
                # adaug primul parametru
                stack[-1].set_par1(prenex_list[i])
                stack[-1].decrease_par_num()
            elif stack[-1].get_par_num() == 1:
                # adaug al doilea parametru
                stack[-1].set_par2(prenex_list[i])
                regex = stack.pop()
                # parcurg expresiile ce mai au nevoie de un singur parametru
                while len(stack) >= 1 and stack[-1].get_par_num() == 1:
                    stack[-1].set_par2(regex)
                    regex = stack.pop()
                # stiva mai are elemente deci avem expresie cu 2 parametrii
                if len(stack) > 0 and stack[-1].get_par_num() == 2:
                    stack[-1].set_par1(regex)
                    stack[-1].decrease_par_num()
        i += 1

    return regex

def main():
    # separ prenex-ul in cuvinte
    with open(sys.argv[1], "r") as f_in:
        prenex_list = f_in.read().split()
    f_out = open(sys.argv[2], "w")

    # parsarea formei prenex
    if len(prenex_list) <= 1:
        regex = prenex_list[0]
    else:
        regex = parse_prenex(prenex_list)

    # transformarea Regex-NFA folosind algoritmul lui Thompson
    nfa = NFA(regex)

    #transformarea NFA-DFA
    dfa = DFA(nfa)
    dfa.write_dfa(f_out)

if __name__ == "__main__":
    main()
