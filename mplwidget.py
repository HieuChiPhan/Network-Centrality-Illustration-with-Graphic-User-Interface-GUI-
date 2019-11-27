# # ------------------------------------------------------
# # -------------------- mplwidget.py --------------------
# # ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import matplotlib

import networkx as nx


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.figure = plt.figure(figsize=(15, 12))
        self.canvas = FigureCanvas(self.figure)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)



# class MplWidget(QWidget):
#     def __init__(self, figure):
#         QWidget.__init__(self, figure)
#         self.figure = figure
#         self.canvas = FigureCanvas(self.figure)
#         vertical_layout = QVBoxLayout()
#         vertical_layout.addWidget(self.canvas)
#         self.canvas.axes = self.canvas.figure.add_subplot(111)
#         self.setLayout(vertical_layout)
