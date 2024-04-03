

import random


#reads input
def read_file(file_path):
    with open(file_path, "r") as file:
        V, B, output_type, restart_count = file.readline().split()
        V, B, restart_count= int(V), int(B), int(restart_count)
        output_type = output_type.strip()

        object_list = []
        for line in file:
            object_name, value, price = line.split()
            value, price = int(value), int(price)
            object_list.append((object_name, value, price))

        print(object_list)
    return V, B, output_type, object_list, restart_count


# accepts the list of objects, how many times to randomly restart, and parameters for the goal state
def hill_climb(V, B, output_type, object_list, restart_count, solutions):

    # for each restart, generate a random state and explore neighbors
    for i in range(0, restart_count):
        random_state = []
        current_value = 0
        current_price = 0
        error = 0

        #randomly select objects to add to the state
        for item in object_list:
            if random.random() > 0.5:
                random_state.append(item)
                current_value += item[1]
                current_price += item[2]
        error = max(current_price - B, 0) + max(V - current_value, 0)
        if output_type =="V": print("Restart with random state:", random_state, "Value:", current_value, "Price:", current_price, "Error:", error)
        if error == 0:
            solutions.append(random_state)
            for solution in solutions:
                print("Solution ",solution)
            return
        
        #explore neighbors if start isnt goal, only break if we get the goal state, but if local max reached, go to next restart
        if neighbor_explore(V, B, output_type, object_list, random_state, [], current_value, current_price, error, solutions):
            print("Solution found", [item[0] for item in solutions[0]], "Value:", sum([item[1] for item in solutions[0]]), "Price:", sum([item[2] for item in solutions[0]]) )
            return
        print("\n")
    
    #if all restarts exhausted, no solution found
    print("No solution found")

#explore neighbors of a state by iterating through list and either adding it if item isnt in the list, or removing it if it is
def neighbor_explore(V, B, output_type, object_list, starting_state, next_state, starting_value, starting_price, error, solutions):
    starting_error = error
    best_error = error
    best_state = starting_state.copy()
    best_price = starting_price
    best_value = starting_value
    if output_type =="V": print("Neighbors: ")

    #updating price and value as we iterate through the list
    for obj in object_list:
        next_state = starting_state.copy()
        next_price = 0
        next_value = 0
        new_error = 0
        if obj in next_state:
            next_state.remove(obj)
            next_value = starting_value - obj[1]
            next_price = starting_price - obj[2]
        else:
            next_state.append(obj)
            next_price = starting_price+obj[2]
            next_value = starting_value+obj[1]

        #checking error after checking next state, if its better than the best error, update best error and best state/values
        new_error = max(next_price - B, 0) + max(V - next_value, 0)
        if output_type =="V": print([item[0] for item in next_state], "Value: ", next_value, "Price: ", next_price, "Error: ", new_error)
        if new_error < best_error:
            best_error = new_error
            best_state = next_state.copy()
            best_value = next_value
            best_price = next_price

        #break if we find the goal state
        if new_error == 0:
            solutions.append(next_state)
            return True
    #if state is better, take that and conitnue exploring neighbors
    if best_error < starting_error:
        if output_type =="V": print("\nMove to: ", best_state)
        return neighbor_explore(V, B, output_type, object_list, best_state, next_state, best_value, best_price, best_error, solutions)
    else:
        print("\nSearch Failed")
        return False

            

            


        

#main function with file input
if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    V, B, output_type, object_list, restart_count = read_file(file_path)
    solutions = []
    hill_climb(V, B, output_type, object_list, restart_count, solutions)
