from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibWidget(FigureCanvas):

    def __init__(self):
        self.fig = Figure(figsize=(5, 6), dpi=100)
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
        self.draw()
    
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


