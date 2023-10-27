from prog1 import *

#print results for bfs and astar for all 3 heuristic
def solution(p1,p2,p3,p4,p5):
    sum = 0
    list = [p1,p2,p3,p4,p5]
    h = 0
    k = 0

    while(h != 2):
        if(h == 0 and k == 0):
                print("BFS with Manhattan distance")
        if(h == 0 and k == 1):
                print("BFS with Euclidean distance")
        if(h == 0 and k == 2):
                print("BFS with Misplaced tiles")
        if(h == 1 and k == 0):
                print("A* Manhattan distance")
        if(h == 1 and k == 1):
                print("A* with Euclidean distance")
        if(h == 1 and k == 2):
                print("A* with Misplaced tiles")

        for j in list:
            print("Initial State: ",j.initial_matrix)

            if(h == 0 and k == 0):
                    path, count = j.bestFirstSearch(manhattan)
            if(h == 0 and k == 1):
                    path, count = j.bestFirstSearch(euclidean)
            if(h == 0 and k == 2):
                    path, count = j.bestFirstSearch(misplacedTiles)
            if(h == 1 and k == 0):
                    path, count = j.aSearch(manhattan)
            if(h == 1 and k == 1):
                    path, count = j.aSearch(euclidean)
            if(h == 1 and k == 2):
                    path, count = j.aSearch(misplacedTiles)

            if(path != []):
                path.reverse()
                for i in path:
                    print(i.cloned_matrix)
                    final_output[h][k] = final_output[h][k] + len(path)
                print("Steps:", len(path) ,"States:", count)
                sum += len(path) 
            else:
                print("Search Stopped after", count-1, "states")
        print("Average Steps:",sum/5)
        sum =0

        if(k != 2):
            k += 1
        else:
            h += 1
            k = 0

def main():
    p1 = Puzzle()
    p2 = Puzzle()
    p3 = Puzzle()
    p4 = Puzzle()
    p5 = Puzzle()
    p1.initMatrix('510342786')
    p2.initMatrix('245061873')
    p4.initMatrix('123045678')
    p3.initMatrix('123405678')
    p5.initMatrix('012345678')

    solution(p1,p2,p3,p4,p5)

if __name__ == "__main__":
    main() 