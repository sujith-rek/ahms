import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QSizePolicy, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pandas import ExcelFile

class ExcelReaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Reader")
        self.setGeometry(0, 0, 800, 600)


        self.layout = QGridLayout()

        # Info tab layout
        self.info_layout = QVBoxLayout()
        self.label_filename = QLabel("No file selected")
        self.info_layout.addWidget(self.label_filename)

        # Bar chart layout
        self.chart_widget = MatplotlibWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_layout.addWidget(self.chart_widget)

        # Column data layout
        self.column_data_widget = QLabel("Column Data")
        self.column_data_layout = QVBoxLayout()
        self.column_data_layout.addWidget(self.column_data_widget)

        # Empty layout
        self.empty_widget = QWidget()
        self.empty_layout = QVBoxLayout()
        self.empty_layout.addWidget(self.empty_widget)

        # Open file button
        self.button = QPushButton("Open file")
        self.button.clicked.connect(self.open_file)

        # Add widgets to the main layout
        self.layout.addLayout(self.info_layout, 0, 0)
        self.layout.addLayout(self.chart_layout, 0, 1)
        self.layout.addLayout(self.column_data_layout, 1, 0)
        self.layout.addLayout(self.empty_layout, 1, 1)
        self.layout.addWidget(self.button, 2, 0, 1, 2)  # Stretch button over two columns

        self.setLayout(self.layout)
        self.showMaximized()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName()

        if path:
            header_list, file = read_excel_file(path)
            self.update_info_tab(path)
            self.update_chart_tab(file['Gender'])
            # self.update_column_data_tab(header_list)

    def update_info_tab(self, filename):
        self.label_filename.setText(f"File: {filename}")

    def update_chart_tab(self, gender_column):
        self.chart_widget.update_chart(gender_column)

    def update_column_data_tab(self, header_list):
        self.column_data_widget.setText(str(header_list))


class MatplotlibWidget(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        # self.ax.set_position([0.1, 0.1, 0.8, 0.8])
        super().__init__(self.fig)
        

    def update_chart(self, data):
        self.ax.clear()
        counts = data.value_counts()
        counts.plot(kind='bar', ax=self.ax)
        self.draw()


def read_excel_file(path):
    df = ExcelFile(path)
    file = df.parse(df.sheet_names[0], skiprows=1)
    header_list = file.columns.tolist()
    return header_list, file

def main():
    app = QApplication(sys.argv)
    window = ExcelReaderApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
