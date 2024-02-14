import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QGridLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pandas import ExcelFile
from components.matplot import MatplotlibWidget
from components.stats import StatsWidget

# Student Id	Student Name	Gender	Program - Major	Category	School Name	Department	Foreign Category	Nationality	Hostel	Room	Hold	Term Active	Hold Status	Email
# 1410110012	Abhishek  Kumar	Male	Bachelor of Technology - Electrical and Electronics Engineering	UGRD	School of Engineering	Electrical Engineering		India	Not Allocated		No	No		ak206@snu.edu.in


class ExcelReaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Reader")
        self.setGeometry(0, 0, 800, 600)

        self.option = ""
        self.data = None
        self.graph_option = "Bar"
        self.ef = None
        self.sheet = 0

        self.layout = QGridLayout()

        # Info tab layout
        self.info_layout = QVBoxLayout()
        self.label_filename = QLabel("No file selected")
        self.info_layout.addWidget(self.label_filename)

        self.header_label = QLabel("Pick a column")
        self.info_layout.addWidget(self.header_label)

        # Add QComboBox to display header_list
        self.header_combobox = QComboBox()
        self.header_combobox.currentIndexChanged.connect(self.pick_combo)
        self.info_layout.addWidget(self.header_combobox)

        self.graph_label = QLabel("Pick a graph type")
        self.info_layout.addWidget(self.graph_label)

        # Graph options
        self.graph_options = ["Bar", "Pie", "Line"]
        self.graph_combobox = QComboBox()
        self.graph_combobox.addItems(self.graph_options)
        self.graph_combobox.currentIndexChanged.connect(self.pick_graph)
        self.info_layout.addWidget(self.graph_combobox)

        self.sheet_label = QLabel("Pick a sheet")
        self.info_layout.addWidget(self.sheet_label)

        # Sheet options
        self.sheet_option = QComboBox()
        self.sheet_option.currentIndexChanged.connect(self.pick_sheet)
        self.info_layout.addWidget(self.sheet_option)

        # Bar chart layout
        self.chart_widget = MatplotlibWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_layout.addWidget(self.chart_widget)

        self.stats_widget = StatsWidget()
        self.stats_layout = QVBoxLayout()
        self.stats_layout.addWidget(self.stats_widget)


        # Empty layout
        self.empty_widget = QWidget()
        self.empty_layout = QVBoxLayout()
        self.empty_layout.addWidget(self.empty_widget)

        # Open file button
        self.button = QPushButton("Open file")
        self.button.clicked.connect(self.open_file)


        # Add widgets to the main layout
        self.layout.addLayout(self.stats_layout, 0, 0)
        self.layout.addLayout(self.chart_layout, 0, 1)
        self.layout.addLayout(self.info_layout, 1, 0)
        self.layout.addWidget(self.button, 2, 0, 1, 2)  # Stretch button over two columns

        self.setLayout(self.layout)
        self.showMaximized()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName()

        if path:
            header_list, file = self.read_excel_file(path)
            self.update_chart_tab(file['Gender'])
            self.update_info_tab(header_list)
            self.data = file

    def update_info_tab(self, header_list):
        self.header_combobox.clear()
        self.header_combobox.addItems(header_list)
        self.option = header_list[0]

    def seondary_info_tab_update(self, header_list):
        self.header_combobox.clear()
        self.header_combobox.addItems(header_list)

    def determine_data_type(self, data):
        # check if numbers or strings
        return data.dtype == "object" and data.str.isnumeric().all()

    def sanitize_data(self, data):
        # convert into numbers if possible
        if self.determine_data_type(data):
            return data.astype(int)
        return data

    def update_chart_tab(self, gender_column):

        self.stats_widget.display_frequency_count(gender_column)
        self.stats_widget.display_stats_in_percent(gender_column)

        if self.graph_option == "Bar":
            self.chart_widget.plot_bar(gender_column)
        elif self.graph_option == "Pie":
            self.chart_widget.plot_pie(gender_column)
        elif self.graph_option == "Line" and self.determine_data_type(gender_column):
            self.sanitize_data(gender_column)
            self.chart_widget.plot_line(gender_column)

    def pick_combo(self, index):
        if self.data is not None:
            self.option = self.header_combobox.itemText(index)
            if self.option:
                self.update_chart_tab(self.data[self.option])

    def pick_graph(self, index):
        if self.data is not None:
            self.graph_option = self.graph_combobox.itemText(index)
            self.update_chart_tab(self.data[self.option])

    def read_excel_file(self, path):
        df = ExcelFile(path)
        self.ef = df
        self.sheet_option.addItems(df.sheet_names)
        file = df.parse(df.sheet_names[0], skiprows=1)
        header_list = file.columns.tolist()
        return header_list, file

    def pick_sheet(self, index):
        self.sheet = index
        self.sheet_option.setCurrentIndex(index)
        self.update_data_from_sheet(index)

    def update_data_from_sheet(self, index):
        file = self.ef.parse(self.ef.sheet_names[index], skiprows=1)
        header_list = file.columns.tolist()
        self.data = file
        self.seondary_info_tab_update(header_list)
        self.update_chart_tab(file[self.option])

def main():
    app = QApplication(sys.argv)
    window = ExcelReaderApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
