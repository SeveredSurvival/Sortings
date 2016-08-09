from graphics import *
from math import ceil
import random
import time
from pygame import midi

midi.init()
PLAYER = midi.Output(0)
PLAYER.set_instrument(54, 1) # Nice sounds: 46, 54, 72
FRAMEHEIGHT = 600
FRAMEWIDTH = 500
RECTWIDTH = 5

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

def Pling(note):
    note = ceil(note / 2) + 50
    PLAYER.note_on(note, 127, 1)
    time.sleep(0.01)
    PLAYER.note_off(note, 127, 1)

def MoveElements(index1, index2, list, window):
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, 100, window, False)
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index1]), window, True)  
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, 100, window, False)
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index2]), window, True)
    Pling(int(list[index2]))

def MoveElement(index, size, list, window):
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, 100, window, False)
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), window, True)
    Pling(size)

def GenerateUI(list, window):
    step = 0
    window.delete('all')
    for element in list:
        DrawRect(step, FRAMEHEIGHT, step + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * element), window, True)
        step += RECTWIDTH
    CreateButton(30, 15, 'Gnome', window)
    CreateButton(90, 15, 'Bubble', window)
    CreateButton(150, 15, 'Shaker', window)
    CreateButton(210, 15, 'EvenOdd', window)
    CreateButton(270, 15, 'Heap', window)
    CreateButton(330, 15, 'Merge', window)
    CreateButton(390, 15, 'Comb', window)
    CreateButton(450, 15, 'Quick', window)

def MeasureTime(function):
    def timed_function(*args, **kwargs):     
        start = time.time()
        Result = function(*args, **kwargs);
        end = time.time()
        CreateButton(51, 40, 'Time: ' + str(end - start)[0:7], window)
        window.getMouse()
        return Result
    return timed_function

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
                time.sleep(0.01)
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
                time.sleep(0.01)
                left += 1
                right -= 1
        if right > _left:
            QS(_left, right)
        if _right > left:
            QS(left, _right)
    QS(0, len(list) - 1)

@MeasureTime
def MergeSort(list, window):
    def MS(part, ofs):
        result = []
        if len(part) < 2: return part
        mid = ceil(len(part) / 2)
        y = MS(part[:mid], ofs)
        z = MS(part[mid:], mid + ofs)
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                MoveElement(i + j + ofs, z[j], list, window)
                j += 1
            else:
                result.append(y[i])                
                MoveElement(i + j + ofs, y[i], list, window)
                i += 1
        for item in y[i:]:
            result.append(item)
            MoveElement(ofs + len(result) - 1, item, list, window)        
        for item in z[j:]:
            result.append(item)
            MoveElement(ofs + len(result) - 1, item, list, window)
        return result
    MS(list, 0)

@MeasureTime
def HeapSort(list, window):
    def shiftDown(list, i, j):
        while i * 2 + 1 < j:
            if i * 2 + 1 == j - 1 or list[i * 2 + 1] > list[i * 2 + 2]:
                maxChild = i * 2 + 1
            else:
                maxChild = i * 2 + 2
            if list[i] < list[maxChild]:
                list[i], list[maxChild] = list[maxChild], list[i]
                MoveElements(i, maxChild, list, window)
                i = maxChild
            else:
                break
    for i in range(int(len(list) / 2 - 1), -1, -1):
        shiftDown(list, i, len(list))
    for i in range(len(list) - 1, 0, -1):
        list[0], list[i] = list[i], list[0]
        MoveElements(0, i, list, window)
        shiftDown(list, 0, i)

window = GraphWin("Сортировки", FRAMEWIDTH, FRAMEHEIGHT)
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
            if   x < 60 : GnomeSort(_list, window)
            elif x < 120: BubbleSort(_list, window)
            elif x < 180: ShakerSort(_list, window)
            elif x < 240: EvenOddSort(_list, window)
            elif x < 300: HeapSort(_list, window)
            elif x < 360: MergeSort(_list, window)
            elif x < 420: CombSort(_list, window)
            elif x < 480: QuickSort(_list, window)
            _list = list.copy()
            GenerateUI(_list, window)
    except:
        break
