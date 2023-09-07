#Made by LimonAga
import sys
import pygame
import random
from plant import Plant

pygame.init()
info = pygame.display.Info()

#constants
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
FPS = 30

BG_COLOR = 'black'
CELL_SIZE = 4
Row_Count, Col_Count = SCREEN_WIDTH // CELL_SIZE ,SCREEN_HEIGHT // CELL_SIZE
RESET_TIME = 17000 #miliseconds
reset = True

#screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Plants')
clock = pygame.time.Clock()

def new_grid():
    '''Creates an empty grid.'''
    return [[0 for _ in range(Row_Count)] for _ in range(Col_Count)]

def draw_grid(grid):
    '''Draws plants if plants are not already drawn.'''
    for row in range(Row_Count):
        for col in range(Col_Count):
            cell = grid[row][col]
            if cell and not cell.drawn:# Don't draw cell if it's already drawn
                pygame.draw.rect(screen, cell.color, (row * CELL_SIZE, col * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                cell.drawn = True

def get_neighbours(row, col):
    '''Checks for avaible empty cells for given row and col number.'''
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    neighbours = []
    for neighbour in offsets:
    # Look for neighbour coords
        x, y = row + neighbour[0], col + neighbour[1]
        # Skip this cell if it's not on the board
        if not (0 <= x < Row_Count and 0 <= y < Col_Count) or grid[x][y]:
            continue
        neighbours.append((x, y))
    return neighbours

def update_grid(grid):
    '''Every plant spreads to a nearby empty cell with slightly different hue. 
    If a plant has no empty cell nearby ignores it.'''
    grid2 = new_grid()

    for row in range(Row_Count):
        for col in range(Col_Count):
            cell = grid[row][col]
            if cell:
                grid2[row][col] = cell

                if cell.has_empty_neighbours:
                    neighbours = get_neighbours(row, col)
                    if neighbours:
                        #If plant has an empty cells nearby place a plant there
                        x, y = random.choice(neighbours)
                        if not grid[x][y]:
                            grid2[x][y] = cell.clone()
                    else:
                        #If there is no remaing cells around mark cell to skip it next generations
                        cell.has_empty_neighbours = False
    return grid2

def randomize(grid):
    '''Places 1 to 5 plants to random locations.'''
    amount = random.randint(1,5)
    for _ in range(amount):
        x = random.randint(0, Row_Count)
        y = random.randint(0, Col_Count)
        if not grid[x][y]:
            grid[x][y] = Plant()
    return grid

grid = new_grid()
grid = randomize(grid)

reset_timer = pygame.USEREVENT + 1
pygame.time.set_timer(reset_timer, RESET_TIME)
#main loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == reset_timer and reset:
           grid = new_grid()
           screen.fill(BG_COLOR)
           grid = randomize(grid)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #Close the program
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_SPACE:
                #Clear the grid
                grid = new_grid()
                screen.fill(BG_COLOR)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = x // CELL_SIZE,y // CELL_SIZE
            if not grid[row][col]: grid[row][col] = Plant()

    #updating window
    grid = update_grid(grid)
    draw_grid(grid)
    pygame.display.flip()
    clock.tick(FPS)
