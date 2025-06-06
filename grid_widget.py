from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QTransform
from PyQt5.QtCore import Qt
from undo_redo import UndoRedoManager

CELL_SIZE = 30
GRID_ROWS = 20
GRID_COLS = 20

class GridWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.cells = {}  # Ключ: (i, j) -> QGraphicsRectItem
        self.start_point = None
        self.end_point = None
        self.mode = "wall"  # Режим по умолчанию
        self.undo_redo_stack = UndoRedoManager(self)
        self.init_grid()
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # Для панорамирования

    def init_grid(self):
        self.scene.clear()
        self.cells = {}
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                rect = QGraphicsRectItem(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                rect.setBrush(QBrush(Qt.white))
                rect.setPen(Qt.gray)
                self.scene.addItem(rect)
                self.cells[(i, j)] = rect

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        j = int(pos.x() // CELL_SIZE)
        i = int(pos.y() // CELL_SIZE)
        if (i, j) in self.cells:
            # Запоминаем действие для undo/redo
            self.undo_redo_stack.record_state((i, j), self.cells[(i, j)].brush().color())
            if self.mode == "wall":
                current_color = self.cells[(i, j)].brush().color()
                if current_color == QColor(Qt.white):
                    self.cells[(i, j)].setBrush(QBrush(Qt.black))
                else:
                    self.cells[(i, j)].setBrush(QBrush(Qt.white))
            elif self.mode == "start":
                if self.start_point is not None:
                    self.cells[self.start_point].setBrush(QBrush(Qt.white))
                self.cells[(i, j)].setBrush(QBrush(Qt.green))
                self.start_point = (i, j)
            elif self.mode == "end":
                if self.end_point is not None:
                    self.cells[self.end_point].setBrush(QBrush(Qt.white))
                self.cells[(i, j)].setBrush(QBrush(Qt.red))
                self.end_point = (i, j)
            # Режим Free Draw для сложных препятствий (будет переключаться через настройки)
            # TODO: Реализовать свободное рисование
        super().mousePressEvent(event)

    def get_grid_data(self):
        grid = []
        for i in range(GRID_ROWS):
            row = []
            for j in range(GRID_COLS):
                color = self.cells[(i, j)].brush().color()
                row.append(1 if color == QColor(Qt.black) else 0)
            grid.append(row)
        return grid

    def reset_grid(self):
        self.start_point = None
        self.end_point = None
        self.init_grid()

    def apply_settings(self, settings):
        # Пример применения настроек из диалога: изменение размеров, цвета, темы
        global GRID_ROWS, GRID_COLS, CELL_SIZE
        GRID_ROWS = settings.get("rows", GRID_ROWS)
        GRID_COLS = settings.get("cols", GRID_COLS)
        CELL_SIZE = settings.get("cell_size", CELL_SIZE)
        self.init_grid()

    def clear_animation_highlights(self):
        """Clear all animation highlights while preserving walls, start, and end points."""
        for (i, j), cell in self.cells.items():
            current_color = cell.brush().color()
            # Reset cells that are yellow (animation highlights) or blue (path highlights)
            if current_color == QColor("yellow") or current_color == QColor("blue"):
                cell.setBrush(QBrush(Qt.white))

    def load_from_config(self, config):
        grid = config.get("grid")
        start = tuple(config.get("start", ()))
        end = tuple(config.get("end", ()))
        if grid:
            for i, row in enumerate(grid):
                for j, val in enumerate(row):
                    if val == 1:
                        self.cells[(i, j)].setBrush(QBrush(Qt.black))
                    else:
                        self.cells[(i, j)].setBrush(QBrush(Qt.white))
        if start:
            self.start_point = start
            self.cells[start].setBrush(QBrush(Qt.green))
        if end:
            self.end_point = end
            self.cells[end].setBrush(QBrush(Qt.red))
    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            factor = zoom_in_factor
        else:
            factor = zoom_out_factor
        self.scale(factor, factor)
