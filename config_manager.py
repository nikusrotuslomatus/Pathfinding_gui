import json
from PyQt5.QtWidgets import QFileDialog

def save_config(grid_widget):
    config = {
        "grid": grid_widget.get_grid_data(),
        "start": grid_widget.start_point,
        "end": grid_widget.end_point
    }
    filename, _ = QFileDialog.getSaveFileName(grid_widget, "Save Configuration", "", "JSON Files (*.json)")
    if filename:
        with open(filename, "w") as f:
            json.dump(config, f)

def load_config(grid_widget):
    import json
    from PyQt5.QtWidgets import QFileDialog
    filename, _ = QFileDialog.getOpenFileName(None, "Load Configuration", "", "JSON Files (*.json)")
    if filename:
        with open(filename, "r") as f:
            config = json.load(f)
        grid_widget.load_from_config(config)
