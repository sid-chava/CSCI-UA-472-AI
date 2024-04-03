Sid Chava - Programming Assignment 2
NetID: sc9423

To run the the Front_End file, run: python3 ./Front_End.py

Upon running it will ask for a file path for the input file. (can be obtained by right-clicking on your input path and clicking copy path)
It will also ask for an output file path (if it doesnt exist, then the file will be created in the same directory).

Example input file path: Chava_Sid_Davis-Putnam/frontend_input.txt
Example output file path: frontend_output.txt

Takes in an input file that displays a peg game and converts it into CNF. Creates clauses based on 6 axioms. Creates a key to decipher actions from the numbered clause


To run the DPLL file, run: python3 ./Davis_Putnam.py

Upon running it will ask for a file path for the input file. (can be obtained by right-clicking on your input path and clicking copy path)
It will also ask for an output file path (if it doesnt exist, then the file will be created in the same directory).

Example input file path: Chava_Sid_Davis-Putnam/frontend_output.txt
Example output file path: dpll_output.txt

To run the DPLL file, run: python3 ./Backend.py

Upon running it will ask for a file path for the input file. (can be obtained by right-clicking on your input path and clicking copy path)
It will also ask for an output file path (if it doesnt exist, then the file will be created in the same directory).

Example input file path: Chava_Sid_Davis-Putnam/dpll_output.txt
Example output file path: solution.txt

This file takes either the T/F assignments for all the clauses, and uses the key given to turn the assignments into the jumps required to solve the clauses. If there is no solution it will just print no solution.


