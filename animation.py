from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor
# Для плавных анимаций можно использовать QPropertyAnimation – здесь оставляем QTimer как базовый вариант

class Animator:
    def __init__(self, grid_widget, steps, path=None, interval=200):
        """
        :param grid_widget: экземпляр GridWidget для обновления отображения.
        :param steps: список шагов, полученный от алгоритма.
        :param path: список координат финального пути (если есть).
        :param interval: интервал обновления в миллисекундах.
        """
        self.grid_widget = grid_widget
        self.steps = steps
        self.path = path
        self.interval = interval
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)
        self.is_running = False

    def start(self):
        self.is_running = True
        self.timer.start(self.interval)

    def stop(self):
        self.is_running = False
        self.timer.stop()

    def animate_step(self):
        if self.current_step < len(self.steps):
            i, j = self.steps[self.current_step]
            # Подсвечиваем ячейку (если она не является стартовой или конечной)
            if (i, j) != self.grid_widget.start_point and (i, j) != self.grid_widget.end_point:
                # Если это часть финального пути, окрашиваем в синий
                if self.path and (i, j) in self.path:
                    self.grid_widget.cells[(i, j)].setBrush(QBrush(QColor("blue")))
                else:
                    self.grid_widget.cells[(i, j)].setBrush(QBrush(QColor("yellow")))
            self.current_step += 1
        else:
            self.stop()

    def step_forward(self):
        """Execute one step forward manually."""
        if self.current_step < len(self.steps):
            self.animate_step()
            return True
        return False

    def step_backward(self):
        """Execute one step backward manually."""
        if self.current_step > 0:
            self.current_step -= 1
            # Reset the color of the current cell
            i, j = self.steps[self.current_step]
            if (i, j) != self.grid_widget.start_point and (i, j) != self.grid_widget.end_point:
                # If it was part of the path, we need to check if it should remain blue
                if self.path and (i, j) in self.path:
                    self.grid_widget.cells[(i, j)].setBrush(QBrush(QColor("blue")))
                else:
                    self.grid_widget.cells[(i, j)].setBrush(QBrush(QColor("lightGray")))
            return True
        return False

    def is_finished(self):
        """Check if the animation has reached the end."""
        return self.current_step >= len(self.steps)
