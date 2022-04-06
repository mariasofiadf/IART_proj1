from dataCenter import Solution
from graphics import *
import time

def display(solution: Solution):
    win = GraphWin()
    pt = Point(100, 50)

    cir = Circle(pt, 25)

    cir.draw(win)
    time.sleep(5000)