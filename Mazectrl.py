class MazeMove() :
    def __init__(self , maze) :
        self.mouseRoute = []
        self.candidatesStack = []
        self.visited = []
        self.maze = maze
        self.currentItem = None

    def canWalk(self , x , y) :

        return (not self.maze.isBlock(x , y) )and( not (x , y) in self.visited)

    def initstate(self , x , y) :
        self.currentItem = (None , None , (x , y) )
        self.mouseRoute.append(self.currentItem)
        self.addCandidates(x , y)
        self.visited.append((x , y))
        
    def addCandidates(self , x , y) :
        if self.canWalk(x+1 , y) :
            self.candidatesStack.append( ('east' , (x , y) , (x+1 , y) ) )
        if self.canWalk(x , y+1) :
            self.candidatesStack.append( ('south' , (x , y) , (x , y+1) ) )
        if self.canWalk(x-1 , y) :
            self.candidatesStack.append( ('west' , (x , y) , (x-1 , y) ) )
        if self.canWalk(x , y-1) :
            self.candidatesStack.append( ('north' , (x , y) , (x , y-1) ) )

    def lastRoute(self):
        return self.mouseRoute[-1]

    def popRoute(self) :
        return self.mouseRoute.pop()

    def moveForward(self):
        state = True
        item = None
        if len(self.candidatesStack) > 0:
            item = self.candidatesStack.pop()
            self.addCandidates(item[2][0],item[2][1])
            self.visited.append(item[2])
        if len(self.candidatesStack) == 0 :
            print('Map Error, no route to exit')
            state = False
        return (state, item)
