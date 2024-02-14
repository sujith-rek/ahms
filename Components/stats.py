import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout


class StatsWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.freq_label = QLabel("Frequency Count")
        self.layout.addWidget(self.freq_label)
        self.freq_data = QLabel("")
        self.layout.addWidget(self.freq_data)

        self.stats_label = QLabel("Stats in Percent")
        self.layout.addWidget(self.stats_label)
        self.stats_data = QLabel("")
        self.layout.addWidget(self.stats_data)

        self.setLayout(self.layout)

    def display_frequency_count(self, data):
        self.freq_data.setText(str(data.value_counts()))
    
    def display_stats_in_percent(self, data):
        self.stats_data.setText(str(data.describe(percentiles=np.arange(0, 1, 0.1))))
    

    

