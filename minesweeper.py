from tkinter import *
import random
import ctypes

#creating Tk instance for the window
win = Tk()
WIN_HEIGHT = 480
WIN_WIDTH = 720
#let offsets of central frame from each side be 15% of window's width/height
FRAME_VERTICAL_OFFSET = int(15/100 * WIN_HEIGHT)
FRAME_HORIZONTAL_OFFSET = int(15/100 * WIN_WIDTH)
FRAME_HEIGHT = WIN_HEIGHT - 2*FRAME_VERTICAL_OFFSET
FRAME_WIDTH = WIN_WIDTH - 2*FRAME_HORIZONTAL_OFFSET



def EndGame(gameWon):
    #display game over or game won message and close window
    if gameWon:
        #display game won message
        ctypes.windll.user32.MessageBoxW(0, "YOU WIN!!! You cleared the board without clicking on any mine", "Game Won", 0) 
        win.destroy()
    else:
        #display game over message
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine", "Game Over", 0) 
        win.destroy()
    

     
class Tile:

    def __init__(self, value, isMine, frame, gridPos_x, gridPos_y):
        self.value = value
        self.isMine = isMine
        self.frame = frame
        self.tileHeight = 1
        self.tileWidth = 5
        self.pos_x = gridPos_x #column position on the grid 
        self.pos_y = gridPos_y #row position on the grid
        self.button = None
        
    def CreateButton(self, board):
        self.button = Button(self.frame, relief = "raised", width = self.tileWidth, height = self.tileHeight, bd = 4, command = lambda: board.RevealTile(self))
        self.button.grid(column = self.pos_x, row = self.pos_y)
        

    def Reveal(self):
        #remove button and replace with number label

        #check if button exists first
        if(self.button != None): 
            self.button.grid_remove()
            self.button = None
        else: #if button doesn't exist, tile has already been revealed
            return 0 #0 tiles revealed

        if(self.value == 0):
            revealTxt = " "
        else:
            revealTxt = str(self.value)

        
        #create a number label for tile
        self.tileBox = Label(self.frame, bg = "white", height = self.tileHeight, width = self.tileWidth, bd = 2, relief = "sunken", text = revealTxt)
        self.tileBox.grid(column = self.pos_x, row = self.pos_y)
        return 1 #1 tile was revealed


    def IsMine(self):
        return self.isMine

    
    
    
class Board:

    def __init__(self):
        self.width = self.height = 10 #no. of tiles in each row and column
        self.nTiles = self.width*self.height
        self.nMines = 20
        self.tiles = [] #two dimensional list which will contain rows and columns of tiles
        self.nOpened = 0 #no. of revealed tiles

    def SetMine(self):       
        mineRow = random.randint(0, self.height - 1)
        mineCol = random.randint(0, self.width - 1)
        if(not self.tiles[mineRow][mineCol].IsMine()): #if there isn't a mine in the tile already
            self.tiles[mineRow][mineCol].isMine = True
            print(mineRow, mineCol)
        else:
            self.SetMine()


    def setup(self):

        #creating frame for minesweeper board
        self.frame = Frame(win, bg = "white", width = FRAME_WIDTH, height = FRAME_HEIGHT)
        self.frame.place(x = FRAME_HORIZONTAL_OFFSET, y = FRAME_VERTICAL_OFFSET)
        
        #adding tiles to tile array
        for y in range(self.height):
            rowTiles = []
            for x in range(self.width):
                tile = Tile(0, False, self.frame, x, y)
                rowTiles.append(tile) #add tile to row of tiles
                #creating buttons for each tile
                tile.CreateButton(self)
            self.tiles.append(rowTiles) #add row of tiles to 2d list
            


        #setting mines at random locations
        for i in range(self.nMines):       
            self.SetMine()

        #assigning values for each tile
        for tileRow in self.tiles:
            for tile in tileRow:
                if (tile.IsMine()):
                    tile.value = 9 #9 simply represents the presence of a mine on the tile
                else:
                    tile.value = self.neighborMineCount(tile, self.tiles)
                    


    def neighborMineCount(self, tile, tiles):

        mineCount = 0

        height = self.height
        width = self.width
        col = tile.pos_x
        row = tile.pos_y

        #determining start and end tiles for neigbouring tiles
        colBegin = max(0, col - 1)
        rowBegin = max(0, row - 1)
        colEnd = min(width - 1, col + 1)
        rowEnd = min(height - 1, row + 1)

        #counting no. of neighbouring mines
        for y in range(rowBegin, rowEnd + 1):
            for x in range(colBegin, colEnd + 1):
                if tiles[y][x].IsMine():
                    mineCount += 1

        return mineCount

    def RevealTile(self, tile):
        if tile.value == 0:
            self.RevealSurrounding(tile)
        elif tile.value == 9:
            EndGame(False)
        else:
            self.nOpened += tile.Reveal()

        if(self.nOpened + self.nMines == self.nTiles):
            EndGame(True)


        
    def RevealSurrounding(self, tile):
        height = self.height
        width = self.width
        col = tile.pos_x
        row = tile.pos_y

        #determining start and end tiles for neighbouring tiles
        colBegin = max(0, col - 1)
        rowBegin = max(0, row - 1)
        colEnd = min(width - 1, col + 1)
        rowEnd = min(height - 1, row + 1)

        #revealing neighbouring tiles
        for y in range(rowBegin, rowEnd + 1):
            for x in range(colBegin, colEnd + 1):
                self.nOpened += self.tiles[y][x].Reveal()



    


###END OF CLASSES###
    
def main():

    #overriding Tk window settings
    win.geometry(str(WIN_WIDTH)+"x"+str(WIN_HEIGHT))
    win.title("Minesweeper")
    win.resizable(False, False)
    win.configure(bg = "black")

    #creating minesweeper board
    minesweeper = Board()
    minesweeper.setup()


    #running the window
    win.mainloop()

#ensuring program runs only when executed as a script and not used as module
if __name__ == "__main__":
    main()
