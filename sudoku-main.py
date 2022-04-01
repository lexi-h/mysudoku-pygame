import os, sys, pygame

#color constants
WHITE = (255,255,255)
GREY = (170, 170, 170)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")



def init_board():
    one_row = [1,2,3, 4,5,6, -1,8,9]
    sudoku_board = []
    for _ in range(0,9):
        sudoku_board.append(one_row)

    return sudoku_board


def print_board(sudoku_board):
    for row_iterator in sudoku_board:
        print(row_iterator)

    return

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


class Tile(pygame.sprite.Sprite):
    """all the tiles"""

    def __init__(self, value=-1, boardx=0, boardy=0, isModifiable=True):
        pygame.sprite.Sprite.__init__(self) # calls parent Sprite initializer
        self.value = value
        self.image_name = "empty.png"
        if self.value != -1:
            self.image_name = "blue" + str(self.value) + ".png"
        self.image, self.rect = load_image(self.image_name, -1)
        self.boardx = boardx 
        self.boardy = boardy
        self.isModifiable = isModifiable

        self.background_color = "grey"
        if self.isModifiable:
            self.background_color = "white"

        self.background_image, self.background_rect = load_image(self.background_color + ".png", None)

    def __str__(self):
        return "VALUE=%s, IMAGENAME=%s, bx=%s, by=%s" % (self.value, self.image_name, self.boardx, self.boardy) 

    def draw(self, screen):
        screenx = 3 + self.boardx*65 + int(self.boardx / 3) * 2
        screeny = 3 + self.boardy*65 + int(self.boardy / 3) * 2

        #draw background 
        screen.blit(self.background_image, (screenx, screeny))

        #draw number
        screen.blit(self.image, (screenx, screeny))

    def modify(self, new_value):
        if self.isModifiable:
            if self.value == new_value: #allow toggling by pressing the same number
                new_value = -1

            self.value = new_value

            #load image
            self.image_name = "empty.png"
            if self.value != -1:
                self.image_name = "blue" + str(self.value) + ".png"
            self.image, self.rect = load_image(self.image_name, -1)

class Cursor(pygame.sprite.Sprite):
    """the red box cursor"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call parent constructor
        self.board_pos = [0,0]
        self.image, self.rect = load_image("cursor.png", (0,255,0))

    def draw(self, screen):
        screenx = 3 + self.board_pos[0]*65 + int(self.board_pos[0] / 3) * 2
        screeny = 3 + self.board_pos[1]*65 + int(self.board_pos[1] / 3) * 2
        screen.blit(self.image, (screenx, screeny))
        
    def move(self, x_movement, y_movement):
        self.board_pos[0] += x_movement
        if self.board_pos[0] < 0: self.board_pos[0] = 0
        if self.board_pos[0] > 8: self.board_pos[0] = 8

        self.board_pos[1] += y_movement
        if self.board_pos[1] < 0: self.board_pos[1] = 0
        if self.board_pos[1] > 8: self.board_pos[1] = 8

class Board(pygame.sprite.Sprite):
    """contains all tiles"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sudoku_board = self._init_board() # a 2d array board full of Tile objects
        self.cursor = Cursor()
        self.image, self.rect = load_image("board.png", (255,0,255))

    def _init_board(self):
        assembling_board = []

        temp_board = init_board()
        for j, row in enumerate(temp_board):
            assembling_row = []
            for i, value in enumerate(row):
                assembling_row.append(Tile(value, i, j))

            assembling_board.append(assembling_row)

        return assembling_board


    def print_board(self):
        for row in self.sudoku_board:
            for tile in row:
                print(tile)

    def draw(self, screen):
        screen.blit(self.image, (0,0))
        for row in self.sudoku_board:
            for tile in row:
                tile.draw(screen)

        self.cursor.draw(screen)

    def modify_tile(self, new_value):
        self.sudoku_board[self.cursor.board_pos[1]][self.cursor.board_pos[0]].modify(new_value)

    def move_cursor(self, x_movement, y_movement):
        self.cursor.move(x_movement, y_movement)

def main():

    pygame.init()

    sudoku_board = init_board()

    #print_board(sudoku_board)

    size = width, height = 900, 900
    black = 0,0,0

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("pydoku")


    ############
    #init
    ############

    #num1 = Tile()
    #allsprites = pygame.sprite.RenderPlain((num1))

    board = Board()

    background = pygame.Surface(screen.get_size())

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Sudoku Gaming :)", True, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)

    gamemode = 0
    clock = pygame.time.Clock()

    gamelooprunning = True
    while gamelooprunning:
        clock.tick(60)

        #########
        # GAMEMODES
        # 0 = Initialize Title Screen
        # 1 = Title Screen
        # 2 = Menus
        # 3 = Initialize Sudoku
        # 4 = Sudoku Game
        # 5 = Sudoku Pause?
        #########
        
        # INITIALIZE TITLE SCREEN
        if gamemode == 0:
            # Load Title Screen
            pass

            #goto title screen
            gamemode = 1
            
        # TITLE SCREEN
        if gamemode == 1:
            # make font 
            if pygame.font:
                font = pygame.font.Font(None, 64)
                text = font.render("Sudoku Gaming :)", True, (WHITE))
                textpos = text.get_rect(centerx=background.get_width() / 2, y=10)

            # handle input; ENTER goes to the main menu
            for event in pygame.event.get():
                #print(event)
                #if event.type == pygame.KeyDown: 
                if event.type == pygame.QUIT: 
                    gamelooprunning=False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                    gamelooprunning=False

                # ENTER moves to the main menu
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    gamemode = 4 # goes directly to sudoku for now

            # DRAW
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill(black)

            screen.blit(background, (0,0))

            screen.blit(text, (100,100))

            pygame.display.flip()





        # SUDOKU GAME
        if gamemode == 4:
        #########
        # inputs and event handling
        #########
            for event in pygame.event.get():
                #print(event)
                #if event.type == pygame.KeyDown: 
                if event.type == pygame.QUIT: 
                    gamelooprunning=False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                    gamelooprunning=False

                #this is cursed but idk how to be smart
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_0 or event.key == pygame.K_KP0):
                    board.modify_tile(-1)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_KP1):
                    board.modify_tile(1)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_2 or event.key == pygame.K_KP2):
                    board.modify_tile(2)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_3 or event.key == pygame.K_KP3):
                    board.modify_tile(3)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_4 or event.key == pygame.K_KP4):
                    board.modify_tile(4)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_5 or event.key == pygame.K_KP5):
                    board.modify_tile(5)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_6 or event.key == pygame.K_KP6):
                    board.modify_tile(6)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_7 or event.key == pygame.K_KP7):
                    board.modify_tile(7)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_8 or event.key == pygame.K_KP8):
                    board.modify_tile(8)
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_9 or event.key == pygame.K_KP9):
                    board.modify_tile(9)

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    board.move_cursor(0, 1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    board.move_cursor(0, -1)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    board.move_cursor(1, 0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    board.move_cursor(-1, 0)

            #########
            # draw
            #########
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill(black)

            screen.blit(background, (0,0))

            board.draw(screen)
            pygame.display.flip()

            #board.print_board()

    pygame.quit()




main()