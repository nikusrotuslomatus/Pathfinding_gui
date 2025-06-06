from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class TutorialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Interactive Tutorial")
        layout = QVBoxLayout(self)
        self.label = QLabel("Step 1: Choose a mode (draw walls, set start/end)...")
        layout.addWidget(self.label)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_step)
        layout.addWidget(self.next_btn)
        self.steps = [
            "Step 1: Choose a mode (draw walls, set start/end).",
            "Step 2: Draw obstacles on the grid.",
            "Step 3: Set the start and end points.",
            "Step 4: Select an algorithm and run the animation.",
            "Step 5: Observe statistics and explanations in the panels."
        ]
        self.current_step = 0

    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.steps):
            self.label.setText(self.steps[self.current_step])
        else:
            self.accept()
