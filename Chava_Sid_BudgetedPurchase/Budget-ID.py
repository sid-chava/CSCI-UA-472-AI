
file_path = "Chava_Sid_BudgetedPurchase/input.txt"



# Read the file
def read_file(file_path):
    with open(file_path, "r") as file:
        V, B, output_type = file.readline().split()
        V, B = int(V), int(B)
        output_type = output_type.strip()
       
        object_list = []
        for line in file:
            object_name, value, price = line.split()
            value, price = int(value), int(price)
            object_name = object_name.strip()
            object_list.append((object_name, value, price))

    return V, B, output_type, object_list

#iterative deepening, at each level it will run a dfs to see if we can reach the goal state
def iterative_deepening(V, B, output_type, object_list, current_set, current_value, current_price, solutions):
    #dfs run at each depth
    for i in range(0, len(object_list)):
        if output_type =="V": print("Depth:", i+1)
        if(dfs(0, 1, i+1, V, B, output_type, object_list, current_set, current_value, current_price, solutions)):
            for solution in solutions:
                # return solution set if found
                print("\nSolution found:", [x[0] for x in solution], " Value: ", sum([x[1] for x in solution]), " Price: ", sum([x[2] for x in solution]))
            return
        print("\n")
    print("No solution found")


def dfs(item_index, depth, max_depth, V, B, output_type, object_list, current_set, current_value, current_price, solutions):
    if depth > max_depth or current_price > B or item_index >= len(object_list):
        return False
    
    #moving down the index of the object list, seeing if we can add the object to the set
    for i in range(item_index, len(object_list)):
        item = object_list[i]
        if current_price + item[2] <= B:
            next_value = current_value + item[1]
            next_price = current_price + item[2]
            current_set.append(item)
            if output_type == "V":
                print([x[0] for x in current_set], "Value: ", next_value, "Price: ", next_price)
            if next_value >= V:
                solutions.append(current_set.copy())
                return True
            # increment index and depth (we added the object)) and run dfs deeper on the exploration
            if dfs(i + 1, depth + 1, max_depth, V, B, output_type, object_list, current_set, next_value, next_price, solutions):
                return True  
            # Backtrack
            current_set.pop()
    return False  

#main function with file input
if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    V, B, output_type, object_list = read_file(file_path)
    solutions = []
    iterative_deepening(V, B, output_type, object_list, [], 0, 0, solutions)



 


    
            
        
    





    
    
    

