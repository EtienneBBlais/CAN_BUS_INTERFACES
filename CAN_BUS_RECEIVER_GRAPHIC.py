# Auteur: Étienne Bellerive-Blais
# Date de création: 2023-06-11
# Nom du fichier: CAN_BUS_RECEIVER_GRAPHIC.py
# Description:
#

from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import can

bms_id = [
    list(range(0x400, 0x40F)),
    list(range(0x410, 0x41F)),
    list(range(0x420, 0x42F)),
    list(range(0x430, 0x43F)),
    list(range(0x440, 0x44F)),
    list(range(0x450, 0x45F)),
    list(range(0x460, 0x46F))
]

# Cells correspondance
cells = {
    0: list(range(0, 4)),
    1: list(range(4, 8)),
    2: list(range(8, 12)),
    3: list(range(12, 16)),
    4: list(range(16, 20)),
    5: list(range(20, 24))
}

# Cell voltage
voltages = [([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24), ([0] * 24)]


def parse_message(bms, cells_id, data):
    data = list(data)
    voltage = [
        ((data[1] << 8) + data[0]),
        ((data[3] << 8) + data[2]),
        ((data[5] << 8) + data[4]),
        ((data[7] << 8) + data[6])
    ]
    cells_message = cells.get(cells_id)
    j = 0
    for i in cells_message:
        voltages[4][i] = voltage[j]
        j += 1


def receive_message(bus):
    message = bus.recv()  # Blocking receive
    if message is not None:
        bms = (message.arbitration_id & 0x0F0) >> 4
        cells_id = message.arbitration_id & 0x00F
        if (cells_id < 6) and (bms in range(0, 7)):
            parse_message(bms, cells_id, message.data)


class CanReceiver(QtCore.QThread):
    message_received = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        bus = can.interface.Bus(channel='PCAN_USBBUS1', bustype='pcan', bitrate=250000)
        while self._running:
            message = bus.recv()
            if message is not None:
                self.message_received.emit(f"Received message: {message}")


class Ui_MainWindow(object):

    def append_to_text_edit(self, message):
        self.textEdit.append(message)
        scrollbar = self.textEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.textEdit.setObjectName("textEdit")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Create the receiver
        self.can_receiver = CanReceiver()


        # Create the stop button and connect it to the receiver's stop method
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(700, 550, 80, 30))  # adjust the position and size as needed
        self.stopButton.setText("Stop")
        self.stopButton.clicked.connect(self.can_receiver.stop)

        # Setup the rest of the UI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the receiver's message_received signal and start the thread
        self.can_receiver.message_received.connect(self.append_to_text_edit)
        self.can_receiver.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("CAN BUS Interface", "CAN BUS Interface"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "hr { height: 1px; border-width: 0; }\n"
                                         "li.unchecked::marker { content: \"\\2610\"; }\n"
                                         "li.checked::marker { content: \"\\2612\"; }\n"
                                         "</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Entree CAN BUS : </p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
