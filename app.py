import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pandas import ExcelFile

class ExcelReaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Reader")
        self.setGeometry(0, 0, 800, 600)

        self.layout = QVBoxLayout()

        # Info tab layout
        self.info_layout = QVBoxLayout()
        self.label_filename = QLabel("No file selected")
        self.info_layout.addWidget(self.label_filename)

        # Bar chart layout
        self.chart_layout = QVBoxLayout()
        self.chart_widget = QLabel("No data to display")
        self.chart_layout.addWidget(self.chart_widget)

        # Open file button
        self.button = QPushButton("Open file")
        self.button.clicked.connect(self.open_file)

        # Add widgets to the main layout
        self.layout.addLayout(self.info_layout)
        self.layout.addLayout(self.chart_layout)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName()

        if path:
            header_list, file = read_excel_file(path)
            self.update_info_tab(path)
            self.update_chart_tab(file['Gender'])

    def update_info_tab(self, filename):
        self.label_filename.setText(f"File: {filename}")

    def update_chart_tab(self, gender_column):
        self.chart_widget.clear()
        self.chart_widget = MatplotlibWidget()
        self.chart_widget.ax.clear()
        counts = gender_column.value_counts()
        counts.plot(kind='bar', ax=self.chart_widget.ax)
        self.chart_widget.draw()
        self.chart_layout.addWidget(self.chart_widget)


class MatplotlibWidget(FigureCanvas):
    def __init__(self):
        fig = Figure()
        self.ax = fig.add_subplot(111)
        super().__init__(fig)


def read_excel_file(path):
    df = ExcelFile(path)
    file = df.parse(df.sheet_names[0], skiprows=1)
    header_list = file.columns.tolist()
    # print(file.columns)
    # print(file['Gender'])
    return header_list, file

def main():
    app = QApplication(sys.argv)
    window = ExcelReaderApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
