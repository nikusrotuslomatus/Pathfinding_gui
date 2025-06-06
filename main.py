#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale
from ui import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Многоязычная поддержка: подключение переводчика (файлы перевода должны быть подготовлены)
    translator = QTranslator()
    locale = QLocale.system().name()
    # translator.load(f"translations_{locale}.qm")  # Предполагается наличие файлов переводов
    # app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
