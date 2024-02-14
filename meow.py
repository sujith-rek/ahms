import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pandas import ExcelFile
from components.matplot import MatplotlibWidget

class ExcelReaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Reader")
        self.setGeometry(0, 0, 800, 600)

        self.layout = QVBoxLayout()

        # Add QComboBox to display header_list
        self.header_combobox = QComboBox()
        self.header_combobox.currentIndexChanged.connect(self.pick_combo)
        self.layout.addWidget(self.header_combobox)

        self.graph_options = ["Bar", "Pie", "Line"]
        self.graph_combobox = QComboBox()
        self.graph_combobox.addItems(self.graph_options)
        self.graph_combobox.currentIndexChanged.connect(self.pick_graph)
        self.layout.addWidget(self.graph_combobox)

        # Bar chart layout
        self.chart_widget = MatplotlibWidget()
        self.layout.addWidget(self.chart_widget)

        # Open file button
        self.button = QPushButton("Open file")
        self.button.clicked.connect(self.open_file)
        self.layout.addWidget(self.button)

        self.option = ""
        self.data = None
        self.original_data = None
        self.graph_option = "Bar"
    
        self.setLayout(self.layout)
        self.showMaximized()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName()

        if path:
            header_list, file = read_excel_file(path)
            self.original_data = file.copy()
            self.update_chart_tab(file['Gender'])
            self.update_info_tab(header_list)
            self.data = file

    def update_info_tab(self, header_list):
        self.header_combobox.clear()
        self.header_combobox.addItems(header_list)
        self.option = header_list[0]

    def update_chart_tab(self, gender_column):
        if self.graph_option == "Bar":
            self.chart_widget.plot_bar(gender_column)
        elif self.graph_option == "Pie":
            self.chart_widget.plot_pie(gender_column)
        elif self.graph_option == "Line":
            self.chart_widget.plot_line(self.original_data[self.option])

    def pick_combo(self, index):
        if self.data is None:
            return
        self.option = self.header_combobox.itemText(index)
        self.update_chart_tab(self.data[self.option])

    def pick_graph(self, index):
        if self.data is None:
            return
        self.graph_option = self.graph_combobox.itemText(index)
        self.update_chart_tab(self.data[self.option])

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
