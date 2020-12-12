from random import choice
from collections import deque
from io import BytesIO

import matplotlib.pyplot as plt

import sett

def record():
    with open('tetris_score.txt') as p:
        record_list = p.read().splitlines()
    int_record_list = [int(i) for i in record_list]
    rec = max(int_record_list)
    return rec

def histogramm():
    buffer_ = BytesIO()
    """ Считывание информации из файлов о последних 5 играх """
    with open('tetris_datetime.txt') as f:
        datetime_list = list(deque(f, 5))

    with open('tetris_score.txt') as t:
        score_list = list(deque(t, 5))

    int_score_list = [int(i) for i in score_list]


    """ Создание столбчатой диаграммы """
    if sett.WHITE_HEX == '#000000':  # Смена цвета подложки в случае темной темы
        plt.style.use('dark_background')
    x = datetime_list
    y = int_score_list
    fig, ax = plt.subplots()

    curr_colors = []
    for i in range(5):
        curr_colors.append(choice(sett.colors_HEX))


    color_rectangle = curr_colors
    ax.bar(x, y, color=color_rectangle, edgecolor='k')
    fig.set_figwidth(13)
    fig.set_figheight(6)
    fig.set_facecolor('white')
    ax.set_facecolor(sett.WHITE_HEX)

    for x, y in zip(datetime_list, int_score_list):
        plt.text(x, y + 1, '%d' % y, ha='center', va='bottom', fontsize=14)

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(14)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.savefig(buffer_, bbox_inches='tight', dpi=80)
    buffer_.seek(0)
    return buffer_
