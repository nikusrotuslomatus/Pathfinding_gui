from PyQt5.QtWidgets import QDialog, QFormLayout, QSpinBox, QComboBox, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QFormLayout(self)

        # Динамическая настройка размеров сетки
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(10, 100)
        self.rows_spin.setValue(20)
        layout.addRow("Rows:", self.rows_spin)

        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(10, 100)
        self.cols_spin.setValue(20)
        layout.addRow("Columns:", self.cols_spin)

        self.cell_size_spin = QSpinBox()
        self.cell_size_spin.setRange(10, 50)
        self.cell_size_spin.setValue(30)
        layout.addRow("Cell Size:", self.cell_size_spin)

        # Выбор цветовой темы
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Blue"])
        layout.addRow("Theme:", self.theme_combo)

        # Расширенная настройка скорости анимации
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(50, 1000)
        self.speed_spin.setValue(200)
        layout.addRow("Animation Speed (ms):", self.speed_spin)

        # Кнопка подтверждения настроек
        btn = QPushButton("OK")
        btn.clicked.connect(self.accept)
        layout.addRow(btn)

    def get_settings(self):
        return {
            "rows": self.rows_spin.value(),
            "cols": self.cols_spin.value(),
            "cell_size": self.cell_size_spin.value(),
            "theme": self.theme_combo.currentText(),
            "speed": self.speed_spin.value()
        }
