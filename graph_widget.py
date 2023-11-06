from graph import Graph
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets

matplotlib.use("Qt5Agg")


class GraphWidget(QtWidgets.QDialog):
    def __init__(self, x, y, labels, mult_plots=False):
        super().__init__()
        graph = Graph(x, y, labels, mult_subplots=mult_plots)

        sc = FigureCanvasQTAgg(graph.figure)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        self.setLayout(layout)
