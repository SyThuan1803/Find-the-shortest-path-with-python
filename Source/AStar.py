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
class PriorityQueue(Node):
    def __init__(self):
        self.items=[]
    def empty(self)->bool:
        return (len(self.items)==0)
    def push(self,item:Node):
        self.items.append(item)
        for i in range(len(self.items)-1):
            for j in range(i+1,len(self.items)):
                if (self.items[i].__lt__(self.items[j])):
                    temp=self.items[i]
                    self.items[i]=self.items[j]
                    self.items[j]=temp

    def pop(self)->Node:
        return self.items.pop()
    def updateStatus(self,end,newBonus,oldBonus):
        #Update status
        for i in self.items:
            i.heuristic=euclidBonusHeuristic(i.item,end,newBonus,oldBonus)
        #Update order
        for i in range(len(self.items)-1):
            for j in range(i+1,len(self.items)):
                if (self.items[i].__lt__(self.items[j])):
                    temp=self.items[i]
                    self.items[i]=self.items[j]
                    self.items[j]=temp

    def getItems(self):
        itemList=[]
        for item in self.items:
            itemList.append(item.getItem())
        return itemList
def children(matrix:list,currentPoint:tuple)->list:
    row=currentPoint[0];
    col=currentPoint[1];
    childrenPoints=[]
    # row< matrix row, go down
    if (row<len(matrix)-1 ):
        if(matrix[row+1][col]!='x'):
            temp=(row+1,col)
            childrenPoints.append(temp)
    #row>0,go up
    if(row>0):
        if(matrix[row-1][col]!='x'):
            temp3=(row-1,col)
            childrenPoints.append(temp3)
    
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
    return childrenPoints
def euclidHeuristic(current:tuple,end:tuple)->float:
    return math.sqrt(math.pow(current[0]-end[0],2)+math.pow(current[1]-end[1],2))
def aStarSearch(start :tuple,end:tuple,matrix)->Optional[Node]:
    #Tạo hàng đợi ưu tiên để duyệt theo các nút có f(n) thấp nhất
    openPoints=PriorityQueue()
    openPoints.push(Node(start,None,0.0,euclidHeuristic(start,end)))
    #Lưu lại cacs nút được mở cùng với cost
    closedPoints:dict[tuple,float]={start:0.0}
    while not (openPoints.empty()):
        currentPoint=openPoints.pop()
        if(currentPoint.getItem()==end):#Nếu gặp điểm kết thúc thì return 
            return currentPoint
        for child in children(matrix,currentPoint.getItem()):
            nextCost=currentPoint.pathCost+1
            #Nếu các nút chưa được mở hoặc đã mở rồi nhưng đường đi đến đó chưa tối ưu->có thể đi
            if(child not in closedPoints or closedPoints[child]>nextCost):
                closedPoints[child]=nextCost
                openPoints.push(Node(child,currentPoint,nextCost,euclidHeuristic(child,end)))
    return None
#Tìm đường đi bằng cách từ nút con tìm ra nút cha cho đến hết
def routeSolved(currentPoint :Node):
    route=[]
    while(currentPoint):
        route.append(currentPoint.getItem())
        currentPoint=currentPoint.parents
    route.reverse()
    return route,len(route)
def runAStar(start,end,matrix,bonus_points,maze):
    finishedPoint=aStarSearch(start,end,matrix)
    route,cost=routeSolved(finishedPoint)
    print("A STAR SEARCH ")
    print(f'Cost from start to end: {cost}')
    print("-------------------------------")
    visualize_maze(matrix,bonus_points,start,end,route,"A star search",maze)