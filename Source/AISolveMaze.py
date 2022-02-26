from AStar import runAStar
from Dfs import runDfs
from AStarBonus import runAStarBonus
from Bfs import runBfs
from visualize import read_file
from Greedy import runGreedy
from readMazeList import readMazeFile

if __name__=="__main__":
    print("###########################")
    print('Maza with no bonus points')
    print('###########################\n')
    mazeList=readMazeFile('Thu muc kiem thu\\Maze no bonus.txt')
    for maze in mazeList:
        print(f'{maze}\n')
        bonus_points, matrix,start,end=read_file(f'Thu muc kiem thu\\{maze}')
        runDfs(start,end,matrix,bonus_points,maze)
        runBfs(start,end,matrix,bonus_points,maze)
        runGreedy(start,end,matrix,bonus_points,maze)
        runAStar(start,end,matrix,bonus_points,maze)

    mazeBonusList=readMazeFile('Thu muc kiem thu\\Maze with bonus.txt')
    print('\n###########################')
    print('Maza with bonus points')
    print('###########################\n')
    for maze in mazeBonusList:
        bonus_points, matrix,start,end=read_file(f'Thu muc kiem thu\\{maze}')
        print(f'{maze}\n')
        runAStarBonus(start,end,matrix,bonus_points,maze)
    
    
    
    

   

