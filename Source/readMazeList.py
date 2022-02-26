def readMazeFile(filename):
    mazeList=[]
    with open(filename,'r') as f:
        for line in f:
            mazeList.append(line.rstrip('\n'))
    return mazeList
