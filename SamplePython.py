from graphics import *
import random
import time

FrameHeight = 600
FrameWidth = 500
RectWidth = 5

############
# UI STUFF #
############

def CreateButton(x, y, text, window):
    button = Text(Point(x, y), text)
    button.setSize(10)
    button.draw(window)

def DrawRect(x1, y1, x2, y2, win, visible):
    if visible: 
        color = color_rgb(74, 137, 220) 
    else: 
        color = color_rgb(255, 255, 255)
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setOutline(color)
    rect.setFill(color)
    rect.draw(win)

def MoveElements(index1, index2, list, window):
    DrawRect(index1 * RectWidth, FrameHeight, index1 * RectWidth + RectWidth, 100, window, False)
    DrawRect(index1 * RectWidth, FrameHeight, index1 * RectWidth + RectWidth, FrameHeight - (RectWidth * list[index1]), window, True)         
    DrawRect(index2 * RectWidth, FrameHeight, index2 * RectWidth + RectWidth, 100, window, False)
    DrawRect(index2 * RectWidth, FrameHeight, index2 * RectWidth + RectWidth, FrameHeight - (RectWidth * list[index2]), window, True)

def GenerateUI(list, window):
    step = 0
    window.delete('all')
    for element in list:
        DrawRect(step, FrameHeight, step + RectWidth, FrameHeight - (RectWidth * element), window, True)
        step += RectWidth
    CreateButton(30, 15, 'Gnome', window)
    CreateButton(90, 15, 'Bubble', window)
    CreateButton(150, 15, 'Shaker', window)
    CreateButton(210, 15, 'EvenOdd', window)
    CreateButton(270, 15, 'Comb', window)
    CreateButton(330, 15, 'Quick', window)

def MeasureTime(function):
    def timed_function(*args, **kwargs):     
        start = time.time()
        Result = function(*args, **kwargs);
        end = time.time()
        CreateButton(51, 40, 'Time: ' + str(end - start)[0:7], window)
        window.getMouse()
        return Result
    return timed_function

##############
# SORT TYPES #
##############

@MeasureTime
def GnomeSort(list, window):
    curptr = 0
    while curptr < len(list) - 1:
        if list[curptr] > list[curptr + 1]: 
            list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
            MoveElements(curptr, curptr + 1, list, window)
            curptr = 0
        else: curptr += 1

@MeasureTime
def BubbleSort(list, window):
    length = len(list) - 1
    while length > 0:
        curptr = 0
        while curptr < length:
            if list[curptr] > list[curptr + 1]: 
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
            curptr += 1
        length -= 1

@MeasureTime
def ShakerSort(list, window):
    curptr = 0
    bleft = 0
    bright = len(list) - 1
    while bright >= bleft:
        while curptr < bright:
            if list[curptr] > list[curptr + 1]: 
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
            curptr += 1
        bright -= 1
        while curptr > bleft:
            if list[curptr - 1] > list[curptr]:
                list[curptr], list[curptr - 1] = list[curptr - 1], list[curptr]
                MoveElements(curptr - 1, curptr, list, window)
            curptr -= 1
        bleft += 1

@MeasureTime
def EvenOddSort(list, window):
    curptr = 0
    finish = 0
    while finish < len(list) - 1:
        while curptr < len(list) - 1:
            if list[curptr] > list[curptr + 1]:
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
                finish = 0
            finish += 1
            curptr += 2
        curptr = abs(curptr % 2 - 1)

@MeasureTime
def CombSort(list, window):
    DECREASE_FACTOR = 1.24
    length = len(list) - 1
    _rightptr = round(length / DECREASE_FACTOR)
    rightptr = _rightptr
    while length > 0:
        leftptr = 0
        rightptr = _rightptr
        while rightptr < len(list):
            if list[leftptr] > list[rightptr]:
                list[leftptr], list[rightptr] = list[rightptr], list[leftptr]
                MoveElements(leftptr, rightptr, list, window)
                time.sleep(0.05)
            rightptr += 1
            leftptr += 1
        if _rightptr > 1: 
            _rightptr = int(_rightptr / DECREASE_FACTOR)
        else:
            length -= 1
        rightptr = _rightptr

@MeasureTime
def QuickSort(list, window):
    def QS(_left, _right):
        left = _left
        right = _right
        pivot = list[round((left + right) / 2)]
        while left <= right:
            while list[left] < pivot:
                left += 1
            while list[right] > pivot:
                right -= 1
            if left <= right:
                list[right], list[left] = list[left], list[right]
                MoveElements(left, right, list, window)
                time.sleep(0.05)
                left += 1
                right -= 1
        if right > _left:
            QS(_left, right)
        if _right > left:
            QS(left, _right)
    QS(0, len(list) - 1)

##################
# IMPLEMENTATION #
##################

window = GraphWin("Сортировки", FrameWidth, FrameHeight)
window.setBackground(color_rgb(255, 255, 255))
list = random.sample(range(100), 100)
_list = list.copy()
GenerateUI(_list, window)

while True:
    try:
        point = window.getMouse()
        x = point.x
        y = point.y
        if y < 30:
            if x < 60   : GnomeSort(_list, window)
            elif x < 120: BubbleSort(_list, window)
            elif x < 180: ShakerSort(_list, window)
            elif x < 240: EvenOddSort(_list, window)
            elif x < 300: CombSort(_list, window)
            elif x < 360: QuickSort(_list, window)
            _list = list.copy()
            GenerateUI(_list, window)
    except:
        break
        