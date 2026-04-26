from board import *
from graphics import *

# Window dimensions
WINDOW_SIZE = 600

# Difficulty presets: (rows, cols, numMines)
DIFFICULTIES = {
    "easy":   (8,  8,  10),
    "medium": (16, 16, 40),
    "hard":   (16, 30, 99)
}

class Game:

    # Creates the game with all its specs once Game is called.
    def __init__(self, difficulty="easy"):
        self.rows, self.cols, self.numMines = DIFFICULTIES[difficulty]
        self.cellSize = WINDOW_SIZE // max(self.rows, self.cols)
        self.winWidth  = self.cols * self.cellSize
        self.winHeight = self.rows * self.cellSize + 60  # extra space for HUD
        self.isFirstClick = True
        self.isOver = False
        self.flagCount = 0

        # Creates the window
        self.win = GraphWin("Minesweeper", self.winWidth, self.winHeight)
        self.win.setBackground(color_rgb(50, 50, 50))

        # Creates the board
        self.board = Board(self.rows, self.cols, self.cellSize, self.numMines, self.win)

        # Draws the HUD (mine counter, flag button, quit button)
        self.hudItems = []
        self._drawHUD()

    # ------------------------------------------------------------------ #
    #  HUD                                                                 #
    # ------------------------------------------------------------------ #

    # Draws the HUD at the bottom of the window.
    def _drawHUD(self):

        # Undraws all previously drawn HUD items.
        for obj in self.hudItems:
            obj.undraw()
        self.hudItems = []

        hudY = self.rows * self.cellSize  # top of HUD strip

        # HUD background
        bg = Rectangle(Point(0, hudY), Point(self.winWidth, self.winHeight))
        bg.setFill(color_rgb(30, 30, 30))
        bg.setOutline(color_rgb(30, 30, 30))
        bg.draw(self.win)
        self.hudItems.append(bg)

        # Mine counter (remaining mines = numMines - flags placed)
        remaining = self.numMines - self.flagCount
        mineText = Text(Point(60, hudY + 30), "Mines: " + str(remaining))
        mineText.setTextColor("white")
        mineText.setSize(14)
        mineText.setStyle("bold")
        mineText.draw(self.win)
        self.hudItems.append(mineText)

        # Flag button
        flagBox = Rectangle(Point(self.winWidth // 2 - 40, hudY + 10),
                            Point(self.winWidth // 2 + 40, hudY + 50))
        flagBox.setFill(color_rgb(80, 80, 80))
        flagBox.draw(self.win)
        self.hudItems.append(flagBox)

        flagLabel = Text(Point(self.winWidth // 2, hudY + 30), "Flag Mode")
        flagLabel.setTextColor("white")
        flagLabel.setSize(12)
        flagLabel.draw(self.win)
        self.hudItems.append(flagLabel)

        # Quit button
        quitBox = Rectangle(Point(self.winWidth - 90, hudY + 10),
                            Point(self.winWidth - 10, hudY + 50))
        quitBox.setFill(color_rgb(180, 50, 50))
        quitBox.draw(self.win)
        self.hudItems.append(quitBox)

        quitLabel = Text(Point(self.winWidth - 50, hudY + 30), "Quit")
        quitLabel.setTextColor("white")
        quitLabel.setSize(12)
        quitLabel.setStyle("bold")
        quitLabel.draw(self.win)
        self.hudItems.append(quitLabel)

        # Store button bounds for click detection
        self.flagBoxBounds = (self.winWidth // 2 - 40, hudY + 10,
                              self.winWidth // 2 + 40, hudY + 50)
        self.quitBoxBounds = (self.winWidth - 90, hudY + 10,
                              self.winWidth - 10,  hudY + 50)

    # Checks if a click point is within a bounding box (x1, y1, x2, y2).
    def _inBounds(self, point, bounds):
        x, y = point.getX(), point.getY()
        x1, y1, x2, y2 = bounds
        return x1 <= x <= x2 and y1 <= y <= y2

    # ------------------------------------------------------------------ #
    #  End screens                                                         #
    # ------------------------------------------------------------------ #

    # Draws a message in the centre of the board.
    def _drawEndScreen(self, message, color):
        overlay = Rectangle(Point(0, 0), Point(self.winWidth, self.rows * self.cellSize))
        overlay.setFill(color)
        overlay.setOutline(color)
        overlay.draw(self.win)

        text = Text(Point(self.winWidth / 2, self.rows * self.cellSize / 2), message)
        text.setSize(24)
        text.setStyle("bold")
        text.setTextColor("white")
        text.draw(self.win)

        subText = Text(Point(self.winWidth / 2, self.rows * self.cellSize / 2 + 40), "Click anywhere to quit.")
        subText.setSize(12)
        subText.setTextColor("white")
        subText.draw(self.win)

    # ------------------------------------------------------------------ #
    #  Game loop                                                           #
    # ------------------------------------------------------------------ #

    # Starts the game loop.
    def start(self):
        flagMode = False

        while not self.isOver:

            # Waits for a click.
            click = self.win.getMouse()

            # Checks if the quit button was clicked.
            if self._inBounds(click, self.quitBoxBounds):
                self.isOver = True
                break

            # Checks if the flag button was clicked.
            if self._inBounds(click, self.flagBoxBounds):
                flagMode = not flagMode
                continue

            # Gets the clicked cell.
            cell = self.board.getClickedCell(click)

            # Ignores clicks outside the board.
            if cell is None:
                continue

            # First click: place mines then reveal.
            if self.isFirstClick:
                self.board.initialReveal(cell)
                self.isFirstClick = False

            # Flag mode: toggle flag on the cell.
            elif flagMode:
                self.board.flag(cell)
                self.flagCount += 1 if cell.isFlagged else -1
                self._drawHUD()

            # Reveal mode: reveal the cell.
            else:
                hitMine = self.board.reveal(cell)

                # Game over: hit a mine.
                if hitMine:
                    self.board.revealAllMines()
                    self._drawEndScreen("You lose!", color_rgb(180, 50, 50))
                    self.win.getMouse()
                    self.isOver = True
                    break

                # Win: all safe cells revealed.
                if self.board.isSolved():
                    self._drawEndScreen("You win!", color_rgb(50, 150, 50))
                    self.win.getMouse()
                    self.isOver = True
                    break

        self.win.close()
