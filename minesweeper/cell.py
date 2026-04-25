from graphics import *

almostBlack = color_rgb(33, 33, 33)

class Cell:

    # creates the cell once Cell is called
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    # draws cell, and if the cell is revealed, it will show if it's a mine or how many adjacent mines there are
    def draw(self, win, color):
        x = self.col * self.size
        y = self.row * self.size
        rect = Rectangle(Point(x, y), Point(x + self.size, y + self.size))
        rect.setFill(color)
        rect.draw(win)
        if self.is_revealed:
            if self.is_mine:
                rect.setFill(almostBlack)
                mine = Circle(Point(x + self.size / 2, y + self.size / 2), self.size / 4)
                mine.setFill("black")
                mine.draw(win)
            elif self.adjacent_mines > 0:
                text = Text(Point(x + self.size / 2, y + self.size / 2), str(self.adjacent_mines))
                text.setSize(self.size // 2)
                text.setStyle("bold")
                text.draw(win)
            else: 
                rect.setFill(color)
        elif self.is_flagged:
            flag = Polygon(Point(x + self.size / 4, y + self.size / 4), Point(x + self.size / 4, y + 3 * self.size / 4), Point(x + 3 * self.size / 4, y + self.size / 2))
            flag.setFill("red")
            flag.draw(win)
    
    def reveal(self, win, color):
        self.is_revealed = True
        Cell.draw(self, win, color)