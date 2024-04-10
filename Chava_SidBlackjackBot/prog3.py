import random
import numpy as np


 # Use random.choices to pick a random value from  probability distribution
def chooseFromDist(p):
    indices = list(range(1, len(p) + 1))
   
    chosen_index = random.choices(indices, weights=p, k=1)[0]
    
    return chosen_index


# Roll n dice with n sides each and return the sum of the rolls
def rollDice(NDice, NSides):
    total = 0
    for _ in range(NDice):
        roll = random.randint(1, NSides)
        total += roll
    return total



#Picking the best dice to roll based on the win probability, following the formulas for f and p.
def chooseDice(ScoreA, ScoreB, LoseCount, WinCount, NDice, M):
    K = NDice
    #Using K+1 for 1 indexing
    f = [0] * (K + 1)
    for k in range(1, K + 1):
        if WinCount[ScoreA][ScoreB][k] + LoseCount[ScoreA][ScoreB][k] == 0:
            f[k] = 0.5
        else:
            f[k] = WinCount[ScoreA][ScoreB][k] / (WinCount[ScoreA][ScoreB][k] + LoseCount[ScoreA][ScoreB][k])
    
    BestMove = np.argmax(f[1:]) + 1
    SumOtherMoves = sum(f[k] for k in range(1, K + 1) if k != BestMove)
    
    T = sum(WinCount[ScoreA][ScoreB][k] + LoseCount[ScoreA][ScoreB][k] for k in range(1, K + 1))
    
    p = [0] * (K + 1)
    p[BestMove] = (T * f[BestMove] + M) / (T * f[BestMove] + K * M)
    for k in range(1, K + 1):
        if k != BestMove:
            p[k] = (1 - p[BestMove]) * (T * f[k] + M) / (SumOtherMoves * T + (K - 1) * M)
    
    return chooseFromDist(p[1:])


def PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    ScoreA, ScoreB = 0, 0
    APlays, BPlays = [], []
    game_over = False

    while not game_over:
        # Player A's turn
        RollDice = chooseDice(ScoreA, ScoreB, LoseCount, WinCount, NDice, M)
        DiceValues = rollDice(RollDice, NSides)
        TotalA = ScoreA + DiceValues
        # Have to maintain the state right before the total hits the target or goes over, before setting ScoreA to that new sum
        
        
        if LTarget <= TotalA <= UTarget:
            #Player A wins
            APlays.append((ScoreA, ScoreB, RollDice))
            game_over = True
            winner, loser = APlays, BPlays
        elif TotalA > UTarget:
            #Player A loses
            APlays.append((ScoreA, ScoreB, RollDice))
            game_over = True
            winner, loser = BPlays, APlays
        else:
            
            APlays.append((ScoreB, ScoreA, RollDice))
            # Now we can update ScoreA for the next turn, after adding the play to APlays
            ScoreA = TotalA 
             

        if game_over:
            break  # Exit the loop if game is over

        # Player B's turn, logic follows
        RollDice = chooseDice(ScoreB, ScoreA, LoseCount, WinCount, NDice, M)
        DiceValues = rollDice(RollDice, NSides)
        TotalB = ScoreB + DiceValues

        
        if LTarget <= TotalB <= UTarget:
            BPlays.append((ScoreB, ScoreA, RollDice))
            game_over = True
            winner, loser = BPlays, APlays
        elif TotalB > UTarget:
            BPlays.append((ScoreB, ScoreA, RollDice))
            game_over = True
            winner, loser = APlays, BPlays
        else:
            BPlays.append((ScoreB, ScoreA, RollDice))
            ScoreB = TotalB  # Update for next turn

    # Based on who actually won the game, increment Win and Lose Counts
    for play in winner:
        WinCount[play[0]][play[1]][play[2]] += 1
    for play in loser:
        LoseCount[play[0]][play[1]][play[2]] += 1

    return LoseCount, WinCount






#Now the arrays are in the final state, for every possible combination, we look for the best move and consequently it's win probability
def extractAnswer(WinCount, LoseCount, LTarget, UTarget, num_dice):
    BestMove = [[0] * (LTarget) for _ in range(LTarget)]
    WinProb = [[0] * (LTarget) for _ in range(LTarget)]

    for X in range(LTarget):
        for Y in range(LTarget):
            best_move = 0
            max_prob = 0

            for k in range(1, num_dice + 1):
                total_games = WinCount[X][Y][k] + LoseCount[X][Y][k]
                if total_games > 0:
                    win_prob = WinCount[X][Y][k] / total_games
                    if win_prob > max_prob:
                        best_move = k
                        max_prob = win_prob

            BestMove[X][Y] = best_move
            WinProb[X][Y] = max_prob

    return BestMove, WinProb

#Top Level Ffunction to initalize arrays and print output
def prog3(NDice, NSides, LTarget, UTarget, NGames, M):
    max_score = UTarget + NDice * NSides  # Maximum possible score

    max_score = UTarget + NDice * NSides  # Maximum possible score

    WinCount = [[[0 for _ in range(NDice + 1)] for _ in range(LTarget)] for _ in range(LTarget)]
    LoseCount = [[[0 for _ in range(NDice + 1)] for _ in range(LTarget)] for _ in range(LTarget)]

    for _ in range(NGames):
        LoseCount, WinCount = PlayGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)

    BestMove, WinProb = extractAnswer(WinCount, LoseCount, LTarget, UTarget, NDice)

    print("Best Move:")
    for X in range(LTarget):
        row = ""
        for Y in range(LTarget): 
            row += str(BestMove[X][Y]) + " "
        print(row)

    print("\nWin Probability:")
    for X in range(LTarget):  
        row = ""
        for Y in range(LTarget):  
            row += f"{WinProb[X][Y]:.4f} "
        print(row)


def main():
    print("Enter the game parameters.")
    
    NDice = int(input("Number of dice (NDice): "))
    NSides = int(input("Number of sides on each die (NSides): "))
    LTarget = int(input("Lower target score (LTarget): "))
    UTarget = int(input("Upper target score (UTarget): "))
    NGames = int(input("Number of games to simulate (NGames): "))
    M = int(input("Hyperparamater (M): "))
    
    prog3(NDice, NSides, LTarget, UTarget, NGames, M)

if __name__ == "__main__":
    main()
