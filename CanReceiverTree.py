# Auteur: Étienne Bellerive-Blais
# Date de création: 2023-06-11
# Nom du fichier: CanReceiverTree.py
# Description:
#


import CAN_BUS_RECEIVER
import threading
from CAN_BUS_RECEIVER import voltages
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QIcon

from playsound import playsound
from pygame import mixer


class Ui_Form(object):

    def update_voltages(self):
        bold_font = QFont()
        bold_font.setBold(True)
        red_font = QColor(255, 0, 0)
        black_font = QColor(0, 0, 0)
        for i, item in enumerate(self.tension_items):
            bms_index = i // 24  # Integer division to get the index of the BMS
            cell_index = i % 24  # Modulo operation to get the index of the cell within the BMS
            voltage = CAN_BUS_RECEIVER.voltages[bms_index][cell_index]
            item.setText(1, f"{voltage}")  # Set the voltage in the second column
            item.setFont(1, bold_font)  # Make the voltage bold
            item.setText(2, "mV")  # Set the unit in the third column
            if 3000 >= voltage or voltage >= 4150:
                item.setForeground(1, red_font)
                item.parent().setForeground(0, red_font)
                item.parent().parent().setForeground(0, red_font)
                mixer.init()
                mixer.music.load(r'siren.mp3')

                mixer.music.play()

            ##if 3000 >= voltage or voltage >= 4150 and voltage != 0:


            else:
                item.setForeground(1, black_font)
                item.parent().setForeground(0, black_font)

    def setupUi(self, Form):

        Form.setWindowIcon(QIcon('iconMoto.png'))
        Form.setWindowTitle("Lecteur CAN-BUS -- EMUS")

        Form.setObjectName("Form")
        Form.resize(863, 733)
        self.TableauPrincipal = QtWidgets.QTreeWidget(parent=Form)
        self.TableauPrincipal.setGeometry(QtCore.QRect(0, 20, 861, 691))
        self.TableauPrincipal.setObjectName("TableauPrincipal")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.TableauPrincipal.headerItem().setFont(0, font)
        self.TableauPrincipal.setHeaderLabels(["Batteries", "Valeur", "Unité"])
        self.TableauPrincipal.setColumnWidth(0, 150)
        # Number of batteries, tensions, temperatures
        nb_batteries = 6
        nb_tensions = 24
        nb_temperatures = 8

        self.tension_items = []  # This will hold QTreeWidgetItem references




        for b in range(nb_batteries):


            batterie = QtWidgets.QTreeWidgetItem(self.TableauPrincipal)
            batterie.setText(0, f"Batterie {b + 1}")

            tensions = QtWidgets.QTreeWidgetItem(batterie)
            tensions.setText(0, "Tensions")
            for t in range(nb_tensions):
                tension = QtWidgets.QTreeWidgetItem(tensions)
                tension.setText(0, f"V{t + 1}")
                self.tension_items.append(tension)




            temperatures = QtWidgets.QTreeWidgetItem(batterie)
            temperatures.setText(0, "Températures")
            for t in range(nb_temperatures):
                temperature = QtWidgets.QTreeWidgetItem(temperatures)
                temperature.setText(0, f"Temp{t + 1}")

        # self.retranslateUi(Form)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_voltages)
        self.timer.start(1000)  # Update every second
        QtCore.QMetaObject.connectSlotsByName(Form)


    # Rest of the code


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('iconMoto.png'))
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)

    Form.show()

    thread = threading.Thread(target=CAN_BUS_RECEIVER.InitierCAN)
    thread.start()

    sys.exit(app.exec())


