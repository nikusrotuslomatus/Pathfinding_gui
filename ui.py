from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QMainWindow, QToolBar, QAction, QComboBox, QMessageBox, QDockWidget, QWidget, QVBoxLayout, QLabel, QPushButton,
    QApplication
)
from PyQt5.QtCore import Qt
from grid_widget import GridWidget
from algorithms import ALGORITHMS
from animation import Animator
from settings import SettingsDialog
from config_manager import save_config, load_config
from stats_panel import StatsPanel
from tutorial import TutorialDialog

# Algorithm explanations
ALGORITHM_EXPLANATIONS = {
    "BFS": """
    <h3>Breadth-First Search (BFS)</h3>
    <p>BFS explores all nodes at the present depth before moving on to nodes at the next depth level.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Guarantees the shortest path in unweighted graphs</li>
        <li>Uses a queue data structure</li>
        <li>Complete and optimal for unweighted graphs</li>
    </ul>
    <h4>Time Complexity: O(V + E)</h4>
    <h4>Space Complexity: O(V)</h4>
    """,
    
    "DFS": """
    <h3>Depth-First Search (DFS)</h3>
    <p>DFS explores as far as possible along each branch before backtracking.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Uses a stack data structure</li>
        <li>May not find the shortest path</li>
        <li>Good for exploring deep paths</li>
    </ul>
    <h4>Time Complexity: O(V + E)</h4>
    <h4>Space Complexity: O(V)</h4>
    """,
    
    "A*": """
    <h3>A* Search</h3>
    <p>A* combines the advantages of Dijkstra's algorithm and Greedy Best-First Search.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Uses heuristic function to guide search</li>
        <li>Guarantees optimal path if heuristic is admissible</li>
        <li>More efficient than Dijkstra's for most cases</li>
    </ul>
    <h4>Time Complexity: O(E log V)</h4>
    <h4>Space Complexity: O(V)</h4>
    """,
    
    "Dijkstra": """
    <h3>Dijkstra's Algorithm</h3>
    <p>Dijkstra's algorithm finds the shortest path between nodes in a graph.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Guarantees shortest path in weighted graphs</li>
        <li>Uses priority queue</li>
        <li>Works with non-negative edge weights</li>
    </ul>
    <h4>Time Complexity: O((V + E) log V)</h4>
    <h4>Space Complexity: O(V)</h4>
    """,
    
    "Beam Search": """
    <h3>Beam Search</h3>
    <p>Beam Search is a heuristic search algorithm that explores a graph by expanding the most promising nodes.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Limited memory usage</li>
        <li>May not find optimal path</li>
        <li>Good for large search spaces</li>
    </ul>
    <h4>Time Complexity: O(b * w)</h4>
    <h4>Space Complexity: O(w)</h4>
    """,
    
    "Greedy Best-First": """
    <h3>Greedy Best-First Search</h3>
    <p>Greedy Best-First Search uses heuristic function to choose the most promising path.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Uses only heuristic function</li>
        <li>May not find optimal path</li>
        <li>Very fast but not complete</li>
    </ul>
    <h4>Time Complexity: O(b^m)</h4>
    <h4>Space Complexity: O(b^m)</h4>
    """,
    
    "IDDFS": """
    <h3>Iterative Deepening Depth-First Search (IDDFS)</h3>
    <p>IDDFS combines the space-efficiency of DFS with the completeness of BFS.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Guarantees optimal path in unweighted graphs</li>
        <li>Uses less memory than BFS</li>
        <li>May visit same nodes multiple times</li>
    </ul>
    <h4>Time Complexity: O(b^d)</h4>
    <h4>Space Complexity: O(bd)</h4>
    """,
    
    "Bidirectional BFS": """
    <h3>Bidirectional BFS</h3>
    <p>Bidirectional BFS searches from both start and goal nodes simultaneously.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Faster than regular BFS</li>
        <li>Guarantees shortest path</li>
        <li>Requires more memory than regular BFS</li>
    </ul>
    <h4>Time Complexity: O(b^(d/2))</h4>
    <h4>Space Complexity: O(b^(d/2))</h4>
    """,
    
    "Depth-Limited DFS": """
    <h3>Depth-Limited DFS</h3>
    <p>Depth-Limited DFS is DFS with a maximum depth limit.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Prevents infinite loops</li>
        <li>May not find solution if depth limit is too small</li>
        <li>Memory efficient</li>
    </ul>
    <h4>Time Complexity: O(b^l)</h4>
    <h4>Space Complexity: O(bl)</h4>
    """,
    
    "Random Walk": """
    <h3>Random Walk</h3>
    <p>Random Walk is a pathfinding algorithm that makes random choices at each step.</p>
    <h4>Key Characteristics:</h4>
    <ul>
        <li>Simple to implement</li>
        <li>Not guaranteed to find path</li>
        <li>May take long time to find solution</li>
    </ul>
    <h4>Time Complexity: O(∞)</h4>
    <h4>Space Complexity: O(1)</h4>
    """,
    
    "Q-Learning": """
    <h3>Q-Learning</h3>
    <p>Q-Learning is a reinforcement learning algorithm that learns the value of an action in a particular state.</p>
    <h4>Reward and Punishment Structure:</h4>
    <ul>
        <li><b>+100</b> for reaching the goal</li>
        <li><b>+2</b> for moving to a new (unvisited in episode) cell</li>
        <li><b>+3</b> for moving closer to the goal (distance-based reward)</li>
        <li><b>-1</b> for each step taken (default step penalty)</li>
        <li><b>-3</b> for moving further from the goal (distance-based penalty)</li>
        <li><b>-20</b> for revisiting a cell (loop/stale)</li>
        <li><b>-20</b> for hitting a wall or going out of bounds</li>
        <li><b>-30</b> for entering a dead end (no valid moves except backtracking)</li>
        <li><b>-30</b> for oscillation (repeatedly visiting the same cell in a short window)</li>
    </ul>
    <h4>Parameters:</h4>
    <ul>
        <li>Learning Rate (α): 0.1</li>
        <li>Discount Factor (γ): 0.95</li>
        <li>Epsilon (ε): starts at 1.0, decays to 0.05</li>
        <li>Episodes: 5000</li>
        <li>Max Steps per Episode: 400</li>
    </ul>
    <h4>Notes:</h4>
    <ul>
        <li>The agent is encouraged to find the shortest, most efficient path to the goal.</li>
        <li>Loops, dead ends, and invalid moves are strongly discouraged.</li>
        <li>Distance-based rewards help guide the agent toward the goal.</li>
    </ul>
    """
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Path Finding Visualizer")
        self.resize(1000, 700)

        # Центральный виджет – интерактивная сетка
        self.grid_widget = GridWidget()
        self.setCentralWidget(self.grid_widget)

        # Инициализация меню, тулбара и dock‑виджетов
        self.init_menu()
        self.init_toolbar()
        self.init_docks()
        self.statusBar().showMessage("Ready")
        self.animator = None

    def init_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        reset_action = QAction("Reset Grid", self)
        reset_action.setToolTip("Clear grid and reset start/end points")
        reset_action.triggered.connect(self.grid_widget.reset_grid)
        file_menu.addAction(reset_action)

        save_action = QAction("Save Configuration", self)
        save_action.setToolTip("Save current grid configuration")
        save_action.triggered.connect(lambda: save_config(self.grid_widget))
        file_menu.addAction(save_action)

        load_action = QAction("Load Configuration", self)
        load_action.setToolTip("Load grid configuration")
        load_action.triggered.connect(lambda: load_config(self.grid_widget))
        file_menu.addAction(load_action)

        settings_action = QAction("Settings", self)
        settings_action.setToolTip("Open settings dialog")
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)

        exit_action = QAction("Exit", self)
        exit_action.setToolTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("&Help")
        tutorial_action = QAction("Tutorial", self)
        tutorial_action.setToolTip("Start interactive tutorial")
        tutorial_action.triggered.connect(self.open_tutorial)
        help_menu.addAction(tutorial_action)

        about_action = QAction("About", self)
        about_action.setToolTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Выбор алгоритма
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(list(ALGORITHMS.keys()))
        self.algorithm_combo.setToolTip("Select a path finding algorithm")
        self.algorithm_combo.currentTextChanged.connect(self.update_algorithm_explanation)
        toolbar.addWidget(self.algorithm_combo)

        # Режимы работы
        action_wall = QAction("Draw Walls", self)
        action_wall.setToolTip("Toggle wall drawing mode")
        action_wall.triggered.connect(lambda: self.set_mode("wall"))
        toolbar.addAction(action_wall)

        action_start = QAction("Set Start", self)
        action_start.setToolTip("Set start point")
        action_start.triggered.connect(lambda: self.set_mode("start"))
        toolbar.addAction(action_start)

        action_end = QAction("Set End", self)
        action_end.setToolTip("Set end point")
        action_end.triggered.connect(lambda: self.set_mode("end"))
        toolbar.addAction(action_end)

        toolbar.addSeparator()

        # Запуск анимации и пошаговое управление
        action_run = QAction("Run Animation", self)
        action_run.setToolTip("Run the selected algorithm")
        action_run.triggered.connect(self.start_animation)
        toolbar.addAction(action_run)

        action_stop = QAction("Stop", self)
        action_stop.setToolTip("Stop the current animation")
        action_stop.triggered.connect(self.stop_animation)
        toolbar.addAction(action_stop)

        action_step_forward = QAction("Step Forward", self)
        action_step_forward.setToolTip("Execute next step")
        action_step_forward.triggered.connect(self.step_forward)
        toolbar.addAction(action_step_forward)

        action_step_back = QAction("Step Backward", self)
        action_step_back.setToolTip("Go back one step")
        action_step_back.triggered.connect(self.step_backward)
        toolbar.addAction(action_step_back)

    def init_docks(self):
        # Статистика алгоритма
        self.stats_panel = StatsPanel()
        dock_stats = QDockWidget("Statistics", self)
        dock_stats.setWidget(self.stats_panel)
        self.addDockWidget(0x1, dock_stats)  # Qt.LeftDockWidgetArea

        # Пояснения и документация алгоритма
        self.explanation_dock = QDockWidget("Algorithm Explanation", self)
        explanation_widget = QWidget()
        layout = QVBoxLayout()
        explanation_widget.setLayout(layout)
        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setTextFormat(Qt.RichText)
        layout.addWidget(self.explanation_label)
        self.explanation_dock.setWidget(explanation_widget)
        self.addDockWidget(0x2, self.explanation_dock)  # Qt.RightDockWidgetArea
        
        # Set initial explanation
        self.update_algorithm_explanation(self.algorithm_combo.currentText())

    def set_mode(self, mode):
        self.grid_widget.mode = mode
        self.statusBar().showMessage(f"Mode set to: {mode}")

    def start_animation(self):
        grid_data = self.grid_widget.get_grid_data()
        if self.grid_widget.start_point is None or self.grid_widget.end_point is None:
            QMessageBox.warning(self, "Warning", "Please set both start and end points!")
            return

        # Clear any previous animation highlights
        self.grid_widget.clear_animation_highlights()

        start = self.grid_widget.start_point
        end = self.grid_widget.end_point
        algo_name = self.algorithm_combo.currentText()
        algo_function = ALGORITHMS.get(algo_name)
        if not algo_function:
            QMessageBox.critical(self, "Error", f"Algorithm {algo_name} not found!")
            return

        result = None
        if algo_name == "Q-Learning":
            # Pass the clear_animation_highlights callback for Q-Learning
            result = algo_function(grid_data, start, end, clear_callback=self.grid_widget.clear_animation_highlights)
        else:
            result = algo_function(grid_data, start, end)

        if isinstance(result, tuple):
            self.animation_steps, path = result
        else:
            self.animation_steps = result
            path = None

        if not self.animation_steps:
            QMessageBox.information(self, "Result", "No path found!")
            return

        self.animator = Animator(self.grid_widget, self.animation_steps, path=path, interval=200)
        self.animator.start()
        self.statusBar().showMessage(f"Running {algo_name}...")
        # Обновление статистики
        path_length = len(path) if path else "N/A"
        self.stats_panel.update_stats({"Nodes visited": len(self.animation_steps), "Path length": path_length})

    def stop_animation(self):
        """Stop the current animation and allow manual stepping."""
        if self.animator is not None:
            self.animator.stop()
            self.statusBar().showMessage("Animation stopped. Use step controls to continue.")

    def step_forward(self):
        """Execute one step forward in the animation."""
        if self.animator is not None:
            if self.animator.step_forward():
                self.statusBar().showMessage(f"Step {self.animator.current_step} of {len(self.animator.steps)}")
            else:
                self.statusBar().showMessage("Animation complete")

    def step_backward(self):
        """Execute one step backward in the animation."""
        if self.animator is not None:
            if self.animator.step_backward():
                self.statusBar().showMessage(f"Step {self.animator.current_step} of {len(self.animator.steps)}")
            else:
                self.statusBar().showMessage("At the beginning of animation")

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():  # если пользователь нажал OK
            settings = dialog.get_settings()
            # Применяем настройки к сетке
            self.grid_widget.apply_settings(settings)
            # Применяем выбранную тему
            self.apply_theme(settings.get("theme", "Light"))
            # Обновляем интервал анимации, если нужно (пример)
            if self.animator is not None:
                self.animator.interval = settings.get("speed", 200)

    def apply_theme(self, theme):
        if theme == "Dark":
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.instance().setPalette(dark_palette)
        elif theme == "Blue":
            blue_palette = QPalette()
            blue_palette.setColor(QPalette.Window, QColor(53, 122, 204))
            blue_palette.setColor(QPalette.WindowText, Qt.white)
            blue_palette.setColor(QPalette.Base, QColor(25, 25, 112))
            blue_palette.setColor(QPalette.AlternateBase, QColor(53, 122, 204))
            blue_palette.setColor(QPalette.ToolTipBase, Qt.white)
            blue_palette.setColor(QPalette.ToolTipText, Qt.white)
            blue_palette.setColor(QPalette.Text, Qt.white)
            blue_palette.setColor(QPalette.Button, QColor(53, 122, 204))
            blue_palette.setColor(QPalette.ButtonText, Qt.white)
            blue_palette.setColor(QPalette.BrightText, Qt.red)
            blue_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            blue_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            blue_palette.setColor(QPalette.HighlightedText, Qt.black)
            QApplication.instance().setPalette(blue_palette)
        else:  # Light (по умолчанию)
            QApplication.instance().setPalette(QApplication.instance().style().standardPalette())
    def open_tutorial(self):
        dialog = TutorialDialog(self)
        dialog.exec_()

    def show_about(self):
        QMessageBox.about(
            self,
            "About Path Finding Visualizer",
            "Path Finding Visualizer\nVersion 1.0\nDeveloped with PyQt5\n\nDemonstrates various path finding algorithms with an enhanced, user-friendly interface.",
        )

    def update_algorithm_explanation(self, algorithm_name):
        """Update the algorithm explanation when a new algorithm is selected."""
        explanation = ALGORITHM_EXPLANATIONS.get(algorithm_name, "No explanation available.")
        self.explanation_label.setText(explanation)
