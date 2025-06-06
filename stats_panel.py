from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.nodes_label = QLabel("Nodes visited: 0")
        self.path_label = QLabel("Path length: 0")
        layout.addWidget(self.nodes_label)
        layout.addWidget(self.path_label)

    def update_stats(self, stats):
        self.nodes_label.setText(f"Nodes visited: {stats.get('Nodes visited', 0)}")
        self.path_label.setText(f"Path length: {stats.get('Path length', 0)}")
