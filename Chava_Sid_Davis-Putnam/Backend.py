def read_output_file(file_path):
    with open(file_path, "r") as file:
        content = file.read().split('0\n')  # Split by '0' followed by a newline
        solution_str = content[0].strip()
        back_matter_str = content[1].strip()
    return solution_str, back_matter_str


# getting solution from dpll output
def parse_solution(solution_str):
    # Check if the first line is "No solution found"
    if solution_str.startswith('No solution found'):
        return None  # or return {} to return an empty dictionary instead

    solution = {}
    for line in solution_str.split('\n'):
        if not line:
            continue
        var, val = line.split()
        solution[int(var)] = True if val == 'T' else False
    return solution


# writing solution after T F values have been read
def write_solution(solution, back_matter_str, output_file_path):
    with open(output_file_path, "w") as out_file:
        for line in back_matter_str.split('\n'):
            parts = line.split()
            index = int(parts[0])
            # Check if this index is part of the solution and if it represents a jump
            if solution.get(index, False) and parts[1].startswith("Jump"):
                out_file.write(' '.join(parts[1:]) + '\n')

def main():
    input_file_path = input("Enter the input file path: ")
    output_file_path = input("Enter the output file path: ")
    solution_str, back_matter_str = read_output_file(input_file_path)
    solution = parse_solution(solution_str)

    if solution is None:
        # If there is no solution, write "No solution found" to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write("No solution found\n")
        print("No solution was found. Written 'No solution found' to the output file.")
    else:
        # If a solution exists, proceed with normal processing
        print("Parsed solution:", solution)
        write_solution(solution, back_matter_str, output_file_path)
        print("Done writing the final solution to the output file.")


if __name__ == "__main__":
    main()