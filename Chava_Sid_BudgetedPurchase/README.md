Sid Chava - Programming Assignment 1
NetID: sc9423

To run the the iterative deepening file, run: python3 ./Budget-ID.py

Upon running it will ask for a file path for the input file. (can be obtained by right-clicking on your input path and clicking copy path)

Example file path: Chava_Sid_BudgetedPurchase/input.txt

The program first takes the input file and saves the goal parameters, and converts it to a readable list of objects. That input file information is then passed to the iterative deeepening program which then runs dfs an incrementally increasing depth to find the first potential solution



To run the hill climbing file, run: python3 ./Budget-HC.py

Upon running it will ask for a file path for the input file. (can be obtained by right-clicking on your input path and clicking copy path)

Example file path: Chava_Sid_BudgetedPurchase/input.txt

The program first takes the input file and saves the goal parameters, and converts it to a readable list of objects. It will also save the amount of restarts given by the file. This information is then passed to the hill climb algorithm, which will randomly generate a starting state and check its neighbors (recursively until local max) until a solution is found, or it reached the limit on the restart count (specified by the input file)


Both programs will output any potential solution (hc might not find in the given amount of restarts), or output "No solution found"

This program assumes the input files are formatted corrected when passed to the respective program. 

The output is printed to the console.

