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
        #Update heuristic cho những điểm có thể đi, để di chuyển qua tới bonus mới từ bonus cũ
        for i in self.items:
            i.heuristic=manhattanBonusHeuristic(i.item,end,newBonus,oldBonus)
        #Sắp xếp lại theo khoảng cách đến bonus mới
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
    return childrenPoints

#Tính khoảng cách euclid giữa 2 điểm 
def euclidHeuristic(current:tuple,end:tuple)->float:
    return math.sqrt(math.pow(current[0]-end[0],2)+math.pow(current[1]-end[1],2))

#Heuristic la kc đến điểm thưởng mới bằng khoảng cách manhattan nhân với 1.1
def bonusHeuristic(current:tuple,end:tuple,newbonus:tuple,oldbonus:tuple)->float:
    toNewBonus= abs(newbonus[0]-current[0]) + abs(newbonus[1]-current[1])
    toEnd= abs(end[0]-current[0]) + abs(end[1]-current[1])
    if (toEnd <toNewBonus+newbonus[2]):#Neu kc tu diem toi end < kc tu diem toi diem thuong + gia tri diem thuong
        return toEnd #Return kc toi diem End
    result=toNewBonus*1.1
    return result

#Hàm heuristic để chuyển giao khoảng cách từ bonus cũ sang bonus mới
def manhattanBonusHeuristic(current:tuple,end:tuple,newbonus:tuple,oldbonus:tuple)->float:
    toNewBonus= abs(newbonus[0]-current[0]) + abs(newbonus[1]-current[1])
    toOldBonus=abs(oldbonus[0]-current[0]) + abs(oldbonus[1]-current[1])
    toEnd= abs(end[0]-current[0]) + abs(end[1]-current[1])
    if (toEnd <toNewBonus+newbonus[2]):#Neu kc tu diem toi end < kc tu diem toi diem thuong + gia tri diem thuong
        return toEnd #Return kc toi diem End
    result=toNewBonus*1.2+toOldBonus#Nhân 1.2 và cộng thêm khoảng cách tới bonus cũ sẽ giảm giá trị f(n)
    return result

def aStarSearchWithBonusPoints(start :tuple,end:tuple,matrix,bonus)->Optional[Node]:
    tempPoint1=[]
    #Tạo 1 list chứa bonus points
    for point in bonus:
        tempPoint1.append(point)
    # Sort theo khoang cach tu diem hien tai toi diem thuong tang dan
    tempPoint1.sort(key=lambda point: euclidHeuristic(tuple((point[0],point[1])),start)) 
    newBonus=tempPoint1.pop(0) #Lấy bonus gan nhat
    oldBonus=tuple((start[0],start[1],0)) #Chưa có old bonus, đặt là start
    openPoints=PriorityQueue()
    openPoints.push(Node(start,None,0.0,bonusHeuristic(start,end,newBonus,oldBonus)))
    closedPoints:dict[tuple,float]={start:0.0}
    while not (openPoints.empty()):
        currentPoint=openPoints.pop()
        if(currentPoint.item==end):
            return currentPoint
        #Khi đụng tới new bonus hoac vuot qua new bonus mà không ăn bonus sẽ chuyển tới vị trí có bonus mới
        startToBonus=euclidHeuristic(tuple((newBonus[0],newBonus[1])),start)
        startToCurrent=euclidHeuristic(currentPoint.item,start)
        if(currentPoint.item==tuple((newBonus[0],newBonus[1])) or startToBonus <startToCurrent):
            #Sap xep lai list theo khoang cach toi diem thuong
            tempPoint1.sort(key=lambda point: euclidHeuristic(tuple((point[0],point[1])),currentPoint.item)) 
            if len(tempPoint1)>0:
                oldBonus=newBonus 
                newBonus=tempPoint1.pop(0)
                #Cap nhat lai heuric với new bonus va old bonus
                openPoints.updateStatus(end,newBonus,oldBonus)  
            else: #Nêu kh còn bonus,bonus sẽ là end
                oldBonus=newBonus
                newBonus=tuple((end[0],end[1],0))
                openPoints.updateStatus(end,newBonus,oldBonus)

            #Khi ăn được bonus points, sẽ ưu tiên đi theo hướng sau khi ăn bonus points
            #Tạo hàng đợi ưu tiên cho các nút con của bonus
            tempPoints=PriorityQueue()
            for child in children(matrix,currentPoint.getItem()):
                nextCost=currentPoint.pathCost+1
                #if(child not in closedPoints ):
                closedPoints[child]=nextCost
                tempPoints.push(Node(child,currentPoint,nextCost,bonusHeuristic(child,end,newBonus,oldBonus)))
            #Ghép vào openpoints
            for i in tempPoints.items:
                openPoints.items.append(i)
            #openPoints=tempPoints
        #Không thì duyệt bình thường như A*
        else:
            for child in children(matrix,currentPoint.getItem()):
                nextCost=currentPoint.pathCost+1
                if(child not in closedPoints or closedPoints[child]>nextCost):
                    closedPoints[child]=nextCost
                    openPoints.push(Node(child,currentPoint,nextCost,bonusHeuristic(child,end,newBonus,oldBonus)))
    return None

#Tìm đường đi có bonus
def routeSolvedWithBonusPoints(currentPoint :Node,bonusPoints):
    route=[]
    minus=0
    while(currentPoint):
        route.append(currentPoint.getItem())
        #Nếu có bonus trong đường đi -> trừ cost
        for bpoint in bonusPoints:
            if bpoint[0]==currentPoint.getItem()[0] and bpoint[1]==currentPoint.getItem()[1]:
                minus+=bpoint[2]
        currentPoint=currentPoint.parents
    route.reverse()
    cost=len(route)+minus
    return route,cost

def runAStarBonus(start,end,matrix,bonus_points,maze):
    finishedPoint=aStarSearchWithBonusPoints(start,end,matrix,bonus_points)
    route,cost=routeSolvedWithBonusPoints(finishedPoint,bonus_points)
    print("A STAR WITH BONUS POINTS")
    print(f'Cost from start to end: {cost}')
    print("-------------------------------")
    visualize_maze(matrix,bonus_points,start,end,route,"A star with bonus points",maze)