from visualize import visualize_maze
from typing import Optional
import math
class Node:
    def __init__(self,item:tuple,parents:Optional['Node'],pathCost:float=0.0,heuristic:float=0.0)->None:
        self.item:tuple=item
        self.parents:Optional['Node']= parents
        self.pathCost=pathCost
        self.heuristic=heuristic
    def getItem(self)->tuple:
        return self.item
    def __lt__(self,other):
        return (self.pathCost+self.heuristic)< (other.pathCost+other.heuristic)

class Stack(Node):
    def __init__(self):
        self.items=[]
    def empty(self)->bool:
        return (len(self.items)==0)
    def push(self,item:Node):
        self.items.append(item)
    def pop(self)->Node:
        return self.items.pop()
    def getItems(self):
        itemList=[]
        for item in self.items:
            itemList.append(item.getItem())
        return itemList

def children(matrix:list,currentPoint:tuple)->list:
    row=currentPoint[0];
    col=currentPoint[1];
    childrenPoints=[]
    #col<matrix col ,go right
    if (col<len(matrix[0])-1 ):
        if(matrix[row][col+1]!='x'):
            temp1=(row,col+1)
            childrenPoints.append(temp1)
    #col>0 ,go left
    if(col>0):
        if(matrix[row][col-1]!='x'):
            temp2=(row,col-1)
            childrenPoints.append(temp2)
    #row>0,go up
    if(row>0):
        if(matrix[row-1][col]!='x'):
            temp3=(row-1,col)
            childrenPoints.append(temp3)
    # row< matrix row, go down
    if (row<len(matrix)-1 ):
        if(matrix[row+1][col]!='x'):
            temp=(row+1,col)
            childrenPoints.append(temp)
    return childrenPoints
    
def dfs(start :tuple,end:tuple,matrix)->Optional[Node]:
    openPoints=Stack()
    openPoints.push(Node(start,None))
    closedPoints:set[tuple]={start}
    while not (openPoints.empty()):
        currentPoint=openPoints.pop()
        if(currentPoint.getItem()==end):
            return currentPoint
        for child in children(matrix,currentPoint.getItem()):
            if(child not in closedPoints):
                openPoints.push(Node(child,currentPoint))
                closedPoints.add(child)
    return None

def routeSolved(currentPoint :Node):
    route=[]
    while(currentPoint):
        route.append(currentPoint.getItem())
        currentPoint=currentPoint.parents
    route.reverse()
    return route,len(route)

def runDfs(start,end,matrix,bonus_points,maze):
    finishedPoint=dfs(start,end,matrix)
    route,cost=routeSolved(finishedPoint)
    print("DEPTH FIRST SEARCH")
    print(f'Cost from start to end: {cost}')
    print("-------------------------------")
    visualize_maze(matrix,bonus_points,start,end,route,"Depth first search",maze)