class Peg:
    def __init__(self, hole, time, number):
        self.hole = hole
        self.time = time
        self.number = number  # Unique number for each Peg

    def __repr__(self):
        return f"Peg({self.hole},{self.time})"

class Jump:
    def __init__(self, start, over, end, time, number):
        self.start = start
        self.over = over
        self.end = end
        self.time = time
        self.number = number  #Unique number for each Jump
    def __repr__(self):
        return f"Jump({self.start},{self.over},{self.end},{self.time})"


def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_holes, initial_empty = map(int, lines[0].strip().split())
        triples = [list(map(int, line.strip().split())) for line in lines[1:]]

    # Generate and number AllJumps first
    current_num = 1
    AllJumps = []
    # Iterate over time steps first
    for time in range(1, num_holes - 1):
        # Then iterate over each triple for the current time step
        for triple in triples:
            # Assign numbers to Jumps forwards
            AllJumps.append(Jump(triple[0], triple[1], triple[2], time, current_num))
            current_num += 1
            # Assign numbers to Jumps backwards
            AllJumps.append(Jump(triple[2], triple[1], triple[0], time, current_num))
            current_num += 1

        

    # Update current_num for Pegs after numbering all Jumps
    AllPegs = [[Peg(hole, time, current_num + (hole - 1) * (num_holes - 1) + (time - 1)) for time in range(1, num_holes)] for hole in range(1, num_holes + 1)]
    current_num += num_holes * (num_holes - 1) # Adjust in case more Pegs are to be numbered beyond this

    AllPegs = [peg for sublist in AllPegs for peg in sublist]
    return num_holes, initial_empty, AllPegs, AllJumps

#Axiom 1
def generate_precondition_clauses(AllJumps, AllPegs):
    clauses = []
    for jump in AllJumps:
        # Find corresponding Pegs for the current time step of the jump
        start_peg = next(peg for peg in AllPegs if peg.hole == jump.start and peg.time == jump.time)
        over_peg = next(peg for peg in AllPegs if peg.hole == jump.over and peg.time == jump.time)
        
        # Find the end_peg for the next time step (after the jump)
        end_peg = next(peg for peg in AllPegs if peg.hole == jump.end and peg.time == jump.time)

        # Generate clauses
        # If Jump then start Peg and over Peg, and not end Peg
        clauses.append(f"-{jump.number} {start_peg.number}")
        clauses.append(f"-{jump.number} {over_peg.number}")
        clauses.append(f"-{jump.number} -{end_peg.number}")

    return clauses

#Axiom 2
def generate_causal_clauses(AllJumps, AllPegs):
    clauses = []
    for jump in AllJumps:
        
        # Find corresponding Pegs for the current time step of the jump
        start_peg = next(peg for peg in AllPegs if peg.hole == jump.start and peg.time == jump.time+1)
        
        over_peg = next(peg for peg in AllPegs if peg.hole == jump.over and peg.time == jump.time+1)
        
        
        # Find the end_peg for the next time step (after the jump)
        end_peg = next(peg for peg in AllPegs if peg.hole == jump.end and peg.time == jump.time+1)

        # Generate clauses
        # If Jump then ~start Peg and ~over Peg, and end Peg at the next time step
        clauses.append(f"-{jump.number} -{start_peg.number}")
        clauses.append(f"-{jump.number} -{over_peg.number}")
        clauses.append(f"-{jump.number} {end_peg.number}")
    

    return clauses

#Axiom 3a
def generate_frame_clauses1(AllJumps, AllPegs):
    clauses = []
    for peg in AllPegs:
        if peg.time == max(peg.time for peg in AllPegs):
            continue


        
        # Find all jumps that involve the current peg's hole at the current time step
        relevant_jumps = [jump for jump in AllJumps if (jump.start == peg.hole and jump.time == peg.time) or
                           (jump.over == peg.hole and jump.time == peg.time)]
        
  
        
        clause_parts = [f"-{peg.number}", f"{peg.number + 1}"]
        for jump in relevant_jumps:
            clause_parts.append(f"{jump.number}")
        
       
        
        # Combine for CNF
        combined_clause = " ".join(clause_parts)
        clauses.append(combined_clause)
        
      
    
    return clauses

#Axiom 3b
def generate_frame_clauses2(AllJumps, AllPegs):
    clauses = []
    for peg in AllPegs:
        if peg.time == max(peg.time for peg in AllPegs):
            continue

        
        # Find all jumps that involve the current peg's hole at the current time step
        relevant_jumps = [jump for jump in AllJumps if
                           (jump.end == peg.hole and jump.time == peg.time)]
        
        clause_parts = [f"{peg.number}", f"-{peg.number + 1}"]
        for jump in relevant_jumps:
            clause_parts.append(f"{jump.number}")
        
        # Combine for CNF
        combined_clause = " ".join(clause_parts)
        clauses.append(combined_clause)
    
    return clauses

#Axiom 4a
def generate_conflict_clause(AllJumps, num_holes):
    clauses = []
    # Iterate over time steps
    for time in range(1, num_holes):  # Time starts from 1 to num_holes - 1
        # Find all jumps at the current time
        jumps_at_time = [jump for jump in AllJumps if jump.time == time]
        # Generate conflict clauses for all pairs of jumps at this time
        for i in range(len(jumps_at_time)):
            for j in range(i + 1, len(jumps_at_time)):
                clause = f"-{jumps_at_time[i].number} -{jumps_at_time[j].number}"
                clauses.append(clause)
    return clauses



#Axiom 5
def generate_starting_state_clauses(num_holes, initial_empty, AllPegs):
    clauses = []
    # Iterate through all the pegs and set the initial state
    for peg in AllPegs:
        if peg.time == 1:  # Initial time step
            if peg.hole == initial_empty:
                # The initial empty hole, so this peg should not be present
                clauses.append(f"-{peg.number}")
            else:
                # This hole starts with a peg in it
                clauses.append(f"{peg.number}")
    return clauses

#Axiom 6
def generate_ending_state_clauses(num_holes, AllPegs):
    clauses = []
    final_time = num_holes - 1  # The final time step
    at_least_one_clause = []

    #clause for at least one peg remaining at the final time
    for i in range(1, num_holes + 1):
        peg_i = next(peg for peg in AllPegs if peg.hole == i and peg.time == final_time)
        at_least_one_clause.append(f"{peg_i.number}")
    
    #add clause for at least one peg remaining to the beginning of the list
    clauses.append(' '.join(at_least_one_clause))

    # No two holes have a peg at the final time
    for i in range(1, num_holes + 1):
        for j in range(i + 1, num_holes + 1):
            peg_i = next(peg for peg in AllPegs if peg.hole == i and peg.time == final_time)
            peg_j = next(peg for peg in AllPegs if peg.hole == j and peg.time == final_time)
            clauses.append(f"-{peg_i.number} -{peg_j.number}")
    
    return clauses


def main(input_path, output_path):
    num_holes, initial_empty, AllPegs, AllJumps = read_input(input_path)
    precondition_clauses = generate_precondition_clauses(AllJumps, AllPegs)
    causal_clauses = generate_causal_clauses(AllJumps, AllPegs)
    frame_clauses = generate_frame_clauses1(AllJumps, AllPegs)
    frame_clauses += generate_frame_clauses2(AllJumps, AllPegs)
    conflict_clause = generate_conflict_clause(AllJumps, num_holes)
    starting_state_clauses = generate_starting_state_clauses(num_holes, initial_empty, AllPegs)
    ending_state_clauses = generate_ending_state_clauses(num_holes, AllPegs)

    
    with open(output_path, 'w') as file:
        
        for clause in precondition_clauses:
            file.write(clause + '\n')
        
        for clause in causal_clauses:
            file.write(clause + '\n')
        
        for clause in frame_clauses:
            file.write(clause + '\n')
        
        for clause in conflict_clause:
            file.write(clause + '\n')
        
        for clause in starting_state_clauses:
            file.write(clause + '\n')
        
        for clause in ending_state_clauses:
            file.write(clause + '\n')
        file.write("0\n")
        for jump in AllJumps:
            file.write(f"{jump.number} {jump}\n")
        for peg in AllPegs:
            file.write(f"{peg.number} {peg}\n")
        # Print statements for testing
    
    counter = 0

    print("\nPrecondition Clauses:")
    for clause in precondition_clauses:
        print(clause)
        
    print("\nCausal Clauses:")
    for clause in causal_clauses:
        print(clause)
    print("\nFrame Clauses:")
    for clause in frame_clauses:
        print(clause)
    print("\nConflict Clause:")
    for clause in conflict_clause:
        print(clause)
        counter += 1
    print("\nStarting State Clauses:")
    for clause in starting_state_clauses:
        print(clause)
    print("\nEnding State Clauses:")
    for clause in ending_state_clauses:
        print(clause)
    print("0\n")
    for jump in AllJumps:
        print(f"{jump.number} {jump}")
    for peg in AllPegs:
        print(f"{peg.number} {peg}")
    
    print(f"\Conflict: {counter}")


if __name__ == "__main__":
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    main(input_file_path, output_file_path)
    
