import time

def read_file(file_path):
    with open(file_path, "r") as file:
        clauses = []
        back_matter = []
        reading_clauses = True

        for line in file:
            stripped_line = line.strip()

            if stripped_line == '0':
                reading_clauses = False
            elif reading_clauses:
                clause = [int(word) for word in stripped_line.split()]
                clauses.append(clause)
            else:
                back_matter.append(stripped_line)

    return clauses, back_matter

def emptyClause(CS):
    return [] in CS

def easyCase(CS, B):
    # Initialize the set of unit literals.
    unit_literals = set()
    for clause in CS:
        if len(clause) == 1:  # Check for singletons.
            unit_literals.add(clause[0])
            if(-clause[0] in unit_literals):  # Conflict detected.
                return [[]], B
            B[abs(clause[0])] = clause[0] > 0  # Assign the value to the atom in the bindings.
            CS.remove(clause)  # Remove the singleton clause.
    

    
    new_CS = []  # Will hold the updated clauses after propagation.

    for clause in CS:
        should_add = True
        new_clause = []  # Create a new list to store the updated clause.
        for atom in clause:
            if atom in unit_literals:
                should_add = False  # Don't add this clause to new_CS.
                break
            elif -atom in unit_literals:
                continue  # Skip this atom, don't add it to new_clause.
            else:
                new_clause.append(atom)  # Add the atom to new_clause if it's not negated in unit_literals.
        
        if should_add:
            if not new_clause:  # If new_clause is empty after removing atoms, a contradiction is found.
                return [[]], B
            new_CS.append(new_clause)  # Add the updated clause to new_CS if it's not to be skipped.



            

    # Return the updated clause set and bindings.
    return new_CS, B






def propagate(CS, B, A, V):
    B[A] = V
    new_CS = []  # Will hold the updated clauses after propagation.

    for clause in CS:
        # If the current assignment satisfies the clause, skip it entirely.
        if (A in clause and V) or (-A in clause and not V):
            continue  # Skip adding this clause to new_CS since it's satisfied.

        # Otherwise, remove the negated atom if it's present, because it's now irrelevant.
        new_clause = [x for x in clause if x != (-A if V else A)]

        # If the new_clause is empty, indicate a conflict and return immediately.
        if not new_clause:
            return [[]], B  # Conflict detected.

        # Otherwise, add the modified clause to the new set.
        new_CS.append(new_clause)

    return new_CS, B








# The main DPLL function and additional necessary logic will follow.
def dpll(CS, B):
    if not CS:
        return B  # Successfully found a solution.
    if emptyClause(CS):
        return "Fail"  # Conflict detected immediately.

    # Propagate unit clauses and detect conflicts.
    while True:
        original_CS, original_B = list(CS), dict(B)
        CS, B = easyCase(CS, B)
        if emptyClause(CS):
            return "Fail"  # Conflict detected after propagating unit clauses.

        # If no new bindings are made, break out of the loop.
        if B == original_B:
            break

    # All atoms assigned and no conflict, solution found.
    if not CS:
        return B

    # Select an unassigned atom.
    P = next((abs(atom) for clause in CS for atom in clause if abs(atom) not in B), None)
    if P is None:
        return "Fail"  # No more atoms to assign but no solution found.

    # Try assigning true then false to the unassigned atom and recurse.
    for value in [True, False]:
        print("Trying", P, value)
        new_CS, new_B = propagate(CS, dict(B), P, value)
        if not emptyClause(new_CS):  # Only recurse if no immediate conflict.
            result = dpll(new_CS, new_B)
            if result != "Fail":
                return result  # Valid solution found.

    return "Fail"  # Tried all possibilities for this atom, backtrack.






if __name__ == "__main__":
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    starttime = time.time()

    # Read the CNF clauses and back matter from the input file.
    clauses, back_matter = read_file(input_file_path)

    # Initialize empty bindings; atoms will get their values through the algorithm.
    bindings = {}

    # Apply the DPLL algorithm.
    solution = dpll(clauses, bindings)


    # Identify all atoms involved for output purposes.
    print(f"Solution: {solution}")
    


    # Writing the solution to the output file.
    with open(output_file_path, 'w') as file:
        if solution == "Fail":
            file.write('No solution found.\n')
            file.write('0\n')  # Writing a single line containing 0 if no solution was found.
        else:
            all_atoms = dict(solution.keys())
            # Sort the atoms for output. Use the solution's assignments, defaulting to True if not found.
            for atom in sorted(all_atoms):
                truth_value = solution.get(atom, True)  # Default to True if not in solution.
                truth_str = 'T' if truth_value else 'F'
                file.write(f'{atom} {truth_str}\n')
            file.write('0\n')  # End of solution section.

        # Reproducing back matter from the input file.
        for line in back_matter:
            file.write(line + '\n')

    print("Time taken: ", time.time() - starttime)
    print(f"Solution written to {output_file_path}")