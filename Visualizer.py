import random
import sys
import time

import pygame
from pygame import midi

FRAMEWIDTH = 500
RECTWIDTH = 10
INSTRUMENT_ID = 54  # 54

pygame.init()
midi.init()
PLAYER = midi.Output(0)
PLAYER.set_instrument(INSTRUMENT_ID, 1)
CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
FRAMEHEIGHT = FRAMEWIDTH + 100


def draw_rect(x1, y1, x2, y2, win, color=(90, 0, 140)):
    pygame.draw.rect(win, color, (x1, y1, x2, y2), 0)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()


def pling(note):
    if RECTWIDTH == 1:
        return
    note = round(note / CANVAS_SIZE * 50) + 50
    PLAYER.note_on(note, 127, 1)
    pygame.time.wait(100 if RECTWIDTH == 20 else 10)
    PLAYER.note_off(note, 127, 1)


def mark_elements(index1, index2, seq, window):
    draw_rect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window,
              color=(255, 0, 0))
    draw_rect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window,
              color=(255, 0, 0))
    pling(seq[index2])
    draw_rect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window)
    draw_rect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window)


def mark_element(index1, size, window):
    draw_rect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window,
              color=(255, 0, 0))
    pling(size)
    draw_rect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window)


def move_elements(index1, index2, seq, window):
    draw_rect(index1 * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color=(255, 255, 255))
    draw_rect(index1 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index1]), RECTWIDTH, RECTWIDTH * seq[index1], window)
    draw_rect(index2 * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color=(255, 255, 255))
    draw_rect(index2 * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * seq[index2]), RECTWIDTH, RECTWIDTH * seq[index2], window)
    pling(seq[index2])


def move_element(index, size, window):
    draw_rect(index * RECTWIDTH, 100, RECTWIDTH, FRAMEHEIGHT, window, color=(255, 255, 255))
    draw_rect(index * RECTWIDTH, FRAMEHEIGHT - (RECTWIDTH * size), RECTWIDTH, RECTWIDTH * size, window)
    pling(size)


def create_button(x, y, text, window, setbold=False):
    font = pygame.font.SysFont("Segoe UI", 13)
    font.set_bold(setbold)
    label = font.render(text, 1, (0, 0, 0))
    window.blit(label, (x, y - 10))


def generate_ui(seq, window):
    window.fill((255, 255, 255))
    step = 0
    for element in seq:
        draw_rect(step, FRAMEHEIGHT - (RECTWIDTH * element), RECTWIDTH, RECTWIDTH * element, window)
        step += RECTWIDTH
    create_button(10, 15, 'Bubble', window)
    create_button(70, 15, 'Selection', window)
    create_button(130, 15, 'Insertion', window)
    create_button(190, 15, 'Heap', window)
    create_button(250, 15, 'Radix', window)
    create_button(310, 15, 'Merge', window)
    create_button(370, 15, 'Comb', window)
    create_button(430, 15, 'Quick', window)
    create_button(10, 40, 'Gnome', window)
    create_button(70, 40, 'EvenOdd', window)
    create_button(130, 40, 'Shaker', window)
    create_button(190, 40, 'Counting', window)
    create_button(250, 40, 'Bucket', window)
    create_button(430, 40, 'Resize', window, setbold=True)
    pygame.display.update()


def measure_time(function):
    def timed_function(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        create_button(10, 65, 'Time: ' + str(end - start)[0:7], main_window)
        pygame.display.flip()
        return result

    return timed_function


def debug(function):
    def debugged_function(*args, **kwargs):
        import traceback
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception:
            traceback.print_exc()
        return result
    return debugged_function


@measure_time
def gnome_sort(seq, window):
    curptr = 0
    while curptr < len(seq) - 1:
        mark_elements(curptr, curptr + 1, seq, window)
        if seq[curptr] > seq[curptr + 1]:
            seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
            move_elements(curptr, curptr + 1, seq, window)
            curptr = 0
        else:
            curptr += 1
    return seq


@measure_time
def bubble_sort(seq, window):
    length = len(seq) - 1
    while length > 0:
        curptr = 0
        while curptr < length:
            mark_elements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]:
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                move_elements(curptr, curptr + 1, seq, window)
            curptr += 1
        length -= 1
    return seq


@measure_time
def shaker_sort(seq, window):
    curptr = 0
    bleft = 0
    bright = len(seq) - 1
    while bright >= bleft:
        while curptr < bright:
            mark_elements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]:
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                move_elements(curptr, curptr + 1, seq, window)
            curptr += 1
        bright -= 1
        while curptr > bleft:
            mark_elements(curptr - 1, curptr, seq, window)
            if seq[curptr - 1] > seq[curptr]:
                seq[curptr], seq[curptr - 1] = seq[curptr - 1], seq[curptr]
                move_elements(curptr - 1, curptr, seq, window)
            curptr -= 1
        bleft += 1
    return seq


@measure_time
def evenodd_sort(seq, window):
    curptr = 0
    finish = 0
    while finish < len(seq) - 1:
        while curptr < len(seq) - 1:
            mark_elements(curptr, curptr + 1, seq, window)
            if seq[curptr] > seq[curptr + 1]:
                seq[curptr], seq[curptr + 1] = seq[curptr + 1], seq[curptr]
                move_elements(curptr, curptr + 1, seq, window)
                finish = 0
            finish += 1
            curptr += 2
        curptr = abs(curptr % 2 - 1)
    return seq


@measure_time
def comb_sort(seq, window):
    decrease_factor = 1.25
    length = len(seq) - 1
    _rightptr = round(length / decrease_factor)
    while True:
        leftptr = 0
        rightptr = _rightptr
        while rightptr < len(seq):
            mark_elements(leftptr, rightptr, seq, window)
            if seq[leftptr] > seq[rightptr]:
                seq[leftptr], seq[rightptr] = seq[rightptr], seq[leftptr]
                move_elements(leftptr, rightptr, seq, window)
            rightptr += 1
            leftptr += 1
        if _rightptr > 1:
            _rightptr = int(_rightptr / decrease_factor)
        else:
            break
    return seq


@measure_time
def quick_sort(seq, window):
    def qs(_left, _right):
        left = _left
        right = _right
        pivot = seq[round((left + right) / 2)]
        while left <= right:
            while seq[left] < pivot:
                mark_elements(left, round((left + right) / 2), seq, window)
                left += 1
            while seq[right] > pivot:
                mark_elements(right, round((left + right) / 2), seq, window)
                right -= 1
            if left <= right:
                seq[right], seq[left] = seq[left], seq[right]
                move_elements(left, right, seq, window)
                left += 1
                right -= 1
        if right > _left:
            qs(_left, right)
        if _right > left:
            qs(left, _right)
    qs(0, len(seq) - 1)
    return seq


def ms(part, ofs, window):
    result = []
    if len(part) < 2:
        return part
    mid = round(len(part) / 2)
    y = ms(part[:mid], ofs, window)
    z = ms(part[mid:], mid + ofs, window)
    i = 0
    j = 0
    while i < len(y) and j < len(z):
        mark_element(ofs + i + j, y[i], window)
        if y[i] > z[j]:
            result.append(z[j])
            move_element(i + j + ofs, z[j], window)
            j += 1
        else:
            result.append(y[i])
            move_element(i + j + ofs, y[i], window)
            i += 1
    for item in y[i:]:
        result.append(item)
        move_element(ofs + len(result) - 1, item, window)
    for item in z[j:]:
        result.append(item)
        move_element(ofs + len(result) - 1, item, window)
    return result


@measure_time
def merge_sort(seq, window):
    return ms(seq, 0, window)


def shift_down(seq, i, j, window):
    while i * 2 + 1 < j:
        if i * 2 + 1 == j - 1 or seq[i * 2 + 1] > seq[i * 2 + 2]:
            max_child = i * 2 + 1
        else:
            max_child = i * 2 + 2
        mark_elements(i, max_child, seq, window)
        if seq[i] < seq[max_child]:
            seq[i], seq[max_child] = seq[max_child], seq[i]
            move_elements(i, max_child, seq, window)
            i = max_child
        else:
            break


@measure_time
def heap_sort(seq, window):
    for i in range(int(len(seq) / 2 - 1), -1, -1):
        shift_down(seq, i, len(seq), window)
    for i in range(len(seq) - 1, 0, -1):
        seq[0], seq[i] = seq[i], seq[0]
        move_elements(0, i, seq, window)
        shift_down(seq, 0, i, window)
    return seq


@measure_time
def insertion_sort(seq, window):
    curptr = 1
    while curptr < len(seq):
        key = seq[curptr]
        prevptr = curptr - 1
        while prevptr >= 0 and seq[prevptr] > key:
            mark_elements(prevptr, prevptr + 1, seq, window)
            seq[prevptr + 1] = seq[prevptr]
            move_element(prevptr, 0, window)
            move_element(prevptr + 1, seq[prevptr], window)
            prevptr -= 1
        seq[prevptr + 1] = key
        move_element(prevptr + 1, key, window)
        curptr += 1
    return seq


@measure_time
def radix_sort(seq, window):
    radix = 10
    max_length = False
    tmp, placement = -1, 1
    while not max_length:
        max_length = True
        buckets = [[] for _ in range(radix)]
        for i in seq:
            tmp = i / placement
            buckets[int(tmp % radix)].append(i)
            if tmp >= 1:
                max_length = False
        if max_length:
            break
        a = 0
        for b in range(radix):
            buck = buckets[b]
            for i in buck:
                seq[a] = i
                move_element(a, i, window)
                a += 1
        placement *= radix
    return seq


@measure_time
def selection_sort(seq, window):
    curptr = 0
    while curptr < len(seq):
        ptr = curptr
        keyindex = curptr
        while ptr < len(seq):
            mark_elements(ptr, keyindex, seq, window)
            if seq[ptr] <= seq[keyindex]:
                keyindex = ptr
            ptr += 1
        seq[curptr], seq[keyindex] = seq[keyindex], seq[curptr]
        move_elements(curptr, keyindex, seq, window)
        curptr += 1
    return seq


@measure_time
def counting_sort(seq, window):
    maximum = CANVAS_SIZE
    count = [0] * (maximum + 1)
    for item in seq:
        count[item] += 1
        move_element(item, count[item], window)
    i = 0
    for item in range(maximum + 1):
        for c in range(count[item]):
            seq[i] = item
            move_element(i, seq[i], window)
            i += 1
    return seq


@measure_time
def bucket_sort(seq, window):
    min_value = 0
    max_value = CANVAS_SIZE
    bucket_size = 4
    bucket_count = int((max_value - min_value) / bucket_size) + 1
    buckets = []
    for i in range(0, bucket_count):
        buckets.append([])
    for i in range(0, len(seq)):
        index = int((seq[i] - min_value) / bucket_size)
        buckets[index].append(seq[i])
        move_element((index * bucket_size) + len(buckets[index]) - 1, seq[i], window)
    seq = []
    offset = 0
    for i in range(0, len(buckets)):
        seq.append(ms(buckets[i], offset, window))
        offset += len(buckets[i])
    return seq


def update_ui(seq, window):
    while True:
        pygame.time.wait(100)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                generate_ui(seq, window)
                return


if __name__ == "__main__":
    main_window = pygame.display.set_mode((FRAMEWIDTH, FRAMEHEIGHT))
    main_window.fill((255, 255, 255))
    pygame.display.set_caption("Sortings @ github.com/worldbeater")
    sample = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
    _sample = sample.copy()
    generate_ui(_sample, main_window)
    while True:
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                px = point[0]
                py = point[1]
                if py < 30:
                    if px < 60:
                        bubble_sort(_sample, main_window)
                    elif px < 120:
                        selection_sort(_sample, main_window)
                    elif px < 180:
                        insertion_sort(_sample, main_window)
                    elif px < 240:
                        heap_sort(_sample, main_window)
                    elif px < 300:
                        radix_sort(_sample, main_window)
                    elif px < 360:
                        merge_sort(_sample, main_window)
                    elif px < 420:
                        comb_sort(_sample, main_window)
                    elif px < 480:
                        quick_sort(_sample, main_window)
                    _sample = sample.copy()
                    update_ui(_sample, main_window)
                elif py < 55:
                    if px < 60:
                        gnome_sort(_sample, main_window)
                    elif px < 120:
                        evenodd_sort(_sample, main_window)
                    elif px < 180:
                        shaker_sort(_sample, main_window)
                    elif px < 240:
                        counting_sort(_sample, main_window)
                    elif px < 300:
                        bucket_sort(_sample, main_window)
                    else:
                        if RECTWIDTH < 20:
                            RECTWIDTH = int((RECTWIDTH + 10) / 10) * 10
                        else:
                            RECTWIDTH = 1
                        CANVAS_SIZE = round(FRAMEWIDTH / RECTWIDTH)
                        sample = random.sample(range(CANVAS_SIZE), CANVAS_SIZE)
                        _sample = sample.copy()
                        generate_ui(_sample, main_window)
                        break
                    _sample = sample.copy()
                    update_ui(_sample, main_window)
