from tkinter import *
from random import randint

global HEIGHT, WIDTH
HEIGHT = 700    
WIDTH = 700
root = Tk()
root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

class Wordle():
    global TRIES, LINES, TILES, GRID_HEIGHT, GRID_WIDTH, TILE_SIZE, TILE_CENTER, DISCOVERED
    TRIES = 0
    LINES = 6 # Number of lines
    TILES = 5 # Number of tiles per lines
    GRID_HEIGHT = 550
    GRID_WIDTH = (GRID_HEIGHT // LINES) * TILES
    TILE_SIZE = GRID_WIDTH // TILES
    TILE_CENTER = TILE_SIZE // 2
    DISCOVERED = False
    
    def __init__(self):
        self.Word = None # Word to guess
        self.Attempt = None # Attempt to guess the right word

        self.init_Title()
        self.init_frames()
        self.init_Grid()
        self.init_Entry()
        self.init_Word()
        
        Button(self.misc_frame, text="Retry", borderwidth=0, font=('Modern', 20), command=self.retry).pack()
# =============================================================================
# Reset the game and the assets
# =============================================================================
    def retry(self):
        global TRIES, DISCOVERED
        self.Word = "tttta"
        self.reset_grid()
        self.init_Word()
        TRIES = 0
        DISCOVERED = False
        
    def reset_grid(self):
        self.Grid.destroy()
        self.init_Grid()
# =============================================================================
# Initialize elements
# =============================================================================
    def init_Title(self):
        self.Title = Label(root, text="WORDLE", font=('MS Gothic',20))
        self.Title.pack(pady=10)

    def init_frames(self):
        self.init_game_frame = Frame(root, height=HEIGHT, width=WIDTH/4*3, bd=1, relief=SOLID)
        self.misc_frame = Frame(root, height=HEIGHT, width=WIDTH/4, bd=1, relief=SOLID)
        self.init_game_frame.pack(side=LEFT, padx=30)
        self.misc_frame.pack(side=RIGHT, padx=30)
        
    # Initialize the grid to 5x6
    def init_Grid(self):
        self.Grid = Canvas(self.init_game_frame, bg="white", height=GRID_HEIGHT, width=GRID_WIDTH)
        for i in range(TILES):
            for j in range(LINES):
                self.Grid.create_rectangle(i*TILE_SIZE, j*TILE_SIZE, (i+1)*TILE_SIZE, (j+1)*TILE_SIZE, fill='blue')
        self.Grid.pack(side=TOP)
     
    # Initialize the entry to realise the guess    
    def init_Entry(self):
        self.Entry = Entry(self.init_game_frame, font=('MS Gothic', 20))
        self.Entry.pack(side=BOTTOM, pady=10)
        self.Entry.bind("<Return>", self.guess)
        
    def init_Word(self):
        b = randint(0,67)
        f = open("words.txt", 'r')
        i = 0
        for line in f:
            if (i == b):
                self.Word = line[0:len(line)-1] # evite de recuperer le '\n'
                print(self.Word)
                # print(self.Word)
                return
            i += 1    
        print("Erreur de lecture du dictionnaire")    
# =============================================================================
# Attempt to guess the right word
# =============================================================================
    def guess(self, event):
        global TRIES, DISCOVERED
        self.Attempt = self.Entry.get()
        if (self.game_is_over() or DISCOVERED): 
            print("The game's already over, please retry")
        elif (self.is_5_letters_word(self.Attempt)):
            self.print_word(self.Attempt)
            TRIES += 1
            if (self.word_is_discover(self.Attempt)):
                print("YOU WON")
            elif (self.game_is_over() and not DISCOVERED): 
                print("YOU LOST")
            print("Tries left :", LINES-TRIES)
        self.clear_Attempt()
         
    def is_5_letters_word(self, word:str):
        if (len(word) != 5):
            print("Only 5 letters words are accepted")
            return False
        return True

    def print_word(self, word:str):
        tile = 1
        for letter in word:
            x1 = (tile-1)*TILE_SIZE
            y1 = (TRIES)*TILE_SIZE
            x2 = (tile)*TILE_SIZE
            y2 = (TRIES+1)*TILE_SIZE
            if (self.is_word_letter(letter)):
                self.Grid.create_rectangle(x1,y1,x2,y2, fill='orange')
                if (self.is_letter_right_pos(letter,tile-1)):
                    self.Grid.create_rectangle(x1,y1,x2,y2, fill='green')
            else:
                self.Grid.create_rectangle(x1,y1,x2,y2, fill='blue')
            self.Grid.create_text(TILE_CENTER*(tile-0.5)*2, (TRIES+0.5)*TILE_CENTER*2, text=letter, fill="white", font=('MS Gothic', int(TILE_SIZE/3)))
            tile += 1
        self.Grid.update()

    def is_word_letter(self, letter:str):
        return letter in self.Word

    def is_letter_right_pos(self, letter:str, pos):
        return letter == self.Word[pos]

    def clear_Attempt(self):
        self.Attempt = None
        self.Entry.delete(0,END)
# =============================================================================
# End of the game
# =============================================================================
    def game_is_over(self):
        return (LINES-TRIES == 0)
    
    def word_is_discover(self, word:str):
        if (self.Word == word):
            self.discover_word()
            return True
        else:
            return False
        
    def discover_word(self):
        global DISCOVERED
        DISCOVERED = True 
        

w = Wordle()
root.iconbitmap("icon.ico")
root.mainloop()