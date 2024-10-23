import heapq
from copy import deepcopy
import time

# pre-defined initial puzzle states for the user to choose from
trivial = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 0]]

very_easy = [[1, 2, 3],
             [4, 5, 6],
             [0, 7, 8]]

easy = [[1, 2, 3],
        [5, 0, 6],
        [4, 7, 8]]

medium = [[1, 3, 6],
          [5, 0, 2],
          [4, 7, 8]]

hard = [[1, 6, 7],
        [5, 0, 3],
        [4, 8, 2]]

impossible = [[7, 1, 2],
              [4, 8, 5],
              [6, 3, 0]]

# the goal state of the 8 puzzle 
solved = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 0]]

# var equates to size of the puzzle (i.e. 3 for 3x3 puzzle/8 puzzle)
# can be changed to account for 15-puzzle, 25-puzzle, etc.
puzzle_size = 3


class Node:
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle
        self.moves = 0
        self.h = 0
            
    def setHeuristicH(self, h):
        self.h = h
        
    def setMoves(self, moves):
        self.moves = moves
        
    def solved(self) -> bool:
        return (self.puzzle == solved)
    
    def __lt__(self, other):
        return ((self.moves + self.h) < (other.moves + other.h))
    

# function to determine where on the puzzle is the empty/zero space 
def setEmptyTilePosition(puzzle):
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            if (puzzle[i][j] == 0):
                return [i, j]
            
            
# function to calcualte the total number of misplaced tiles in the puzzle
# this number equates to h in the heuristic function   
def calculateMisplacedTiles(puzzle) -> int:
    num = 0
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            if ((puzzle[i][j] != solved[i][j]) and (puzzle[i][j])):
                num+=1
                
    return num


# function to calculate the manhattan distance heuristic of an eight puzzle
# used as a heuristic for A* search 
def calculateManhattanHeuristic(puzzle) -> int:
    distance = 0
    solved_dict = {1: [0,0], 2: [0,1], 3: [0,2], 4: [1,0], 
                   5: [1,1], 6: [1,2], 7: [2,0], 8: [2,1]}
    
    for i in range(puzzle_size):
        for j in range(puzzle_size):
            if (puzzle[i][j] != 0 and puzzle[i][j] != solved[i][j]):
                coordinate = []
                coordinate = solved_dict[puzzle[i][j]]
                distance += abs(i-coordinate[0]) + abs(j-coordinate[1])
                
    return int(distance)

def generateNewNode(initial_node, new_puzzle, algorithm):
    new_node = Node(new_puzzle)
    new_node.setMoves(initial_node.moves + 1)
    
    if algorithm == "1":
        new_node.setHeuristicH(0)
    elif algorithm == "2":
        h = calculateMisplacedTiles(new_node.puzzle)
        new_node.setHeuristicH(h)
    elif algorithm == "3":
        h = calculateManhattanHeuristic(new_node.puzzle)
        new_node.setHeuristicH(h)
        
    return new_node

def move(initial_node, empty_tile, direction, algorithm):
    x, y = empty_tile
    temp_puzle = deepcopy(initial_node.puzzle)
    
    if direction == 'up' and x > 0:
        temp_puzle[x][y], temp_puzle[x-1][y] = temp_puzle[x-1][y], temp_puzle[x][y]
    elif direction == 'down' and x < puzzle_size - 1:
        temp_puzle[x][y], temp_puzle[x+1][y] = temp_puzle[x+1][y], temp_puzle[x][y]
    elif direction == 'left' and y > 0:
        temp_puzle[x][y], temp_puzle[x][y-1] = temp_puzle[x][y-1], temp_puzle[x][y]
    elif direction == 'right' and y < puzzle_size - 1:
        temp_puzle[x][y], temp_puzle[x][y+1] = temp_puzle[x][y+1], temp_puzle[x][y]
    else:
        return None
    
    return generateNewNode(initial_node, temp_puzle, algorithm)
  
    if (empty_tile[1] != puzzle_size - 1):
        # shift empty tile to the right one space
        temp_puzzle = deepcopy(initial_node.puzzle)
        empty_x = empty_tile[0]
        empty_y = empty_tile[1]
        shifted = temp_puzzle[empty_x][empty_y+1]
        temp_puzzle[empty_x][empty_y] = shifted
        temp_puzzle[empty_x][empty_y+1] = 0
        
        # calculate heuristics
        new_node = Node(temp_puzzle)
        new_node.setMoves(initial_node.moves+1)
        if (algorithm == "1"):
            new_node.setHeuristicH(0)
        elif (algorithm == "2"):
            h = calculateMisplacedTiles(new_node.puzzle)
            new_node.setHeuristicH(h)
        elif (algorithm == "3"):
            h = calculateManhattanHeuristic(new_node.puzzle)
            new_node.setHeuristicH(h)
            
        return new_node
  
# the general search algorithm to solve the 8 puzzle problem
# this function accepts custom puzzles or pre-defined puzzles and 
# allows for use of Uniform Cost search and A* with either the 
# misplaced tile heuristic or the manhattan distance heuristic
def generalSearch(algorithm, puzzle, heuristic):
    # creating a priority queue and initializing it with the initial puzzle
    root = Node(puzzle)
    root.setHeuristicH(heuristic)
    empty_tile_pos = setEmptyTilePosition(root.puzzle)
    p_queue = []
    heapq.heappush(p_queue, root)
    heapq.heapify(p_queue)
    num_expanded_nodes = 1
    max_queue_len = 1
    
    # set to store puzzles that have been traversed/analyzed
    puzzle_states = set()
    
    while (len(p_queue) > 0):
        # analyze first node for a solution
        max_queue_len = max(len(p_queue), max_queue_len)
        head_node = heapq.heappop(p_queue)
        
        # convert the puzle to tuple for checking and storing
        puzzle_tuple = tuple(map(tuple, head_node.puzzle))
        
        # if the node has the solution print to user max queue size, depth, and algorithm runtime
        if (head_node.solved()):
            # print puzzle solution path
            print("Path to solved puzzle:")
            for i in puzzle_states:
                printPuzzle(i)
            
            print("Number of nodes expanded: ", num_expanded_nodes)
            print("Max queue size: ", max_queue_len)
            print("Answer found at depth: ", head_node.moves)
            return
        # if the node is not one of the already checked puzzle states, we can analyze it and create new states from it
        if (puzzle_tuple not in puzzle_states):
            # show user which puzzle is being expanded
            print("The best state to expand with a g_n = ", head_node.moves, "and h_n = ", head_node.h, "is...")
            printPuzzle(head_node.puzzle)
            num_expanded_nodes+=1
            empty_tile_pos = setEmptyTilePosition(head_node.puzzle)
            
            # compute movements here to create new puzzle nodes and add them to a list
            new_nodes = []
            new_nodes.append(move(head_node, empty_tile_pos, 'down', algorithm))
            new_nodes.append(move(head_node, empty_tile_pos, 'up', algorithm))
            new_nodes.append(move(head_node, empty_tile_pos, 'right', algorithm))
            new_nodes.append(move(head_node, empty_tile_pos, 'left', algorithm))
              
            # check that the nodes are not empty and add them to the priority queue
            for temp in new_nodes:
                if temp is not None:
                    temp_puzzle_tuple = tuple(map(tuple, temp.puzzle))
                    if temp_puzzle_tuple not in puzzle_states:
                        heapq.heappush(p_queue, temp)
                        max_queue_len = max(len(p_queue), max_queue_len)
            
            # add the original node to the list containing already visited puzzles
            puzzle_states.add(puzzle_tuple)
    
    print("No solution found")
            
# print the n x n puzzle in its entirety            
def printPuzzle(puzzle):
    for row in puzzle:
        print(" | ".join(map(str, row)))
    print('\n')
    

# main driver code for the program
def main():
    # get user input to determine if they want to create a custom puzzle or use a default one
    game_mode = input("Welcome to my 8-Puzzle Solver. Type 1 to use a default puzzle, or 2 to " + "make your own.\n")
    
    # user chooses a default puzzle; have the user choose one based on puzzle difficulty
    if (game_mode == "1"):
        default_puzzle = []
        
        difficulty = input("You chose to use one of the default puzzles in this program. Enter your desired"
              + " difficulty on a scale from 0 to 5.\n")
        
        if (difficulty == "0"):
            print("Difficulty of 'trivial' selected.")
            default_puzzle = trivial
        elif (difficulty == "1"):
            print("Difficulty of 'very easy' selected.")
            default_puzzle = very_easy
        elif (difficulty == "2"):
            print("Difficulty of 'easy' selected.")
            default_puzzle = easy
        elif (difficulty == "3"):
            print("Difficulty of 'medium' selected.")
            default_puzzle = medium
        elif (difficulty == "4"):
            print("Difficulty of 'hard' selected.")
            default_puzzle = hard
        elif (difficulty == "5"):
            print("Difficulty of 'impossible' selected.")
            default_puzzle = impossible
        
        # finally have user choose which algorithm to solve the puzzle
        chooseAlgorithm(default_puzzle)
    # user wants to input a custom puzzle
    elif (game_mode == "2"):
        custom_puzzle = []
        
        print("Enter the numbers for the puzzle one by one. Hit enter after inputting each number" +
              "\nNine valid numbers should be entered, including 0 for the blank space.\n")
        
        # checks for input of numbers for the puzzle
        for i in range(puzzle_size):
            arr = []
            for j in range(puzzle_size):
                arr.append(int(input()))
            custom_puzzle.append(arr)
        
        # finally have user choose which algorithm to solve the puzzle
        chooseAlgorithm(custom_puzzle)
    
    
# ask the user which algorithm to use to solve the puzzle
def chooseAlgorithm(puzzle):
    algorithm = input("Select an algorithm:\n1. Uniform Cost Search\n2. Misplaced Tile Heuristic"
                      + "\n3. Manhattan Distance Heuristic\n")
    start_time = time.time()
    
    # user has chosen the Uniform Cost Search; heuristic is set to 0
    if algorithm == "1":
        print("You chose: Uniform Cost Search")
        generalSearch(algorithm, puzzle, 0)
    # user has chosen A* with the Misplaced Tile Heuristic; heuristic is computed using misplaced tiles function
    elif algorithm == "2":
        print("You chose: Misplaced Tile Heuristic Search")
        h = calculateMisplacedTiles(puzzle)
        generalSearch(algorithm, puzzle, h)
    # user has chosen A* with the Manhattan Distance Heuristic; heuristic is computed using manh. dist. function
    elif algorithm == "3":
        print("You chose: Manhattan Distance Heuristic Search")
        h = calculateManhattanHeuristic(puzzle)
        generalSearch(algorithm, puzzle, h)
        
    end_time = time.time()
    print(f'Time taken: {end_time - start_time:.2f} seconds...')

if __name__ == "__main__":
    main()
