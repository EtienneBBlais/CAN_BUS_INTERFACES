from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QSpinBox, QLabel, \
    QTreeWidget, QTreeWidgetItem, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import sys


class SliderWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('EMUS -- CAN-BUS Generator')
        self.resize(1000, 800)  # Make the app bigger at launch

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabel('Categories')

        # Define categories
        categories = ['ECU', 'Batteries', 'Drive']
        for category in categories:
            category_item = QTreeWidgetItem(self.tree)
            category_item.setText(0, category)

            if category == 'Batteries':
                # Create the master tension
                master_tension_item = QTreeWidgetItem(self.tree)
                master_tension_widget = QWidget(self)
                master_tension = QSlider(Qt.Orientation.Horizontal, self)
                master_tension.setRange(0, 5000)  # range from 0 to 5000 for Tensions
                master_tension.setValue(2000)  # default value is set to 2000 for Tensions
                master_tension.setMaximumWidth(200)  # Set maximum width
                master_tension.last_value = 2000  # Initialize the last_value attribute
                master_tension_label = QLabel("Master Tensions", self)
                h_layout = QHBoxLayout()
                h_layout.addWidget(master_tension)
                h_layout.addWidget(master_tension_label)
                master_tension_widget.setLayout(h_layout)
                self.tree.setItemWidget(master_tension_item, 0, master_tension_widget)

                # Create the master temperature
                master_temperature_item = QTreeWidgetItem(self.tree)
                master_temperature_widget = QWidget(self)
                master_temperature = QSlider(Qt.Orientation.Horizontal, self)
                master_temperature.setRange(0, 100)  # range from 0 to 100 for Temperatures
                master_temperature.setValue(50)  # default value is set to 50 for Temperatures
                master_temperature.setMaximumWidth(200)  # Set maximum width
                master_temperature.last_value = 50  # Initialize the last_value attribute
                master_temperature_label = QLabel("Master Temperatures", self)
                h_layout = QHBoxLayout()
                h_layout.addWidget(master_temperature)
                h_layout.addWidget(master_temperature_label)
                master_temperature_widget.setLayout(h_layout)
                self.tree.setItemWidget(master_temperature_item, 0, master_temperature_widget)

                # Create a list to store all master tension and temperature sliders
                master_tension_sliders = []
                master_temperature_sliders = []

                for i in range(6):
                    battery_item = QTreeWidgetItem(category_item)
                    battery_item.setText(0, f"Batterie {i}")

                    subcategories = ['Tensions', 'Températures']
                    for subcategory in subcategories:
                        subcategory_item = QTreeWidgetItem(battery_item)
                        subcategory_item.setText(0, subcategory)

                        # Master slider
                        master_slider_item = QTreeWidgetItem(subcategory_item)
                        master_widget = QWidget(self)
                        master_slider = QSlider(Qt.Orientation.Horizontal, self)
                        master_slider.setRange(0, 5000 if subcategory == 'Tensions' else 100)  # range from 0 to 5000 for Tensions and 0 to 100 for Températures
                        master_slider.setValue(2000 if subcategory == 'Tensions' else 50)  # default value is set to 2000 for Tensions and 50 for Températures
                        master_slider.setMaximumWidth(200)  # Set maximum width
                        master_slider.last_value = 2000 if subcategory == 'Tensions' else 50  # Initialize the last_value attribute

                        if subcategory == 'Tensions':
                            master_tension_sliders.append(master_slider)  # Add the slider to the list
                        else:
                            master_temperature_sliders.append(master_slider)  # Add the slider to the list

                        master_spin_box = QSpinBox(self)
                        master_spin_box.setRange(0, 5000 if subcategory == 'Tensions' else 100)  # range from 0 to 5000 for Tensions and 0 to 100 for Températures
                        master_spin_box.setValue(2000 if subcategory == 'Tensions' else 50)  # default value is set to 2000 for Tensions and 50 for Températures
                        master_spin_box.setMaximumWidth(50)  # Set maximum width for numeric values

                        # Connect signals and slots for interactive response
                        master_slider.valueChanged.connect(master_spin_box.setValue)
                        master_spin_box.valueChanged.connect(master_slider.setValue)

                        # Create a horizontal layout for each label, slider and spin box
                        h_layout = QHBoxLayout()
                        label = QLabel("Master", self)
                        spacer = QSpacerItem(80, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                        h_layout.addItem(spacer)
                        h_layout.addWidget(master_slider)
                        h_layout.addWidget(label)
                        h_layout.addWidget(master_spin_box)
                        master_widget.setLayout(h_layout)

                        self.tree.setItemWidget(subcategory_item, 0, master_widget)

                        num_sliders = 24 if subcategory == 'Tensions' else 8
                        sliders = []
                        for j in range(num_sliders):
                            slider_item = QTreeWidgetItem(subcategory_item)

                            # Create a widget that contains a slider, label, and spin box
                            widget = QWidget(self)

                            slider = QSlider(Qt.Orientation.Horizontal, self)
                            slider.setRange(0, 5000 if subcategory == 'Tensions' else 100)  # range from 0 to 5000 for Tensions and 0 to 100 for Températures
                            slider.setValue(2000 if subcategory == 'Tensions' else 50)  # default value is set to 2000 for Tensions and 50 for Températures
                            slider.setMaximumWidth(200)  # Set maximum width
                            sliders.append(slider)

                            spin_box = QSpinBox(self)
                            spin_box.setRange(0, 5000 if subcategory == 'Tensions' else 100)  # range from 0 to 5000 for Tensions and 0 to 100 for Températures
                            spin_box.setValue(2000 if subcategory == 'Tensions' else 50)  # default value is set to 2000 for Tensions and 50 for Températures
                            spin_box.setMaximumWidth(50)  # Set maximum width for numeric values

                            # Connect signals and slots for interactive response
                            slider.valueChanged.connect(spin_box.setValue)
                            spin_box.valueChanged.connect(slider.setValue)

                            # Create a horizontal layout for each slider, label and spin box
                            h_layout = QHBoxLayout()
                            label_text = f"V{j + 1}" if subcategory == 'Tensions' else f"Temp{j + 1}"
                            label = QLabel(label_text, self)
                            h_layout.addWidget(slider)
                            h_layout.addWidget(label)
                            h_layout.addWidget(spin_box)
                            widget.setLayout(h_layout)

                            self.tree.setItemWidget(slider_item, 0, widget)

                        # Connect the master slider to a lambda function that updates the child sliders
                        master_slider.valueChanged.connect(
                            lambda value, sliders=sliders, master=master_slider: self.change_sliders(value, sliders,
                                                                                                     master))

            else:
                for i in range(5):
                    slider_item = QTreeWidgetItem(category_item)

                    # Rest of your code...

        # Connect the master tension to a lambda function that updates all master tension sliders
        master_tension.valueChanged.connect(
            lambda value, sliders=master_tension_sliders, master=master_tension: self.change_sliders(value, sliders, master))

        # Connect the master temperature to a lambda function that updates all master temperature sliders
        master_temperature.valueChanged.connect(
            lambda value, sliders=master_temperature_sliders, master=master_temperature: self.change_sliders(value, sliders, master))

        self.layout.addWidget(self.tree)

    def change_sliders(self, value, sliders, master):
        # Calculate the difference between the new and the old value
        diff = value - master.last_value
        # Apply the difference to all child sliders
        for slider in sliders:
            new_value = slider.value() + diff
            new_value = max(0, min(slider.maximum(), new_value))  # Make sure the new value is within the range
            slider.setValue(new_value)
        # Remember the new value of the master slider
        master.last_value = value


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SliderWindow()
    window.show()

    sys.exit(app.exec())


