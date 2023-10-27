import math

maximum_moves = 10000
goal_state = [[1,2,3],[4,5,6],[7,8,0]]
final_output = [[0,0,0],[0,0,0]]

def index(i,seq):
    if(len(seq) > 0):
        count = -1
        for x in range(len(seq)):
            if(i == seq[x].cloned_matrix):
                count = x
        return count
    else:
        return -1

class Puzzle:
    def __init__(self):
        self.parent_node = None
        self.heuristic_fvalue = 0
        self.depth = 0
        self.cloned_matrix = []
        for i in range(3):
            self.cloned_matrix.append(goal_state[i][:])
    
    #setter
    def setValue(self, row, col,value):
        self.cloned_matrix[row][col] = value
    
    #getter
    def getValue(self, row, col):
        return self.cloned_matrix[row][col]

    #initialize the 3x3 matrix
    def initMatrix(self, values):
        i = 0
        for row in range(3):
            for col in range(3):
                self.cloned_matrix[row][col] = int(values[i])
                i = i+1
        self.initial_matrix = self.cloned_matrix

    #returns solution path
    def solutionPath(self, path):
        if(self.parent_node == None):
            return path
        else:
            path.append(self)
            return self.parent_node.solutionPath(path)

    #helper function to find current position
    def find(self,value):
        if(value < 0 or value > 8):
            raise Exception("Value Is Out Of Range")

        for row in range(3):
            for col in range(3):
                if self.cloned_matrix[row][col] == value:
                    return row, col

    #finds the next optimal solution
    def possibleNextOptSolution(self):
        row,col = self.find(0)
        possible_matrix_move = []

        if(row > 0):
            possible_matrix_move.append((row-1,col))
        if(col > 0):
            possible_matrix_move.append((row, col-1))
        if(row < 2):
            possible_matrix_move.append((row+1, col))
        if(col < 2):
            possible_matrix_move.append((row, col+1))

        zero = self.find(0)

        def swap_and_clone(x, y):
            p = Puzzle()
            for i in range(3):
                p.cloned_matrix[i] = self.cloned_matrix[i][:]
            temp = p.getValue(*x)
            p.setValue(x[0],x[1],p.getValue(*y))
            p.setValue(y[0],y[1],temp)
            p.depth = self.depth + 1
            p.parent_node = self
            return p
        return map(lambda  pair: swap_and_clone(zero,pair), possible_matrix_move)

    #A* search algorithm
    def aSearch(self, heuristicFunction):       
        input_matrix_list = [self]
        intermediate_matrix_list = []
        move_count = 0

        while len(input_matrix_list) > 0:
            x = input_matrix_list.pop(0)
            move_count += 1
            heuristic_val = heuristicFunction(x)
            x.heuristic_fvalue = heuristic_val

            if(move_count > maximum_moves):
                print("No Solution, Max Iteration Hit")
                return [], move_count
            
            if(x.cloned_matrix == goal_state):
                if len(intermediate_matrix_list) > 0:
                    return x.solutionPath([]), move_count
                else:
                    return [x]
            
            next_possible_position = x.possibleNextOptSolution()
            id_open = id_close = -1
            for move in next_possible_position:
                id_open = index(move.cloned_matrix, input_matrix_list)
                id_close = index(move.cloned_matrix, intermediate_matrix_list)
                heuristic_val = heuristicFunction(move)
                fval = heuristic_val + move.depth

                if(id_close == -1 and id_open == -1):
                    move.heuristic_fvalue = heuristic_val
                    input_matrix_list.append(move)
                elif id_open > -1:
                    copy = input_matrix_list[id_open]
                    if fval < copy.heuristic_fvalue + copy.depth:
                        copy.heuristic_fvalue = heuristic_val
                        copy.parent_node = move.parent_node
                        copy.depth = move.depth
                elif id_close > -1:
                    copy = intermediate_matrix_list[id_close]
                    if fval < copy.heuristic_fvalue + copy.depth:
                        move.heuristic_fvalue = heuristic_val
                        intermediate_matrix_list.remove(copy)
                        input_matrix_list.append(move)

            intermediate_matrix_list.append(x)
            input_matrix_list = sorted(input_matrix_list, key=lambda p:p.heuristic_fvalue + p.depth)
        return [],move_count

    #best-first search algorithm
    def bestFirstSearch(self, heuristicFunction):
        input_matrix_list = [self]
        intermediate_matrix_list = []
        move_count = 0
        while len(input_matrix_list) > 0:
            x = input_matrix_list.pop(0)
            move_count += 1

            if(move_count > maximum_moves):
                print("No Solution, Max Iteration Hit")
                return [], move_count

            if(x.cloned_matrix == goal_state):
                if(len(intermediate_matrix_list) > 0):
                    return x.solutionPath([]), move_count
                else:
                    return[x]
            
            next_possible_position = x.possibleNextOptSolution()
            id_open = id_close = -1
            for move in next_possible_position:
                id_open = index(move.cloned_matrix, input_matrix_list)
                id_close = index(move.cloned_matrix, intermediate_matrix_list)
                heuristic_val = heuristicFunction(move)
                fval = heuristic_val

                if(id_close == -1 and id_open == -1):
                    move.heuristic_fvalue = heuristic_val
                    input_matrix_list.append(move)
                elif(id_open > -1):
                    copy = input_matrix_list[id_open]
                    if(fval < copy.heuristic_fvalue):
                        copy.heuristic_fvalue = heuristic_val
                        copy.parent_node = move.parent_node
                        copy.depth = move.depth
                elif(id_close > -1):
                    copy = intermediate_matrix_list[id_close]
                    if(fval < copy.heuristic_fvalue):
                        move.heuristic_fvalue = heuristic_val
                        intermediate_matrix_list.remove(copy)
                        input_matrix_list.append(move)
            intermediate_matrix_list.append(x)
            input_matrix_list = sorted(input_matrix_list, key=lambda p: p.heuristic_fvalue)
        return [],move_count

#for each heuristics, calculate total
def heuristic(puzzle,item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.getValue(row,col)
            if(val != 0):
                target_col = (val-1) % 3
                target_row = (val-1) / 3

                if target_row < 0:
                    target_row = 2
                t += item_total_calc(row,target_row,col,target_col)
    return total_calc(t)

#manhattan distance heuristic
def manhattan(puzzle):
    return heuristic(puzzle, lambda r,tr, c, tc: abs(tr-r) + abs(tc -c), lambda t : t)

#euclidean distance heuristic
def euclidean(puzzle):
    return heuristic(puzzle,lambda r,tr,c,tc: math.sqrt((tr-r)**2 + (tc-c)**2), lambda t:t)

#misplaced tite heuristics
def misplacedTiles(puzzle):
    count = 0
    for row in range(3):
        for col in range(3):
            if(puzzle.getValue(row,col) != goal_state[row][col]):
                count = count + 1

    return heuristic(puzzle, lambda r,tr,c,tc: count, lambda t:t)