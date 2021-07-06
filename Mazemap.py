import csv

class Map() :
    def __init__(self) :
        self.info = []
        self.rows = 0
        self.columns = 0

    def loadMap(self , filepath) :
        with open(filepath , newline='') as csvfile :
            rows = csv.reader(csvfile) #read the csv file and turn it into a 2d list
            for row in rows :
                print (row)
                self.info.append(row)
            self.rows = len(self.info)
            self.columns = len(self.info[0])
            print('map rows = {0}, columns = {1}'.format(self.rows, self.columns))

    def isBlock(self , x , y) :
        if not self.inRange(x , y) :
            return True
        return self.info[y][x] == '0'
        
    def isCake(self , x , y) :
        if not self.inRange(x , y) :
            return True
        return self.info[y][x] == '3'
        

    def isHome(self , x , y) :
        if not self.inRange(x , y) :
            return True
        return self.info[y][x] == '2'

    def inRange(self , x , y) :
        temp = x in range(0 , self.columns) and y in range(0 , self.rows)
        return temp