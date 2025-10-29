import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from tipoAlimento import crearTipos




def main():
    app = QApplication(sys.argv)
    loader = QUiLoader()
    file = QFile("main_ui.ui")
    file.open(QFile.ReadOnly)
    window = loader.load(file)
    file.close()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()