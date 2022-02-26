from visualize import visualize_maze
from typing import Optional
import math
#Cài đặt node cho thuật toán greedy, vì thuật toán không có chi phí di chuyển g(n) nên ta chỉ dùng chi phí heuristic (kc ước tính)
class Node:
    def __init__(self,item:tuple,parents:Optional['Node'],heuristic:float=0.0)->None:
        self.item:tuple=item
        self.parents:Optional['Node']= parents
        self.heuristic=heuristic
    def getItem(self)->tuple:
        return self.item
    def __lt__(self,other):
        return self.heuristic < other.heuristic
#Cài đặt stack cho thuật toán, ngoài các hàm cơ bản push, pop,..ta thêm hàm getItems để lấy ra các list của item
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
#Ở thuật toán greedy và cả A*, ta đều sử dụng hàng đợi ưu tiên này
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
    def getItems(self):
        itemList=[]
        for item in self.items:
            itemList.append(item.getItem())
        return itemList
#hàm duyệt mê cung
def children(matrix:list,currentPoint:tuple)->list:
    row=currentPoint[0];
    col=currentPoint[1];
    childrenPoints=[]
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

#Ta sẽ thử dùng cả hai hàm heuristic là khoảng cách manhattan và euclid để so sánh xem heuristic nào là tối ưu hơn
#-> heuristic ảnh hưởng đến chi phí thuật toán

#def manhattanDistance(current:tuple,end:tuple)->float:
#    return abs(current[0]-end[0]) + abs(current[1]-end[1])

def euclidHeuristic(current:tuple,end:tuple)->float:
    return math.sqrt(math.pow(current[0]-end[0],2)+math.pow(current[1]-end[1],2))

#Hàm chứa thuật toán chính greedy
def greedy(start :tuple,end:tuple,matrix)->Optional[Node]:
    openPoints=PriorityQueue()
    openPoints.push(Node(start,None,euclidHeuristic(start,end)))
    #closedPoints:dict[tuple,float]={start:0.0}
    closedPoints:set[tuple]={start}
    while not (openPoints.empty()):
        currentPoint=openPoints.pop()
        if(currentPoint.getItem()==end):
            return currentPoint
        for child in children(matrix,currentPoint.getItem()):
            if(child not in closedPoints):
                openPoints.push(Node(child,currentPoint,euclidHeuristic(child,end)))
                closedPoints.add(child)
    return None
#Hàm định tuyến giải quyết thuật toán
def routeSolved(currentPoint :Node):
    route=[]
    while(currentPoint):
        route.append(currentPoint.getItem())
        currentPoint=currentPoint.parents
    route.reverse()
    return route,len(route)
#Hàm chạy thuật toán, ta xuất ra cả chi phí đường đi cho thuật toán
def runGreedy(start,end,matrix,bonus_points,maze):
    finishedPoint=greedy(start,end,matrix)
    route,cost=routeSolved(finishedPoint)
    print("GREEDY SEARCH ")
    print(f'Cost from start to end: {cost}')
    print("-------------------------------")
    visualize_maze(matrix,bonus_points,start,end,route,"Greedy search",maze)