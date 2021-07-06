from typing import ItemsView
import Maze
import os
import tkinter as tk
import time
import cv2
import threading

from PIL import Image , ImageTk
from Root import ProgramBase
from tkinter import messagebox

from Mazemap import Map
from Mazectrl import MazeMove
from MazeUI import Mapdraw

MOUSE_THREAD_ID = 0

class MazeThread(threading.Thread) :
    def __init__(self , ID , name , parent) :
        threading.Thread.__init__(self)
        self.threadID = ID
        self.name = name
        self.parent = parent

    def run(self) :
        if self.threadID == MOUSE_THREAD_ID :
            self.parent.funcThread()


class Maze(ProgramBase) :

    def __init__(self , root , width = 640 , height = 480):
        super().__init__(root , width , height)
        self.root.title('老鼠覓食')
        
        self.map = Map()
        self.mazemove = MazeMove(self.map)
        self.canvas = tk.Canvas(self.root , bg = 'black' , width=width , height = height)
        self.mapUI = Mapdraw(self.map , self.mazemove ,self.canvas , width , height)
        self.canvas.pack()

        self.gameFinsihed = False

        self.threadMouse = None
        self.threadEventMouse = threading.Event()
        self.walkSpeed = 0.3

    # override
    def onKey(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == 'Escape':
                self.threadEventMouse.set() # signal the thread loop to quit
                print("key Escape") 
                self.root.destroy()
            else: # any other key
                if not self.threadMouse:
                    self.startThread()

    def startThread(self) :
        self.threadMouse = MazeThread(MOUSE_THREAD_ID , 'Mouse Thread' , self)
        self.threadEventMouse.clear()
        self.threadMouse.start()

    def funcThread(self) :
        while not self.threadEventMouse.wait(self.walkSpeed) :
            self.nextStep()
        self.gameOver()

    def nextStep(self) :
        (state , item) = self.mazemove.moveForward()
        if state :
            #lastRoute = self.mazemove.lastRoute() 
            #check if need to move backward
            while self.mapUI.mousePos != item[1] : 
                lastRoute= self.mazemove.popRoute()
                lastRoute = ( self.changedir( lastRoute[0] ) , lastRoute[2] , lastRoute[1] )
                #print (item[1] , self.mousePos , lastRoute)
                self.mapUI.moveBackward(lastRoute , self.walkSpeed)

            if self.map.isCake(item[2][0],item[2][1]):
                self.threadEventMouse.set() # signal the thread loop to quit
                self.gameFinsihed = True
            else:
                self.mapUI.moveForward(item)

        else :
            messagebox.showerror(title = 'Maze' , message = 'No route to get out of this maze !! ')
            self.threadEventMouse.set()

    def changedir(self , direction) :
        reverseDict = {'east' : 'west' ,
                       'west' : 'east' ,
                       'south' : 'north' ,
                       'north' : 'south'}
        return reverseDict[direction]


    def gameOver(self):
        if self.gameFinsihed:
            messagebox.showinfo(title='Maze', message='Mission Completed')
if __name__ == '__main__' :
    program = Maze(tk.Tk())
    cwd = os.getcwd()
    program.mapUI.loadMaze(os.path.join(cwd , 'data/maze_map01.csv'))
    program.run()
