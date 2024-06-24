# data-plotter

This Python project is a comprehensive data visualization tool built with Python, leveraging PyQt5 for the graphical user interface and Matplotlib for data plotting. The application is designed to manage, aggregate, and visualize data from various sources, offering graphical representations of the data.

### Key Features

- **Multi-Format Support**: The program can open any file format as long as it is readable text and column-wise data.
- **Dynamic Plotting**: Utilizes Matplotlib to create dynamic, interactive plots with statistical annotations.
- **Customizable Axes**: Allows users to select any column for the X and Y axes for simultaneous plotting.
- **Statistics Display**: Provides basic statistical information (average, standard deviation, minimum, and maximum values) for the plotted data.
- **Export Options**: Supports exporting plots as images or PDFs.

### Usage

This tool is highly useful for data analysts, engineers, and researchers who need to visualize and analyze data efficiently. By providing graphical visualizations and statistical summaries, the application helps in identifying trends, outliers, and areas for further investigation in various data sets.

### Python Branch and Complexity

- **Python Branch**: This project utilizes several advanced Python libraries, including PyQt5 for GUI development, Pandas for data manipulation, and Matplotlib for plotting. These libraries indicate a high-level proficiency in Python, especially in data analysis and visualization domains.
- **Complexity**: The project involves GUI design, data processing, and dynamic plotting. The code demonstrates good practices in object-oriented programming and modular design.

### Code Structure

- **Main Interface**: The main GUI is structured using PyQt5 to manage user interactions and plotting functionalities.
- **Data Handling**: Data is read from various file formats, cleaned, and processed using Pandas.
- **Plotting**: Matplotlib is used extensively for creating interactive plots with statistical annotations.

### Future Enhancements

- **Real-Time Data Integration**: Incorporate real-time data fetching and updating mechanisms.
- **Enhanced Customization**: Allow users to further customize plots and export options through the GUI.
- **Additional Data Sources**: Extend support for other data formats and sources, such as databases or APIs.

This repository is a valuable resource for professionals who need powerful tools for data-driven decision-making and analytical insights.

## Screenshots

### Main Window
![grafik](https://github.com/PrGermux/data-plotter/assets/11144116/48876795-f4b6-48b9-a87c-17c21dacfc4b)


### Plot Example
![grafik](https://github.com/PrGermux/data-plotter/assets/11144116/7c62bff2-5087-4338-b9e2-91ee54c1c9c2)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/data-plotter.git
   cd data-plotter
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

**WARNING**: This program works only with specific data files. The user must adjust the selections for the X and Y axes based on the structure of the input file.

Run the main application:

```sh
python main.py
```

## Freezing

To create an executable using PyInstaller, run the following command:

```sh
pyinstaller --onefile --windowed --icon=icon.png --add-data "icon.png;." --name "Data Plotter" main.py
```

## Dependencies

- Python 3.x
- PyQt5
- Pandas
- Matplotlib

## License

This project is licensed under the MIT License.
