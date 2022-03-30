import os, sys, pygame

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

    def __init__(self, value=-1, boardx=0, boardy=0):
        pygame.sprite.Sprite.__init__(self) # calls parent Sprite initializer
        self.value = value
        self.image_name = "empty.png"
        if value != -1:
            self.image_name = "blue" + str(value) + ".png"
        self.image, self.rect = load_image(self.image_name, -1)
        self.boardx = boardx 
        self.boardy = boardy
        self.screenx = boardx*64
        self.screeny = boardy*64

    def __str__(self):
        return "VALUE=%s, IMAGENAME=%s, bx=%s, by=%s" % (self.value, self.image_name, self.boardx, self.boardy) 

    def draw(self, screen):
        screen.blit(self.image, (self.screenx, self.screeny))


class Board(pygame.sprite.Sprite):
    """contains all tiles"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sudoku_board = self._init_board() # a 2d array board full of Tile objects

    def _init_board(self):
        assembling_board = []

        temp_board = init_board()
        row_counter = 0
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
        for row in self.sudoku_board:
            for tile in row:
                tile.draw(screen)

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

    clock = pygame.time.Clock()

    gamelooprunning = True
    while gamelooprunning:
        clock.tick(60)
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

        #########
        # draw
        #########
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(black)
        #screen.fill(black)

        background.blit(text, textpos)

        #allsprites.update()

        screen.blit(background, (0,0))

        board.draw(screen)
        #allsprites.draw(screen)
        pygame.display.flip()

        board.print_board()

    pygame.quit()




main()