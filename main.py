import os
import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QCheckBox, QLabel, QGroupBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Plotter')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        
        self.layout = QVBoxLayout()

        self.button = QPushButton('Open File')
        self.button.clicked.connect(self.open_file)
        self.layout.addWidget(self.button)

        self.plot_button = QPushButton('Show Plot')
        self.plot_button.clicked.connect(self.show_plot)
        self.plot_button.setEnabled(False)
        self.layout.addWidget(self.plot_button)

        self.plot_group = QGroupBox("Y-axis")
        self.plot_layout = QHBoxLayout()
        self.plot_group.setLayout(self.plot_layout)
        self.layout.addWidget(self.plot_group)

        self.against_group = QGroupBox("X-axis")
        self.against_layout = QHBoxLayout()
        self.against_group.setLayout(self.against_layout)
        self.layout.addWidget(self.against_group)

        self.plot_label = QLabel()
        self.plot_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.plot_label)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "All Files (*)", options=options)
        if file_name:
            self.load_data(file_name, file_name.split("/")[-1])

    def load_data(self, file_name, short_name):
        self.data, self.columns = self.parse_file(file_name)
        self.file_name = short_name
        if self.data is not None:
            self.create_checkboxes()
        else:
            self.plot_label.setText("Unsupported file format or error reading file.")

    def detect_separator(self, file_name):
        with open(file_name, 'r') as file:
            sample = file.read(1024)  # Read a sample of the file
        delimiters = [',', ';', '\t', ' ']
        delimiter = max(delimiters, key=sample.count)
        return delimiter

    def convert_comma_to_dot(self, data):
        return data.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

    def parse_file(self, file_name):
        try:
            separator = self.detect_separator(file_name)
            if separator is None:
                return None, None

            with open(file_name, 'r') as file:
                lines = file.readlines()

            # Find the first line with data and the previous line for headers
            header_index = None
            header_line = None
            for i, line in enumerate(lines):
                if self.is_data_line(line, separator):
                    header_index = i
                    header_line = lines[i - 1] if i > 0 else line
                    break

            if header_index is None:
                return None, None

            columns = header_line.strip().split(separator)
            data = pd.read_csv(file_name, skiprows=header_index, sep=separator, names=columns)
            data = self.convert_comma_to_dot(data)
            data = data.apply(pd.to_numeric, errors='coerce')

            return data, columns

        except Exception as e:
            print(f"Error reading file: {e}")
            return None, None

    def is_data_line(self, line, separator):
        # Checks if a line is a data line by trying to parse it
        parts = line.split(separator)
        if len(parts) < 2:
            return False
        try:
            float(parts[0].replace(',', '.'))
            return True
        except ValueError:
            return False

    def create_checkboxes(self):
        self.clear_layout(self.plot_layout)
        self.clear_layout(self.against_layout)
        self.checkboxes_plot = []
        self.checkboxes_against = []

        for column in self.columns:
            checkbox_plot = QCheckBox(column)
            checkbox_against = QCheckBox(column)
            self.plot_layout.addWidget(checkbox_plot)
            self.against_layout.addWidget(checkbox_against)
            self.checkboxes_plot.append(checkbox_plot)
            self.checkboxes_against.append(checkbox_against)

        self.plot_button.setEnabled(True)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_plot(self):
        columns_to_plot = [cb.text() for cb in self.checkboxes_plot if cb.isChecked()]
        columns_against = [cb.text() for cb in self.checkboxes_against if cb.isChecked()]

        if not columns_to_plot or not columns_against:
            self.plot_label.setText("Please select columns to plot and against.")
            return

        self.plot_label.setText("")
        self.fig, self.ax = plt.subplots()

        for column_to_plot in columns_to_plot:
            for column_against in columns_against:
                self.y_data = self.data[column_to_plot]
                self.x_data = self.data[column_against]
                avg = self.y_data.mean()
                std_dev = self.y_data.std()
                min_val = self.y_data.min()
                max_val = self.y_data.max()
                label = (f'{column_to_plot} vs {column_against}\n'
                         f'File: {self.file_name}\n'
                         f'Avg: {avg:.2f}, Std Dev: {std_dev:.2f}\n'
                         f'Min: {min_val:.2f}, Max: {max_val:.2f}')
                self.line, = self.ax.plot(self.x_data, self.y_data, label=label)

        plt.xlabel('Against Columns')
        plt.ylabel('Plot Columns')
        plt.legend()
        self.fig.canvas.mpl_connect('button_release_event', self.update_stats)
        plt.show()

    def update_stats(self, event):
        if event.inaxes != self.ax:
            return
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        mask = (self.x_data >= xlim[0]) & (self.x_data <= xlim[1]) & (self.y_data >= ylim[0]) & (self.y_data <= ylim[1])
        y_data_zoomed = self.y_data[mask]

        if len(y_data_zoomed) == 0:
            return

        avg = y_data_zoomed.mean()
        std_dev = y_data_zoomed.std()
        min_val = y_data_zoomed.min()
        max_val = y_data_zoomed.max()

        self.line.set_label((f'{self.line.get_label().split("\n")[0]}\n'
                             f'File: {self.file_name}\n'
                             f'Avg: {avg:.2f}, Std Dev: {std_dev:.2f}\n'
                             f'Min: {min_val:.2f}, Max: {max_val:.2f}'))
        self.ax.legend()
        self.fig.canvas.draw_idle()

app = QApplication(sys.argv)
window = DataPlotter()
window.show()
sys.exit(app.exec_())
