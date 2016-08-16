from graphics import *
from pygame import midi
import random
import time

FRAMEWIDTH = 500
RECTWIDTH = 10
INSTRUMENT_ID = 54

midi.init()
PLAYER = midi.Output(0)
PLAYER.set_instrument(INSTRUMENT_ID, 1)
CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
FRAMEHEIGHT = FRAMEWIDTH + 100

def CreateButton(x, y, text, window, style = 'normal'):
    button = Text(Point(x, y), text)
    button.setStyle(style)
    button.setSize(10)
    button.draw(window)

def DrawRect(x1, y1, x2, y2, win, color = color_rgb(74,137,220)):
    rect = Rectangle(Point(x1, y1), Point(x2, y2))
    rect.setOutline(color)
    rect.setFill(color)
    rect.draw(win)

def Pling(note):
    if RECTWIDTH == 1: return None
    note = round(note / CANVAS_SIZE * 50) + 50
    PLAYER.note_on(note, 127, 1)
    time.sleep(0.01)
    PLAYER.note_off(note, 127, 1)

def MarkElements(index1, index2, list, window):
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index2]), window, color = color_rgb(255,0,0))
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index1]), window, color = color_rgb(255,0,0))  
    Pling(int(list[index2]))
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index2]), window)
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index1]), window) 

def MarkElement(index, size, list, window):
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), window, color = color_rgb(255,0,0))
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), window)

def MoveElements(index1, index2, list, window):
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, 100, window, color = color_rgb(255,255,255))
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT, index1 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index1]), window)  
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, 100, window, color = color_rgb(255,255,255))
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT, index2 * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * list[index2]), window)
    Pling(int(list[index2]))

def MoveElement(index, size, list, window):
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, 100, window, color = color_rgb(255,255,255))
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT, index * RECTWIDTH + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), window)
    Pling(size)

def GenerateUI(list, window):
    step = 0
    window.delete('all')
    for element in list:
        DrawRect(step, FRAMEHEIGHT, step + RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * element), window)
        step += RECTWIDTH
    CreateButton(30, 15,  'Bubble', window)
    CreateButton(90, 15,  'Selection', window)
    CreateButton(150, 15, 'Insertion', window)
    CreateButton(210, 15, 'Heap', window)
    CreateButton(270, 15, 'Radix', window)
    CreateButton(330, 15, 'Merge', window)
    CreateButton(390, 15, 'Comb', window)
    CreateButton(450, 15, 'Quick', window)
    CreateButton(30, 40, 'Gnome', window)
    CreateButton(90, 40, 'Even-Odd', window)
    CreateButton(150, 40, 'Shaker', window)
    CreateButton(210, 40, 'Counting', window)
    CreateButton(270, 40, 'Bucket', window)
    CreateButton(430, 40, 'Change size', window, style = 'bold')
    
def MeasureTime(function):
    def timed_function(*args, **kwargs):     
        start = time.time()
        Result = function(*args, **kwargs);
        end = time.time()
        CreateButton(51, 65, 'Time: ' + str(end - start)[0:7], window)
        window.getMouse()
        return Result
    return timed_function
    
def Debug(function):
    def debugged_function(*args, **kwargs):
        import traceback
        try:
            Result = function(*args, **kwargs)
        except Exception:
            traceback.print_exc()
        return Result
    return debugged_function

@MeasureTime
def GnomeSort(list, window):
    curptr = 0
    while curptr < len(list) - 1:
        MarkElements(curptr, curptr + 1, list, window)
        if list[curptr] > list[curptr + 1]: 
            list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
            MoveElements(curptr, curptr + 1, list, window)
            curptr = 0
        else: curptr += 1
    return list

@MeasureTime
def BubbleSort(list, window):
    length = len(list) - 1
    while length > 0:
        curptr = 0
        while curptr < length:
            MarkElements(curptr, curptr + 1, list, window)
            if list[curptr] > list[curptr + 1]: 
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
            curptr += 1
        length -= 1
    return list

@MeasureTime
def ShakerSort(list, window):
    curptr = 0
    bleft = 0
    bright = len(list) - 1
    while bright >= bleft:
        while curptr < bright:
            MarkElements(curptr, curptr + 1, list, window)
            if list[curptr] > list[curptr + 1]: 
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
            curptr += 1
        bright -= 1
        while curptr > bleft:
            MarkElements(curptr - 1, curptr, list, window)
            if list[curptr - 1] > list[curptr]:
                list[curptr], list[curptr - 1] = list[curptr - 1], list[curptr]
                MoveElements(curptr - 1, curptr, list, window)
            curptr -= 1
        bleft += 1
    return list

@MeasureTime
def EvenOddSort(list, window):
    curptr = 0
    finish = 0
    while finish < len(list) - 1:
        while curptr < len(list) - 1:
            MarkElements(curptr, curptr + 1, list, window)
            if list[curptr] > list[curptr + 1]:
                list[curptr], list[curptr + 1] = list[curptr + 1], list[curptr]
                MoveElements(curptr, curptr + 1, list, window)
                finish = 0
            finish += 1
            curptr += 2
        curptr = abs(curptr % 2 - 1)
    return list

@MeasureTime
def CombSort(list, window):
    DECREASE_FACTOR = 1.25
    length = len(list) - 1
    _rightptr = round(length / DECREASE_FACTOR)
    rightptr = _rightptr
    while True:
        leftptr = 0
        rightptr = _rightptr
        while rightptr < len(list):
            MarkElements(leftptr, rightptr, list, window)
            if list[leftptr] > list[rightptr]:
                list[leftptr], list[rightptr] = list[rightptr], list[leftptr]
                MoveElements(leftptr, rightptr, list, window)
            rightptr += 1
            leftptr += 1
        if _rightptr > 1: 
            _rightptr = int(_rightptr / DECREASE_FACTOR)
        else:
            break
        rightptr = _rightptr
    return list
 
@MeasureTime
def QuickSort(list, window):
    def QS(_left, _right):
        left = _left
        right = _right
        pivot = list[round((left + right) / 2)]
        while left <= right:
            while list[left] < pivot:
                MarkElements(left, round((left + right) / 2), list, window)
                left += 1
            while list[right] > pivot:
                MarkElements(right, round((left + right) / 2), list, window)
                right -= 1
            if left <= right:
                list[right], list[left] = list[left], list[right]
                MoveElements(left, right, list, window)
                left += 1
                right -= 1
        if right > _left:
            QS(_left, right)
        if _right > left:
            QS(left, _right)
    QS(0, len(list) - 1)
    return list
    
    
def MS(part, ofs):
    result = []
    if len(part) < 2: return part
    mid = round(len(part) / 2)
    y = MS(part[:mid], ofs)
    z = MS(part[mid:], mid + ofs)
    i = 0
    j = 0
    while i < len(y) and j < len(z):
        MarkElement(i + j + ofs, y[i], list, window)
        MarkElement(i + j + ofs, z[j], list, window)
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

@MeasureTime
def MergeSort(list, window): 
    return MS(list, 0)
@Debug
@MeasureTime
def HeapSort(list, window):
    def shiftDown(list, i, j):
        while i * 2 + 1 < j:
            if i * 2 + 1 == j - 1 or list[i * 2 + 1] > list[i * 2 + 2]:
                maxChild = i * 2 + 1
            else:
                maxChild = i * 2 + 2
            MarkElements(i, maxChild, list, window)
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
    return list

@MeasureTime
def InsertionSort(list, window):
    curptr = 1
    while curptr < len(list):
        key = list[curptr]
        prevptr = curptr - 1
        MarkElements(curptr, prevptr, list, window)
        while prevptr >= 0 and list[prevptr] > key:
            list[prevptr + 1] = list[prevptr]
            MoveElement(prevptr, 0, list, window)
            MoveElement(prevptr + 1, list[prevptr], list, window)
            prevptr -= 1
        list[prevptr + 1] = key
        MoveElement(prevptr + 1, key, list, window)
        curptr += 1
    return list
    
@MeasureTime
def RadixSort(list, window):
    RADIX = 10
    maxLength = False
    tmp, placement = -1, 1
    while not maxLength:
        maxLength = True
        buckets = [[] for _ in range(RADIX)]
        for i in list:
            tmp = i / placement
            buckets[int(tmp % RADIX)].append(i)
            if tmp >= 1: maxLength = False
        if maxLength: break
        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                list[a] = i
                MoveElement(a, i, list, window)
                a += 1
        placement *= RADIX
    return list

@MeasureTime
def SelectionSort(list, window):
    curptr = 0
    while curptr < len(list):
        ptr = curptr
        keyindex = curptr
        while ptr < len(list):
            MarkElements(ptr, keyindex, list, window)
            if list[ptr] <= list[keyindex]:
                keyindex = ptr
            ptr += 1
        list[curptr], list[keyindex] = list[keyindex], list[curptr]
        MoveElements(curptr, keyindex, list, window)
        curptr += 1
    return list
      
@MeasureTime
def CountingSort(list, window):
    MAX = CANVAS_SIZE
    count = [0] * (MAX + 1)
    for item in list: 
        count[item] += 1
        MoveElement(item, count[item], list, window)
    i = 0
    for item in range(MAX + 1):
        for c in range(count[item]):
            list[i] = item
            MoveElement(i, list[i], list, window)
            i += 1
    return list
      
@MeasureTime
def BucketSort(array, window):
    minValue = 0
    maxValue = CANVAS_SIZE
    bucketSize = 4
    bucketCount = int((maxValue - minValue) / bucketSize) + 1
    buckets = []
    for i in range(0, bucketCount): buckets.append([])
    for i in range(0, len(array)): 
        index = int((array[i] - minValue) / bucketSize)
        buckets[index].append(array[i])
        MoveElement((index * bucketSize) + len(buckets[index]) - 1, array[i], list, window)      
    array = []
    offset = 0
    for i in range(0, len(buckets)):
        array.append(MS(buckets[i], offset))
        offset += len(buckets[i])
    return array
       
if __name__ == "__main__":       
    window = GraphWin("Sortings @ github.com/Worldbeater", FRAMEWIDTH, FRAMEHEIGHT)
    window.setBackground(color_rgb(255, 255, 255))
    list = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
    _list = list.copy()
    GenerateUI(_list, window)
    while True:
        try:
            point = window.getMouse()
            x = point.x
            y = point.y
            if y < 30:
                if   x < 60 : BubbleSort(_list, window)
                elif x < 120: SelectionSort(_list, window)
                elif x < 180: InsertionSort(_list, window)
                elif x < 240: HeapSort(_list, window)
                elif x < 300: RadixSort(_list, window)
                elif x < 360: MergeSort(_list, window)
                elif x < 420: CombSort(_list, window)
                elif x < 480: QuickSort(_list, window)
                _list = list.copy()
                GenerateUI(_list, window)
            elif y < 55:
                if   x < 60 : GnomeSort(_list, window)
                elif x < 120: EvenOddSort(_list, window)
                elif x < 180: ShakerSort(_list, window)
                elif x < 240: CountingSort(_list, window)
                elif x < 300: BucketSort(_list, window)
                else:
                    if RECTWIDTH < 20:
                        RECTWIDTH = RECTWIDTH + 10
                    else: 
                        RECTWIDTH = 1
                    CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
                    list = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
                _list = list.copy()
                GenerateUI(_list, window)
        except:
            break