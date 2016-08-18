from pygame import midi
import random
import pygame
import time
import sys

FRAMEWIDTH = 500
RECTWIDTH = 10
INSTRUMENT_ID = 54 # 54

pygame.init()
midi.init()
PLAYER = midi.Output(0)
PLAYER.set_instrument(INSTRUMENT_ID, 1)
CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
FRAMEHEIGHT = FRAMEWIDTH + 100

def DrawRect(x1, y1, x2, y2, win, color = (90,0,140)):
    pygame.draw.rect(win, color, (x1, y1, x2, y2), 0)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()

def Wait():
    if RECTWIDTH == 20:
        pygame.time.wait(100)
    else:
        pygame.time.wait(10)

def Pling(note):
    if RECTWIDTH == 1: return
    note = round(note / CANVAS_SIZE * 50) + 50
    PLAYER.note_on(note, 127, 1)
    Wait()
    PLAYER.note_off(note, 127, 1)

def MarkElements(index1, index2, seq, window):
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window, color = (255,0,0))  
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window, color = (255,0,0))
    Pling(seq[index2])
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window) 
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window)

def MarkElement(index1, size, window):
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window, color = (255,0,0))  
    Pling(size)
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window) 

def MoveElements(index1, index2, seq, window):
    DrawRect(index1 * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color = (255,255,255))
    DrawRect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window)  
    DrawRect(index2 * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color = (255,255,255))
    DrawRect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window)
    Pling(seq[index2])

def MoveElement(index, size, window):
    DrawRect(index * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color = (255,255,255))
    DrawRect(index * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window)
    Pling(size)

def CreateButton(x, y, text, window, setbold = False):
    font = pygame.font.SysFont("Segoe UI", 13)
    font.set_bold(setbold)
    label = font.render(text, 1, (0,0,0))
    window.blit(label, (x, y - 10))

def GenerateUI(seq, window):
    window.fill((255,255,255))
    step = 0
    for element in seq:
        DrawRect(step, FRAMEHEIGHT - (RECTWIDTH * element), RECTWIDTH, RECTWIDTH * element, window)
        step += RECTWIDTH
    CreateButton(10, 15,  'Bubble', window)
    CreateButton(70, 15,  'Selection', window)
    CreateButton(130, 15, 'Insertion', window)
    CreateButton(190, 15, 'Heap', window)
    CreateButton(250, 15, 'Radix', window)
    CreateButton(310, 15, 'Merge', window)
    CreateButton(370, 15, 'Comb', window)
    CreateButton(430, 15, 'Quick', window)
    CreateButton(10, 40, 'Gnome', window)
    CreateButton(70, 40, 'EvenOdd', window)
    CreateButton(130, 40, 'Shaker', window)
    CreateButton(190, 40, 'Counting', window)
    CreateButton(250, 40, 'Bucket', window)
    CreateButton(430, 40, 'Resize', window, setbold = True)
    pygame.display.update()
    
def MeasureTime(function):
    def timed_function(*args, **kwargs):     
        start = time.time()
        Result = function(*args, **kwargs);
        end = time.time()
        CreateButton(10, 65, 'Time: ' + str(end - start)[0:7], window)
        pygame.display.flip()
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
def GnomeSort(seq, window):
    curptr = 0
    while curptr < len(seq) - 1:
        MarkElements(curptr, curptr + 1, seq, window)
        if seq[curptr] > seq[curptr + 1]: 
            seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
            MoveElements(curptr, curptr + 1, seq, window)
            curptr = 0
        else: curptr += 1
    return seq

@MeasureTime
def BubbleSort(seq, window):
    length = len(seq) - 1
    while length > 0:
        curptr = 0
        while curptr < length:
            MarkElements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]: 
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                MoveElements(curptr, curptr + 1, seq, window)
            curptr += 1
        length -= 1
    return seq

@MeasureTime
def ShakerSort(seq, window):
    curptr = 0
    bleft = 0
    bright = len(seq) - 1
    while bright >= bleft:
        while curptr < bright:
            MarkElements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]: 
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                MoveElements(curptr, curptr + 1, seq, window)
            curptr += 1
        bright -= 1
        while curptr > bleft:
            MarkElements(curptr - 1, curptr, seq, window)
            if seq[curptr - 1] > seq[curptr]:
                seq[curptr], seq[curptr - 1] = seq[curptr - 1], seq[curptr]
                MoveElements(curptr - 1, curptr, seq, window)
            curptr -= 1
        bleft += 1
    return seq

@MeasureTime
def EvenOddSort(seq, window):
    curptr = 0
    finish = 0
    while finish < len(seq) - 1:
        while curptr < len(seq) - 1:
            MarkElements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]:
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                MoveElements(curptr, curptr + 1, seq, window)
                finish = 0
            finish += 1
            curptr += 2
        curptr = abs(curptr % 2 - 1)
    return seq

@MeasureTime
def CombSort(seq, window):
    DECREASE_FACTOR = 1.25
    length = len(seq) - 1
    _rightptr = round(length / DECREASE_FACTOR)
    rightptr = _rightptr
    while True:
        leftptr = 0
        rightptr = _rightptr
        while rightptr < len(seq):
            MarkElements(leftptr, rightptr, seq, window)
            if seq[leftptr] > seq[rightptr]:
                seq[leftptr], seq[rightptr] = seq[rightptr], seq[leftptr]
                MoveElements(leftptr, rightptr, seq, window)
            rightptr += 1
            leftptr += 1
        if _rightptr > 1: 
            _rightptr = int(_rightptr / DECREASE_FACTOR)
        else:
            break
        rightptr = _rightptr
    return seq
 
@MeasureTime
def QuickSort(seq, window):
    def QS(_left, _right):
        left = _left
        right = _right
        pivot = seq[round((left + right) / 2)]
        while left <= right:
            while seq[left] < pivot:
                MarkElements(left, round((left + right) / 2), seq, window)
                left += 1
            while seq[right] > pivot:
                MarkElements(right, round((left + right) / 2), seq, window)
                right -= 1
            if left <= right:
                seq[right], seq[left] = seq[left], seq[right]
                MoveElements(left, right, seq, window)
                left += 1
                right -= 1
        if right > _left:
            QS(_left, right)
        if _right > left:
            QS(left, _right)
    QS(0, len(seq) - 1)
    return seq
    
    
def MS(part, ofs):
    result = []
    if len(part) < 2: return part
    mid = round(len(part) / 2)
    y = MS(part[:mid], ofs)
    z = MS(part[mid:], mid + ofs)
    i = 0
    j = 0
    while i < len(y) and j < len(z):
        MarkElement(ofs + i + j, y[i], window)
        if y[i] > z[j]:
            result.append(z[j])
            MoveElement(i + j + ofs, z[j], window)
            j += 1
        else:
            result.append(y[i])                
            MoveElement(i + j + ofs, y[i], window)
            i += 1
    for item in y[i:]:
        result.append(item)
        MoveElement(ofs + len(result) - 1, item, window)        
    for item in z[j:]:
        result.append(item)
        MoveElement(ofs + len(result) - 1, item, window)
    return result

@MeasureTime
def MergeSort(seq, window): 
    return MS(seq, 0)

@MeasureTime
def HeapSort(seq, window):
    def shiftDown(seq, i, j):
        while i * 2 + 1 < j:
            if i * 2 + 1 == j - 1 or seq[i * 2 + 1] > seq[i * 2 + 2]:
                maxChild = i * 2 + 1
            else:
                maxChild = i * 2 + 2
            MarkElements(i, maxChild, seq, window)
            if seq[i] < seq[maxChild]:
                seq[i], seq[maxChild] = seq[maxChild], seq[i]
                MoveElements(i, maxChild, seq, window)
                i = maxChild
            else:
                break
    for i in range(int(len(seq) / 2 - 1), -1, -1):
        shiftDown(seq, i, len(seq))
    for i in range(len(seq) - 1, 0, -1):
        seq[0], seq[i] = seq[i], seq[0]
        MoveElements(0, i, seq, window)
        shiftDown(seq, 0, i)
    return seq

@MeasureTime
def InsertionSort(seq, window):
    curptr = 1
    while curptr < len(seq):
        key = seq[curptr]
        prevptr = curptr - 1
        while prevptr >= 0 and seq[prevptr] > key:
            MarkElements(prevptr, prevptr + 1, seq, window)
            seq[prevptr + 1] = seq[prevptr]
            MoveElement(prevptr, 0, window)
            MoveElement(prevptr + 1, seq[prevptr], window)
            prevptr -= 1
        seq[prevptr + 1] = key
        MoveElement(prevptr + 1, key, window)
        curptr += 1
    return seq
    
@MeasureTime
def RadixSort(seq, window):
    RADIX = 10
    maxLength = False
    tmp, placement = -1, 1
    while not maxLength:
        maxLength = True
        buckets = [[] for _ in range(RADIX)]
        for i in seq:
            tmp = i / placement
            buckets[int(tmp % RADIX)].append(i)
            if tmp >= 1: maxLength = False
        if maxLength: break
        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                seq[a] = i
                MoveElement(a, i, window)
                a += 1
        placement *= RADIX
    return seq

@MeasureTime
def SelectionSort(seq, window):
    curptr = 0
    while curptr < len(seq):
        ptr = curptr
        keyindex = curptr
        while ptr < len(seq):
            MarkElements(ptr, keyindex, seq, window)
            if seq[ptr] <= seq[keyindex]:
                keyindex = ptr
            ptr += 1
        seq[curptr], seq[keyindex] = seq[keyindex], seq[curptr]
        MoveElements(curptr, keyindex, seq, window)
        curptr += 1
    return seq
      
@MeasureTime
def CountingSort(seq, window):
    MAX = CANVAS_SIZE
    count = [0] * (MAX + 1)
    for item in seq: 
        count[item] += 1
        MoveElement(item, count[item], window)
    i = 0
    for item in range(MAX + 1):
        for c in range(count[item]):
            seq[i] = item
            MoveElement(i, seq[i], window)
            i += 1
    return seq
      
@MeasureTime
def BucketSort(seq, window):
    minValue = 0
    maxValue = CANVAS_SIZE
    bucketSize = 4
    bucketCount = int((maxValue - minValue) / bucketSize) + 1
    buckets = []
    for i in range(0, bucketCount): buckets.append([])
    for i in range(0, len(seq)): 
        index = int((seq[i] - minValue) / bucketSize)
        buckets[index].append(seq[i])
        MoveElement((index * bucketSize) + len(buckets[index]) - 1, seq[i], window)      
    seq = []
    offset = 0
    for i in range(0, len(buckets)):
        seq.append(MS(buckets[i], offset))
        offset += len(buckets[i])
    return seq

def UpdateUI(seq, window):
    while True:
        pygame.time.wait(100)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:                               
                GenerateUI(seq, window)
                return
           
if __name__ == "__main__":
    window = pygame.display.set_mode((FRAMEWIDTH, FRAMEHEIGHT))  
    window.fill((255, 255, 255))
    pygame.display.set_caption("Sortings @ github.com/worldbeater")
    sample = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
    _sample = sample.copy()
    GenerateUI(_sample, window)
    while True:
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                x = point[0]
                y = point[1]
                if y < 30:
                    if   x < 60 : BubbleSort(_sample, window)
                    elif x < 120: SelectionSort(_sample, window)
                    elif x < 180: InsertionSort(_sample, window)
                    elif x < 240: HeapSort(_sample, window)
                    elif x < 300: RadixSort(_sample, window)
                    elif x < 360: MergeSort(_sample, window)
                    elif x < 420: CombSort(_sample, window)
                    elif x < 480: QuickSort(_sample, window)
                    _sample = sample.copy()
                    UpdateUI(_sample, window)
                elif y < 55:
                    if   x < 60 : GnomeSort(_sample, window)
                    elif x < 120: EvenOddSort(_sample, window)
                    elif x < 180: ShakerSort(_sample, window)
                    elif x < 240: CountingSort(_sample, window)
                    elif x < 300: BucketSort(_sample, window)
                    else:
                        if RECTWIDTH < 20:
                            RECTWIDTH = int((RECTWIDTH + 10) / 10) * 10
                        else: 
                            RECTWIDTH = 1
                        CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
                        sample = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
                        _sample = sample.copy()
                        GenerateUI(_sample, window)
                        break
                    _sample = sample.copy()
                    UpdateUI(_sample, window)