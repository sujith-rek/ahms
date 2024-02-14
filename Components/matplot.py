from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibWidget(FigureCanvas):

    def __init__(self):
        self.fig = Figure(figsize=(8, 10), dpi=100)
        self.ax = self.fig.add_subplot(111)

        super(MatplotlibWidget, self).__init__(self.fig)

    def plot_bar(self, data):
        self.ax.clear()
        counts = data.value_counts()
        counts.plot(kind='bar', ax=self.ax)
        self.draw()
    
    def plot_pie(self, data):
        self.ax.clear()
        counts = data.value_counts()
        counts.plot(kind='pie', ax=self.ax)
        legend_labels = counts.index
        num_wedges = len(counts)

        if num_wedges in range(1, 5):
            self.ax.legend(legend_labels, title="Legend", loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=self.ax.transAxes)


        self.draw()
        
    # def plot_pie(self, data, title="Pie Chart"):
    #     self.ax.clear()
    #     counts = data.value_counts()

    #     # Get unique colors for each wedge
    #     num_wedges = len(counts)
    #     colors = plt.cm.viridis(np.linspace(0, 1, num_wedges))

    #     # Plot pie chart
    #     wedges, texts, autotexts = self.ax.pie(counts, labels=None, autopct='%1.1f%%', startangle=90, colors=colors)

    #     # Create a legend with colors and labels
    #     legend_labels = counts.index
    #     self.ax.legend(wedges, legend_labels, title="Legend", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    #     # Customize autopct
    #     for autotext in autotexts:
    #         autotext.set_fontweight('bold')

    #     self.ax.set_title(title)
    #     self.draw()

    
    def plot_line(self, data):
        self.ax.clear()
        data.plot(ax=self.ax)
        self.draw()

    def plot_scatter(self, data):
        self.ax.clear()
        data.plot(kind='scatter', ax=self.ax)
        self.draw()

    def plot_hist(self, data):
        self.ax.clear()
        data.plot(kind='hist', ax=self.ax)
        self.draw()


