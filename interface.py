
import time
import eightPuzzle
from Tkinter import *
import ttk
import tkFont
import tkMessageBox
class App:

    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.grid()
        self.speedDelay = StringVar(self.frame, value='1000')
        self.numberShuffle = StringVar(self.frame, value='10')

        self.isSolved = False
        self.dificulty = StringVar()
        self.currentMatrix = eightPuzzle.shuffleEightPuzzle('easy', 10)
        self.drawPuzzle()

        R1 = Radiobutton(self.frame, text="Easy", variable=self.dificulty, value='easy'
                 ).grid(column=1, row=1)
        R2 = Radiobutton(self.frame, text="Hard", variable=self.dificulty, value='hard'
                 ).grid(column=2, row=1)

        self.dificulty.set('easy')

        speed = Label(self.frame, text="Speed (ms): ")
        speed.grid(column=1, row=2)
        self.speedDelayButton = Entry(self.frame, width=8, textvariable=self.speedDelay)
        self.speedDelayButton.grid(column=2, row=2)

        L1 = Label(self.frame, text="Shuffles: ")
        L1.grid(column=1, row=3)
        self.numberShuffleButton = Entry(self.frame, width=8, textvariable=self.numberShuffle)
        self.numberShuffleButton.grid(column=2, row=3)
        
        self.button = Button(self.frame, text="QUIT", fg="red", height = 2, width = 8, command=self.frame.quit)
        self.button.grid(column=0,row=2)

        self.button = Button(self.frame, text="About", fg="red", height = 2, width = 8, command=self.About)
        self.button.grid(column=0,row=1)

        self.button = Button(self.frame, text="Repeat", fg="red", height = 2, width = 8, command=self.repeatMove)
        self.button.grid(column=1,row=4)

        self.timeLabel = Label(master, text="Time spending: ", fg="white",bg="blue", height=2)
        self.timeLabel.grid(column=0, row=8)

        self.shuffleButton = Button(self.frame, text="Shuffle", fg="red", height = 2, width = 8, command=self.shuffle)
        self.shuffleButton.grid(column=0,row=3)

        self.solveButton = Button(self.frame, text="Solve", fg="red", height = 2, width = 8, command=self.solve)
        self.solveButton.grid(column=0,row=4)

    def repeatMove(self):
        if self.isSolved:
            self.reDrawPuzzle()
            self.frame.after(1000, lambda: self.changeGrid(self.listMovement, len(self.listMovement) - 1))            
            return
        else:
            self.messageBox('The pattern has not been solved. Please click Solve first.')

    def shuffle(self):
        if not self.numberShuffle.get():
            self.errorMessage('Shuffles')
            return
        
        self.currentMatrix = eightPuzzle.shuffleEightPuzzle(self.dificulty.get(), int(self.numberShuffle.get()))
        matrix = eightPuzzle.convertMatrixIntoList(self.currentMatrix)
        for i in range(0,9,1):      
            if(matrix[i] == 0):
                continue            
            self.listButton[matrix[i]].config(text=matrix[i])
            self.listButton[matrix[i]].grid(column=i%3,row=5+i/3)        

        self.isSolved = False

    def About(self):
        tkMessageBox.showinfo("About", "This product was made by Trieu Trang Vinh.")

    def messageBox(self, message):
        tkMessageBox.showinfo("Message", message)        

    def errorMessage(self, errMessage):
        tkMessageBox.showinfo("Error", "Please input value in the field " + errMessage )

    def reDrawPuzzle(self):   # just changging the grid
        matrix = eightPuzzle.convertMatrixIntoList(self.currentMatrix)
        for i in range(0,9,1):      
            if(matrix[i] == 0):
                continue            
            self.listButton[matrix[i]].grid(column=i%3,row=5+i/3)

    def drawPuzzle(self):
        helv = tkFont.Font(family='Helvetica',size=11, weight='bold')
        self.listButton = [0,1,2,3,4,5,6,7,8]
        matrix = eightPuzzle.convertMatrixIntoList(self.currentMatrix)
        for i in range(0,9,1):      
            if(matrix[i] == 0):
                continue            
            self.listButton[matrix[i]] = Button(self.frame, text=(matrix[i]), font=helv, fg="red", bg="yellow", height = 2, width = 8)
            self.listButton[matrix[i]].grid(column=i%3,row=5+i/3)        

    def changeGrid(self, listMovement, i):  # direction is the direct of whiteCell want to go at, number is the place where whiteCell want to reach to

        if(i < 0):
            return

        number = int(listMovement[i]['number'])
        direction = listMovement[i]['direction']
        info = self.listButton[number].grid_info()

        if direction == 'left':
            columnNew = int(info['column']) + 1
            rowNew = int(info['row'])

        if direction == 'right':
            columnNew = int(info['column']) - 1
            rowNew = int(info['row'])

        if direction == 'up':
            columnNew = int(info['column'])
            rowNew = int(info['row']) + 1

        if direction == 'down':
            columnNew = int(info['column'])
            rowNew = int(info['row']) - 1

        self.listButton[number].grid(column=columnNew, row=rowNew)
        return self.listButton[number].after(int(self.speedDelay.get()), lambda: self.changeGrid(listMovement, i-1))


    def solve(self):
        startTime = time.time()
        self.listMovement = eightPuzzle.mainEightPuzzle(self.currentMatrix)
        endTime = time.time()

        self.isSolved = True
        print 'Time spend ' + str(round(endTime-startTime,4))
        self.timeLabel.config(text='Time spending: ' + str(round(endTime-startTime,4)))
        self.changeGrid(self.listMovement, len(self.listMovement) - 1)

if __name__ == "__main__":
    root = Tk()
    root.wm_title("8 puzzle")
    root.style = ttk.Style()
    root.style.theme_use('winnative')
    root.resizable(True,True)
    app = App(root)
    root.mainloop()


# =================================================================

# from Tkinter import *

# class Application(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.grid()
#         self.master.title("Grid Manager")

#         for r in range(6):
#             self.master.rowconfigure(r, weight=1)    
#         for c in range(5):
#             self.master.columnconfigure(c, weight=1)
#             Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

#         Frame1 = Frame(master, bg="red")
#         Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
#         Frame2 = Frame(master, bg="blue")
#         Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
#         Frame3 = Frame(master, bg="green")
#         Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

# root = Tk()
# app = Application(master=root)
# app.mainloop()

# =================================================================

# import Tkinter

# class simpleapp_tk(Tkinter.Tk):
#     def __init__(self,parent):
#         Tkinter.Tk.__init__(self,parent)
#         self.parent = parent
#         self.initialize()

#     def initialize(self):
#         self.grid()

#         # self.entryVariable = Tkinter.StringVar()
#         # self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
#         # self.entry.grid(column=0,row=0,sticky='EW')
#         # self.entry.bind("<Return>", self.OnPressEnter)
#         # self.entryVariable.set(u"Enter text here.")


#         shuffleButton = Tkinter.Button(self,text=u"Shuffle", height = 2, width = 8,
#                                 command=None)
#         shuffleButton.grid(column=0,row=2)

#         solveButton = Tkinter.Button(self,text=u"Solve", height = 2, width = 8,
#                                 command=None)
#         solveButton.grid(column=0,row=3)

#         guideButton = Tkinter.Button(self,text=u"Guide", height = 2, width = 8,
#                                 command=None)
#         guideButton.grid(column=0,row=4)

#         quitButton = Tkinter.Button(self,text=u"Quit", height = 2, width = 8,
#                                 command=None)
#         quitButton.grid(column=0,row=5)


#         # self.labelVariable = Tkinter.StringVar()
#         # label = Tkinter.Label(self,textvariable=self.labelVariable,
#         #                       anchor="w",fg="white",bg="blue")
#         # label.grid(column=0,row=1,columnspan=2,sticky='EW')
#         # self.labelVariable.set(u"Hello !")

# #        self.grid_columnconfigure(0,weight=1)
# #        self.grid_rowconfigure(1,weight=1)
#         self.grid_rowconfigure(2,weight=0)
#         self.grid_rowconfigure(3,weight=1)
#         self.grid_rowconfigure(4,weight=1)
#         self.grid_rowconfigure(5,weight=1)
# #        self.grid_rowconfigure(6,weight=1)

#         self.resizable(True,True)
#         self.update()
#         self.geometry(self.geometry())       
#         # self.entry.focus_set()
#         # self.entry.selection_range(0, Tkinter.END)

#     def OnButtonClick(self):
#         self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
#         self.entry.focus_set()
#         self.entry.selection_range(0, Tkinter.END)

#     def OnPressEnter(self, event):
#         self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
#         # self.entry.focus_set()
#         # self.entry.selection_range(0, Tkinter.END)

# if __name__ == "__main__":
# #    root = Tkinter.Tk()
# #    root.resizable(width=True, height=True)

#     app = simpleapp_tk(None)
#     app.title('my application')

# #    root.mainloop()
#     app.mainloop()

# =================================================================
