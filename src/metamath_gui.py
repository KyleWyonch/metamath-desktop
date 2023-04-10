from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidgetItem, QListWidget,
    QLineEdit, QTextBrowser, QVBoxLayout, QWidget, QFileDialog, QToolBar, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from metamath_parser import main as parse_metamath_database

import sys

class ParseThread(QThread):
    header_parsed = pyqtSignal(list)

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def run(self):
        header = parse_metamath_database(self.file_name)
        self.header_parsed.emit(header)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metamath Proof Explorer")

        self.init_ui()

    def init_ui(self):
        self.create_toolbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        layout.addWidget(self.search_bar)

        self.proof_viewer = QTextBrowser()
        layout.addWidget(self.proof_viewer)

        central_widget.setLayout(layout)

        self.proof_list_dock = QDockWidget("Labels")
        self.proof_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.proof_list = QListWidget()
        self.proof_list_dock.setWidget(self.proof_list)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.proof_list_dock)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        open_file_action = QAction(QIcon("OpenFile.png"), "Open File", self)
        open_file_action.triggered.connect(self.open_file)
        toolbar.addAction(open_file_action)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Metamath File", "", "Metamath Files (*.mm)")
        if file_name:
            self.load_metamath_file(file_name)

    def load_metamath_file(self, file_name):
        self.proof_list.clear()
        self.proof_viewer.setHtml("<p>Loading...</p>")
        self.parsing_thread = ParseThread(file_name)
        self.parsing_thread.header_parsed.connect(self.add_labels_to_list)
        self.parsing_thread.finished.connect(self.show_first_label)
        self.parsing_thread.start()

    def add_labels_to_list(self, header):
        # Clear the existing items in the proof list
        self.proof_list.clear()

        # Add an item for each header label to the proof list
        for label in header:
            print(label)
            item = QListWidgetItem(label)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            item.setCheckState(Qt.Unchecked)
            self.proof_list.addItem(item)

    def show_first_label(self):
        if self.proof_list.count() > 0:
            first_label = self.proof_list.item(0).text()
            self.proof_viewer.setHtml(f"<h1>{first_label}</h1>")
        else:
            self.proof_viewer.setHtml("<p>No labels found.</p>")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
