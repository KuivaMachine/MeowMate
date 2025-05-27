import numpy as np
import matplotlib.pyplot as plt

# Функция для построения буквы "Л"
def letter_L(ax, x_offset):
    t = np.linspace(0, 1, 100)
    ax.plot(x_offset + t, t, color='black')  # Вертикальная линия
    ax.plot(x_offset + t, 1 - t, color='black')  # Горизонтальная линия

# Функция для построения буквы "Е"
def letter_E(ax, x_offset):
    t = np.linspace(0, 1, 100)
    ax.plot([x_offset] * 100, t, color='black')  # Вертикальная линия
    ax.plot(x_offset + t, [1] * 100, color='black')  # Верхняя горизонтальная
    ax.plot(x_offset + t, [0.5] * 100, color='black')  # Средняя горизонтальная
    ax.plot(x_offset + t, [0] * 100, color='black')  # Нижняя горизонтальная

# Функция для построения буквы "Н"
def letter_N(ax, x_offset):
    t = np.linspace(0, 1, 100)
    ax.plot([x_offset] * 100, t, color='black')  # Левая вертикальная
    ax.plot([x_offset + 1] * 100, t, color='black')  # Правая вертикальная
    ax.plot(x_offset + t, [0.5] * 100, color='black')  # Горизонтальная линия

# Функция для построения буквы "А"
def letter_A(ax, x_offset):
    t = np.linspace(0, 1, 100)
    ax.plot(x_offset + t, t, color='black')  # Левая наклонная
    ax.plot(x_offset + t, 1 - t, color='black')  # Правая наклонная
    ax.plot(x_offset + 0.25 + 0.5 * t, [0.5] * 100, color='black')  # Горизонтальная

# Создание графика
fig, ax = plt.subplots()
letter_L(ax, 0)  # Буква "Л"
letter_E(ax, 2)  # Буква "Е"
letter_N(ax, 4)  # Буква "Н"
letter_A(ax, 6)  # Буква "А"

# Настройка графика
ax.set_aspect('equal')
ax.axis('off')  # Скрыть оси
plt.show()