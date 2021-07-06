import os
import cv2
from PIL import Image , ImageTk 
import time

class Mapdraw() :
    def __init__(self , map , mazemove ,canvas , width , height) :
        self.width = width
        self.height = height
        self.sizeX = 0
        self.sizeY = 0
        self.MouseHeight = 0
        self.MouseWidth = 0
        self.mousePos = (0 , 0)

        self.Block = None
        self.Cake = None
        self.Home = None
        self.Mouse = {}

        self.map = map
        self.mazemove = mazemove
        self.canvas = canvas

        self.isHomeDrawn = False
        self.mouseImgID = None
        self.mouseDirection = 'south'

    def loadMaze(self , path) :
        self.map.loadMap(path)
        self.sizeX = (self.width // self.map.columns) 
        self.sizeY = (self.height // self.map.rows)
        print('sizeX is {0} , and sizeY is {1}'.format(self.sizeX , self.sizeY) )
        self.drawMap()
    
    def drawMap(self) :
        self.loadImages()
        for x in range(self.map.columns) :
            for y in range(self.map.rows) :
                if self.map.isBlock(x , y) :
                    self.drawBlock(x , y)
                elif self.map.isCake(x , y) :
                    self.drawCake(x , y)
                elif self.map.isHome(x , y) :
                    self.drawMouse(x , y)
                #else :
                    #self.drawDot(x , y , 2 , 'yellow')
    
    def loadImages(self) :
        cwd = os.getcwd()
        self.Block = self.createImage(os.path.join(cwd , 'data/block.png'))
        self.Cake = self.createImage(os.path.join(cwd , 'data/cake.png') , 16 , 16)
        self.Home = self.createImage(os.path.join(cwd , 'data/home.png') , 16 , 16)
        self.createMousesImage(os.path.join(cwd , 'data/mouse.png') , 10 , 10)

    def createImage(self , path , offsetx = 0 , offsety = 0) :
        img = self.imgcv2Resize(path , offsetx , offsety)
        tkimg = self.saveAsTkimg(img)
        return tkimg

    def createMousesImage(self , path , offsetx = 0 , offsety = 0) :
        imgCV2 = self.imgcv2Resize(path , offsetx , offsety)
        self.MouseHeight , self.MouseWidth = imgCV2.shape[:2]
        print('MouseWidth is {0} , and MouseHeight is {1}'.format(self.MouseWidth , self.MouseHeight))
        self.Mouse['south'] = self.rotateImage(imgCV2 , 0)
        self.Mouse['east'] = self.rotateImage(imgCV2 , 90)
        self.Mouse['north'] = self.rotateImage(imgCV2 , 180)
        self.Mouse['west'] = self.rotateImage(imgCV2 , 270)

    def rotateImage(self , img , angle , scale=1.0) :
        matrixM = cv2.getRotationMatrix2D( (self.MouseWidth/2 , self.MouseHeight/2) , angle , scale )
        imgRotate = cv2.warpAffine(img , matrixM , (self.MouseWidth, self.MouseHeight) )
        return self.saveAsTkimg(imgRotate)

    def imgcv2Resize(self , path , offsetx = 0 , offsety = 0) :
        imgCV2 = cv2.imread(path)
        imgBGR = cv2.resize(imgCV2 , ( (self.sizeX-offsetx) , (self.sizeY-offsety) ) , interpolation=cv2.INTER_AREA )
        imgRGB = imgBGR[...,::-1] #BGR to RGB
        return imgRGB

    def saveAsTkimg(self  , imgcv2) :
        imgPIL = Image.fromarray(imgcv2)
        return ImageTk.PhotoImage(imgPIL)

    def drawBlock (self , x , y) :
        self.drawImage(self.Block , x , y)

    def drawCake (self , x , y ) :
        self.drawImage(self.Cake , x , y , 8 , 8)

    def drawHome (self , x , y) :
        # only draw once after first moving
        if not self.isHomeDrawn :
            self.drawImage(self.Home , x , y , 8 , 8)
            self.isHomeDrawn = True

    def drawMouse (self , x , y ) :
        self.mouseImgID = self.drawImage(self.Mouse['south'], x , y , 5 , 5 )
        self.mazemove.initstate(x , y)
        self.mousePos = (x , y)

    def drawImage(self , img , x , y , offsetx = 0 , offsety = 0 ):
        id = self.canvas.create_image(x*self.sizeX + offsetx , y*self.sizeY + offsety, anchor = 'nw' , image = img)
        return id

    def drawDot (self , x , y , radius , color) :
        (centx , centy) = ( (x + 0.5) * self.sizeX , (y + 0.5) * self.sizeY )
        coord_rect = ( centx-radius , centy-radius , centx+radius , centy+radius )
        self.canvas.create_oval(coord_rect , fill = color)

    def moveForward(self , item) :
        self.updateUI(item)
        self.mazemove.mouseRoute.append(item)
        self.mazemove.currentItem = item
     
    def moveBackward(self , item , interval) :
        self.updateUI(item)
        time.sleep(interval)
        
    def updateUI(self , item) :
        print (item)
        if not self.isHomeDrawn :
            self.drawHome(self.mousePos[0] , self.mousePos[1])
        self.mousePos = item[2]
        self.checkDirection(item[0])
        self.updateMousePos()    # step forward from child info

    def updateMousePos(self) :
        moveMouseDict = {'east' : (self.sizeX , 0) ,
                       'west' : (self.sizeX * (-1) , 0) ,
                       'south' : (0 , self.sizeY) ,
                       'north' : (0 , self.sizeY * (-1))}
        (offsetx , offsety) = moveMouseDict[self.mouseDirection]
        #print (offsetx , offsety)
        self.canvas.move(self.mouseImgID, offsetx, offsety)

    def checkDirection(self , direction) :
        if self.mouseDirection != direction: 
            self.mouseDirection = direction
            self.canvas.itemconfig(self.mouseImgID, image=self.Mouse[self.mouseDirection])
            #print (self.mouseDirection)
