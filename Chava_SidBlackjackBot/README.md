Sid Chava - Programming Assignment 3
NetID: sc9423

To run the the file, run: python3 ./prog3.py (must be in the same director). If not in the same directory, you can replace ./prog3.py by the path that can be obtained by rightclicking.

Upon running it will ask for the following input paramaters: number of dice, number of sides on each dice, lower and upper target scores, number of games to simulate, and the hyperparameter M. After typing each one simply hit enter to move to the next. When you have finished with M, the program will run through the game simulation, using six functions. The program will run the experiment based on the number of games and hyperparameter. Choosing different ratios of the number of games and M will yield different results as M reperesents the speed at which the program moves from exploring to exploiting, 

The output of the program will be two arrays. The first will be an array of the best move at every combination (# of times to roll the dice). The second is the probability of winning provided the right number of dice was rolled at those states.