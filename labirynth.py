import pygame
from handler import *


matrixes = read_file('input.txt')
globalMatrixIndex = 0
matrixData = matrixes[globalMatrixIndex][0]
matrix = matrixes[globalMatrixIndex][1]
max_rows, max_cols = biggestDimensions(matrixes)
WIDTH = 100 + max_cols*50
HEIGHT = 400+max_rows*50
path =  0
isPathDrawn = False

def main():
    pygame.init()

    # Set the dimensions of the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Laberinto saltarín")

    # Define buttons
    buttons = [
        {
            'rect': pygame.Rect(WIDTH//2 - 175, HEIGHT - 60, 170, 50),
            'color': (226, 170, 97),
            'normal_color': (226, 170, 97),
            'hover_color': (200, 0, 0),
            'clicked_color': (178, 120, 62),
            'function': prevMatrix,
            'text': "Matriz anterior",
        },
        {
            'rect': pygame.Rect(WIDTH//2 + 5, HEIGHT - 60, 170, 50),
            'color': (226, 170, 97),
            'normal_color': (226, 170, 97),
            'hover_color': (200, 0, 0),
            'clicked_color': (178, 120, 62),
            'function': nextMatrix,
            'text': "Matriz siguiente",
        },
        {
            'rect': pygame.Rect(WIDTH//2 - 175, HEIGHT - 120, 170, 50),
            'color': (85, 143, 220),
            'normal_color': (85, 143, 220),
            'hover_color': (200, 0, 0),
            'clicked_color': (61, 108, 171),
            'function': DFS,
            'text': "DFS",
        },
        {
            'rect': pygame.Rect(WIDTH//2 + 5, HEIGHT - 120, 170, 50),
            'color': (225, 46, 76),
            'normal_color': (225, 46, 76),
            'hover_color': (200, 0, 0),
            'clicked_color': (186, 38, 63),
            'function': UCS,
            'text': "Costo Uniforme",
        },
        # Add more buttons here
    ]
    
    font = pygame.font.Font(None, 30)
    fontNumbers = pygame.font.Font(None, 50)

    # Main game loop
    running = True
    while running:
        screen.fill((0, 0, 0))  # Fill the screen with black
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    # If the mouse position is within the button rectangle
                    if button['rect'].collidepoint(event.pos):
                        button['color'] = button['clicked_color']  # Change button color to clicked_color
                        button['function']()  # Call the button's function
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button['color'] = button['normal_color'] 

        # Draw the buttons
        for button in buttons:
            pygame.draw.rect(screen, button['color'], button['rect'])
            buttonText = font.render(button['text'], True, (0, 0, 0))  # Create text surface
            text_rect = buttonText.get_rect(center=button['rect'].center)  # Get text rectangle and set its center as the center of the button
            screen.blit(buttonText, text_rect)  # Draw the text on the screen at the center of the button

        # Info text
        infoTittle = font.render("Laberinto saltarín por Bruno Arce", True, (255, 255, 255))
        infoMatrixNumber = font.render(f"Matriz {globalMatrixIndex+1} de {len(matrixes)}", True, (255, 255, 255))
        textRectTittle = infoTittle.get_rect(center=(WIDTH // 2, 50))
        textRectNumber = infoMatrixNumber.get_rect(center=(WIDTH//2, 100))
        screen.blit(infoTittle, textRectTittle)
        screen.blit(infoMatrixNumber, textRectNumber)

        # Print the matrix
        cellSize = 50
        windowWidth = WIDTH
        windowHeight = HEIGHT
        matrixWidht = len(matrix[0]) * cellSize
        matrixHeight = len(matrix) * cellSize
        matrixStartX = (windowWidth - matrixWidht) // 2
        matrixStartY = (windowHeight - matrixHeight) // 2 - 50
        
        for i, row in enumerate(matrix):
            for j, elem in enumerate(row):
                matrixNumbers = fontNumbers.render(str(elem), True, (255, 255, 255))  # Create text surface
                cellRect = pygame.Rect(matrixStartX + j * cellSize, matrixStartY + i * cellSize, cellSize, cellSize)
                textRectMatrixNums = matrixNumbers.get_rect(center=cellRect.center)  # Get the rectangle of the text surface and center it in the cell
                screen.blit(matrixNumbers, textRectMatrixNums)  # Draw the text on the screen at the center of the cell
                pygame.draw.rect(screen, (255, 255, 255), cellRect, 1)  # Draw the cell border

        # Highlight the start cell
        startCircleX = matrixStartX + matrixData[3] * cellSize
        startCircleY = matrixStartY + matrixData[2] * cellSize
        startCircle = (startCircleX + cellSize // 2, startCircleY + cellSize // 2)  # The center of the cell
        pygame.draw.circle(screen, (0, 255, 0), startCircle, cellSize // 2 - 5, 2)

        # Highlight the end cell
        endCircleX = matrixStartX + matrixData[5] * cellSize
        endCircleY = matrixStartY + matrixData[4] * cellSize
        endCircle = (endCircleX + cellSize // 2, endCircleY + cellSize // 2)
        pygame.draw.circle(screen, (255, 0, 0), endCircle, cellSize // 2 - 5, 2)

        # Highlight the path
        global isPathDrawn
        if path != (0) and isPathDrawn == False: # HANDLE CASE PATH EQUAL TO NONE
            if path == None:
                noPathFound = font.render("No se encontró un camino", True, (255, 255, 255))
                textRectNoPath = noPathFound.get_rect(center=(WIDTH // 2, HEIGHT - 160))
                screen.blit(noPathFound, textRectNoPath)
            else:
                pathFound = font.render(f"Camino encontrado en {len(path)-1} pasos", True, (255, 255, 255))
                textRectPath = pathFound.get_rect(center=(WIDTH // 2, HEIGHT - 160))
                screen.blit(pathFound, textRectPath)
                for i in range(len(path) - 1):
                    x1 = matrixStartX + path[i][1] * cellSize + cellSize // 2
                    y1 = matrixStartY + path[i][0] * cellSize + cellSize // 2
                    x2 = matrixStartX + path[i + 1][1] * cellSize + cellSize // 2
                    y2 = matrixStartY + path[i + 1][0] * cellSize + cellSize // 2
                    pygame.draw.line(screen, (255, 255, 204), (x1, y1), (x2, y2), 5)

                    endCircle = (x2, y2)
                    pygame.draw.circle(screen, (255 - i*5, 196 - i*3, 0), endCircle, cellSize // 2 - 5, 2)
                    pygame.display.update()
                    pygame.time.delay(1000)
                isPathDrawn = True            
        pygame.display.update()  # Update the display

    pygame.quit()

def nextMatrix():
    global globalMatrixIndex
    global matrixData
    global matrix
    global path

    if globalMatrixIndex < len(matrixes) - 1:
        globalMatrixIndex += 1
        matrixData = matrixes[globalMatrixIndex][0]
        matrix = matrixes[globalMatrixIndex][1]
        path = 0


def prevMatrix():
    global globalMatrixIndex
    global matrixData
    global matrix
    global path

    if globalMatrixIndex > 0:
        globalMatrixIndex -= 1
        matrixData = matrixes[globalMatrixIndex][0]
        matrix = matrixes[globalMatrixIndex][1]
        path = 0

def DFS():
    global matrixData
    global matrix
    global path
    global isPathDrawn

    isPathDrawn = False

    start = (matrixData[2], matrixData[3])
    goal = (matrixData[4], matrixData[5])
    path = depthFirstSearch(matrix, start, goal)

def UCS():
    global matrixData
    global matrix
    global path
    global isPathDrawn

    isPathDrawn = False

    start = (matrixData[2], matrixData[3])
    goal = (matrixData[4], matrixData[5])
    path = uniformCostSearch(matrix, start, goal) 

if __name__ == '__main__':
    main()