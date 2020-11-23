import matplotlib.pyplot as plt
from collections import deque
import numpy as np

''' Считывание информации из файлов о полседних 5 играх '''
with open('tetris_datetime.txt') as f:
        datetime_list=list(deque(f, 5))

with open('tetris_score.txt') as t:
        score_list = list(deque(t, 5))

int_score_list = [int(i) for i in score_list]


''' Нахождение рекордного результата '''
record_list = []
with open('tetris_score.txt') as p:
    record_list = p.read().splitlines()

int_record_list = [int(i) for i in  record_list]
rec = max(int_record_list)

''' Создание столбчатой диаграммы '''
x=datetime_list
y=int_score_list
fig, ax = plt.subplots()
color_rectangle = np.random.rand(7, 3)    # RGB
ax.bar(x, y, color = color_rectangle)
ax.set_title('Статистика игр', fontsize=14, fontweight="bold")
fig.set_figwidth(13)
fig.set_figheight(6)
fig.set_facecolor('floralwhite')
ax.set_facecolor('seashell')

plt.xlabel("Рекорд: " + str(rec) + 40*'   ', fontsize = 14)
plt.show()
