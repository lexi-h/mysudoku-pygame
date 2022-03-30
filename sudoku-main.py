import os, sys, pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def init_board():
    one_row = [0,0,0, 0,0,0, 0,0,0]
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
    image = pygame.transform.scale(image.size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


class Tile(pygame.sprite.Sprite):
    """all the tiles"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # calls parent Sprite initializer
        self.image, self.rect = load_image("blue1.png", -1)


def main():

    pygame.init()

    sudoku_board = init_board()

    #print_board(sudoku_board)

    size = width, height = 900, 900
    black = 0,0,0

    screen = pygame.display.set_mode(size)

    gamelooprunning = True
    while gamelooprunning:
        for event in pygame.event.get():
            print(event)
            #if event.type == pygame.KeyDown: 
            if event.type == pygame.QUIT: gamelooprunning=False

        screen.fill(black)
        pygame.display.flip()

    pygame.quit()




main()