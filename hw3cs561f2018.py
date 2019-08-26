# 0:DOWN
# 1:UP
# 2:RIGHT
# 3:LEFT
import copy
import time
import numpy


def PossibleMoves(givenX,givenY,maxX,maxY):
    rList=[[0 for x in range(2)]for y in range(4)]
    if givenX<maxX:
        rList[0]=[1,0]
    if givenX>0:
        rList[1]=[-1,0]
    if givenY<maxY:
        rList[2]=[0,1]
    if givenY>0:
        rList[3]=[0,-1]
    return rList
def CalculateUtilityAndMove(x,y,maxX,maxY,previousUtility,possibleActions):
    max=float('-inf')
    bestMove=[]
    for i in range(4):
        utility = 0
        utility+=rightProbability*previousUtility[x+possibleActions[i][0]][y+possibleActions[i][1]]
        for j in range(4):
            if j==i:
                continue
            utility+=wrongProbability*previousUtility[x+possibleActions[j][0]][y+possibleActions[j][1]]
        if utility==max:
            if bestMove==[-1,0] or possibleActions[i]==[-1,0] or possibleActions[i]==[0,0]:
                bestMove=[-1,0]
            elif bestMove==[1,0] or possibleActions[i]==[1,0]:
                bestMove=[1,0]
            elif bestMove==[0,1] or possibleActions[i]==[0,1]:
                bestMove=[0,1]
            else:
                bestMove=[0,-1]
        elif utility>max:
            max=utility
            bestMove=possibleActions[i]
    return max,bestMove
def turnLeft(move):
    return [-1*move[1],move[0]]
def turnRight(move):
    return [move[1],-1*move[0]]
def Move(move,swerve,count):
    probability=swerve[count]
    if probability<=0.7:
        return move
    else:
        if probability<=0.8:
            return turnLeft(move)
        elif probability<=0.9:
            return turnRight(move)
        else:
            return turnLeft(turnLeft(move))

def Simulate(startPosition,goalPosition,rewardMatrix,moveMatrix,swerve,possibleActions):
    currentPosition=startPosition
    reward=0
    count=0
    while currentPosition!=goalPosition:
        possibleMoves=possibleActions[currentPosition[0]][currentPosition[1]]
        bestMove=moveMatrix[currentPosition[0]][currentPosition[1]]
        move=Move(bestMove,swerve,count)
        if move in possibleMoves:
            currentPosition=[currentPosition[0]+move[0],currentPosition[1]+move[1]]
        reward+=rewardMatrix[currentPosition[0]][currentPosition[1]]
        count+=1
    return reward


gamma=0.9
rightProbability=0.7
wrongProbability=0.1
goalStates=[]
startStates=[]
obstacles=[]
startTime=time.time()
input=open("input.txt",'r')
output=open("output.txt",'w')
gridSize=int(input.readline())
numberOfCars=int(input.readline())
numberOfObstacles=int(input.readline())
dictionaryOfBestMoves={}
givenGrid=[[0 for x in range(gridSize)]for y in range(gridSize)]
for i in range(numberOfObstacles):
    t=input.readline()
    x=t.split(',')
    obstacles.append([int(x[1]),int(x[0])])
for i in range(numberOfCars):
    t=input.readline()
    x=t.split(',')
    startStates.append([int(x[1]),int(x[0])])
for i in range(numberOfCars):
    t=input.readline()
    x=t.split(',')
    goalStates.append([int(x[1]),int(x[0])])
rewardsGrid=[[-1 for x in range(gridSize)] for y in range(gridSize)]
for obstacle in obstacles:
    rewardsGrid[obstacle[0]][obstacle[1]]-=100
possibleMoves=[[PossibleMoves(x,y,gridSize-1,gridSize-1) for y in range(gridSize)] for x in range(gridSize)]
swerve=[[0 for x in range(10000)]for y in range(10)]
for i in range(10):
    numpy.random.seed(i)
    swerve[i]=numpy.random.random_sample(100000)
for car in range(numberOfCars):
    count = 0
    totalMeanRewards=0
    rewardsGrid[goalStates[car][0]][goalStates[car][1]] += 100
    previousUtility = [[rewardsGrid[x][y] for y in range(gridSize)] for x in range(gridSize)]#copy.deepcopy(rewardsGrid)
    currentUtility = [[0 for x in range(gridSize)] for y in range(gridSize)]
    bestMove = [[[0, 0] for x in range(gridSize)] for y in range(gridSize)]
    if startStates[car]==goalStates[car]:
        totalMeanRewards=100
    elif (goalStates[car][0]*gridSize)+goalStates[car][1] in dictionaryOfBestMoves:
        bestMove=dictionaryOfBestMoves[(goalStates[car][0]*gridSize)+goalStates[car][1]]
    else:
        while True:
            for x in range(gridSize):
                for y in range(gridSize):
                    if x==goalStates[car][0] and y==goalStates[car][1]:
                        currentUtility[x][y]=previousUtility[x][y]
                        continue
                    maximum = float('-inf')
                    bestMovePossible = []
                    for i in range(4):
                        utility = 0
                        utility += rightProbability * previousUtility[x + possibleMoves[x][y][i][0]][y + possibleMoves[x][y][i][1]]
                        for j in range(4):
                            if j == i:
                                continue
                            utility += wrongProbability * previousUtility[x + possibleMoves[x][y][j][0]][y + possibleMoves[x][y][j][1]]
                        if utility == maximum:
                            if bestMovePossible == [-1, 0] or possibleMoves[x][y][i] == [-1, 0] or possibleMoves[x][y][i] == [0, 0]:
                                bestMovePossible = [-1, 0]
                            elif bestMovePossible == [1, 0] or possibleMoves[x][y][i] == [1, 0]:
                                bestMovePossible = [1, 0]
                            elif bestMovePossible == [0, 1] or possibleMoves[x][y][i] == [0, 1]:
                                bestMovePossible = [0, 1]
                            else:
                                bestMovePossible = [0, -1]
                        elif utility > maximum:
                            maximum = utility
                            bestMovePossible = possibleMoves[x][y][i]
                    bestMove[x][y]=bestMovePossible
                    currentUtility[x][y]=rewardsGrid[x][y]+(gamma*maximum)
            count+=1
            difference=[[round(abs(currentUtility[x][y]-previousUtility[x][y]),1) for x in range(gridSize)] for y in range(gridSize)]
            if max(max(difference))<=0.00111:
                break
            else:
                #previousUtility=[[currentUtility[x][y] for y in range(gridSize)] for x in range(gridSize)]#copy.deepcopy(currentUtility)
                previousUtility=currentUtility
                del currentUtility
                currentUtility=[[0 for x in range(gridSize)] for y in range(gridSize)]
        dictionaryOfBestMoves[(goalStates[car][0]*gridSize)+goalStates[car][1]]=bestMove
    if totalMeanRewards==0:
        totalRewards=0
        for i in range(10):
            totalRewards+=Simulate(startStates[car],goalStates[car],rewardsGrid,bestMove,swerve[i],possibleMoves)
            print totalRewards
        totalMeanRewards=int(totalRewards/10)
    rewardsGrid[goalStates[car][0]][goalStates[car][1]]-=100
    output.write(str(totalMeanRewards)+"\n")
endTime=time.time()
print totalMeanRewards
print endTime-startTime