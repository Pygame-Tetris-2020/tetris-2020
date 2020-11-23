import matplotlib.pyplot as plt
from collections import deque
import numpy as np

with open('tetris_datetime.txt') as f:
        datetime_list=list(deque(f, 5))

with open('tetris_score.txt') as f:
        score_list = list(deque(f, 5))

int_score_list = [int(i) for i in score_list ]

l = []
with open('tetris_score.txt') as f:
    l = f.read().splitlines()

int_l = [int(i) for i in l ]



x=datetime_list
y=int_score_list

fig, ax = plt.subplots()

color_rectangle = np.random.rand(7, 3)    # RGB
ax.bar(x, y, color = color_rectangle)
ax.set_title('Статистика игр', fontsize=14, fontweight="bold")
fig.set_figwidth(13)    #  ширина и
fig.set_figheight(6)    #  высота "Figure"
fig.set_facecolor('floralwhite')
ax.set_facecolor('seashell')

plt.xlabel("Рекорд: " + str(max(int_l)) + 40*'   ', fontsize = 14)
plt.show()
