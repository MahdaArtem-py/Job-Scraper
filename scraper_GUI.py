from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget,
    QTableWidget, QTableWidgetItem, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
import sys
import pandas as pd
import webbrowser
from scraper import JobScraper


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.scraper = JobScraper()
        self.init_GUI()

    def init_GUI(self):
        self.setWindowTitle("Job Scraper")
        self.setGeometry(950, 300, 400, 650)

        layout = QVBoxLayout()

        self.label = QLabel("Press 'Load Categories' to fetch job categories")
        layout.addWidget(self.label)

        self.load_button = QPushButton("Load Categories")
        self.load_button.clicked.connect(self.load_categories)
        layout.addWidget(self.load_button)

        self.category_list = QListWidget()
        layout.addWidget(self.category_list)

        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.setEnabled(False)
        self.scrape_button.clicked.connect(self.start_scraping)
        layout.addWidget(self.scrape_button)

        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.setEnabled(False)
        self.show_data_button.clicked.connect(self.open_filter_window)
        layout.addWidget(self.show_data_button)

        self.setLayout(layout)

    def load_categories(self):
        select, categories = self.scraper.get_categories()
        self.category_list.clear()
        for index, name in categories.items():
            self.category_list.addItem(name)
        self.scrape_button.setEnabled(True)
        self.label.setText("Select a category and press 'Start Scraping'")

    def start_scraping(self):
        """Start scraping based on the selected category."""
        selected_items = self.category_list.selectedItems()
        if selected_items:
            category = selected_items[0].text()
            self.scraper.driver.quit()
            self.scraper = JobScraper()
            self.scraper.chose_category(category)
            self.scraper.run_scraping(category)
            self.label.setText(f"Scraping completed for: {category}")
            self.show_data_button.setEnabled(True)
        else:
            self.label.setText("Please select a category!")

    def open_filter_window(self):
        """Opens a filter selection window before displaying data."""
        self.filter_window = QWidget()
        self.filter_window.setWindowTitle("Select One Filter")
        self.filter_window.setGeometry(150, 150, 400, 250)

        layout = QVBoxLayout()

        self.salary_filter = QRadioButton("Show only jobs with salary")
        self.junior_filter = QRadioButton("Show 'Junior' level jobs")
        self.middle_filter = QRadioButton("Show 'Middle' level jobs")
        self.senior_filter = QRadioButton("Show 'Senior' level jobs")
        self.remote_filter = QRadioButton("Show only remote jobs")

        self.filter_group = QButtonGroup()
        self.filter_group.addButton(self.salary_filter)
        self.filter_group.addButton(self.junior_filter)
        self.filter_group.addButton(self.middle_filter)
        self.filter_group.addButton(self.senior_filter)
        self.filter_group.addButton(self.remote_filter)

        layout.addWidget(self.salary_filter)
        layout.addWidget(self.junior_filter)
        layout.addWidget(self.middle_filter)
        layout.addWidget(self.senior_filter)
        layout.addWidget(self.remote_filter)

        apply_filters_button = QPushButton("Apply Filter & Show Data")
        apply_filters_button.clicked.connect(self.show_scraped_data)

        layout.addWidget(apply_filters_button)
        self.filter_window.setLayout(layout)
        self.filter_window.show()

    def show_scraped_data(self):
        """Opens a new window to display filtered job data
         with clickable links in the 'link' column."""
        try:
            df = pd.read_csv("jobs.csv")
        except FileNotFoundError:
            self.label.setText("No data found. Please scrape first.")
            return

        if self.salary_filter.isChecked():
            df = df[df["salary"].notna()]
        elif self.junior_filter.isChecked():
            df = df[df["position"].str.contains("Junior",
                                                case=False, na=False)]
        elif self.middle_filter.isChecked():
            df = df[df["position"].str.contains("Middle",
                                                case=False, na=False)]
        elif self.senior_filter.isChecked():
            df = df[df["position"].str.contains("Senior",
                                                case=False, na=False)]
        elif self.remote_filter.isChecked():
            df = df[df["city or remote"].str.contains("віддалено",
                                                      case=False, na=False)]

        self.data_window = QWidget()
        self.data_window.setWindowTitle("Filtered Job Data")
        self.data_window.setGeometry(150, 150, 800, 400)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))

                if df.columns[col] == "link":
                    job_link = df.iat[row, col]
                    item.setData(Qt.ItemDataRole.UserRole, job_link)
                    item.setForeground(Qt.GlobalColor.blue)
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    item.setText(f"🔗 {job_link}")

                self.table.setItem(row, col, item)

        # Connect cell click event to open links
        self.table.cellClicked.connect(self.open_link)

        layout.addWidget(self.table)
        self.data_window.setLayout(layout)
        self.data_window.show()
        self.filter_window.close()

    def open_link(self, row, col):
        """Opens the job link when the 'link' column is clicked."""
        item = self.table.item(row, col)
        if item and item.data(Qt.ItemDataRole.UserRole):
            webbrowser.open(item.data(Qt.ItemDataRole.UserRole))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
