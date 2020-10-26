def arc_consistency():
    queue = [(i, j) for i in constraint_graph for j in constraint_graph[i]]
    while queue:
        arc = queue.pop(0)
        xi, xj = arc[0], arc[1]
        inconsistent, empty_domain = remove_inconsistent(xi, xj)
        if inconsistent:
            for xk in constraint_graph[xi]:
                queue.append((xk, xi))
        if empty_domain:
            return False
    return True


def remove_inconsistent(xi, xj):
    removed = False
    empty = False
    for x in domains[xi]:
        satisfy_constraint = False
        for y in domains[xj]:
            if y != x:
                satisfy_constraint = True
                break
        if not satisfy_constraint:
            domains[xi].remove(x)
            if not domains[xi]:
                empty = True
            removed = True
    return removed, empty


if __name__ == '__main__':
    mode = input("Introduceti modul de preluare date(A(tastatura), B(date existente)):")
    if mode.upper() == 'B':
        constraint_graph = {"T": ["V"], "WA": ["NT", "SA"], "NT": ["WA", "Q", "SA"], "SA": ["WA", "NT", "Q", "NSW", "V"], "Q": ["NT", "SA", "NSW"], "NSW": ["Q", "SA", "V"], "V": ["SA", "NSW", "T"]}
        domains = {"WA": ["r"], "NT": ["r", "b", "g"], "SA": ["r", "b", "g"], "Q": ["g"], "NSW": ["r", "b", "g"], "V": ["r", "b", "g"], "T":["r", "b", "g"]}
        is_consistent = arc_consistency()
        print(is_consistent)
        print(domains)
    elif mode.upper() == "A":
        variables = input("Introduceti variabilele(e.g WA T NT):")
        constraint_graph = {var:[] for var in variables.split()}
        domains = {var:[] for var in variables.split()}
        for var in variables.split():
            neighbours = input("Introduceti vecinii variabilei {}:".format(var))
            constraint_graph[var] = neighbours.split()
        for var in variables.split():
            colors = input("Introduceti culorile disponibile {}:".format(var))
            domains[var] = colors.split()
        is_consistent = arc_consistency()
        print(is_consistent)
        print(domains)