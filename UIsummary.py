import sys, os, ping, time, signal
from PyQt4 import QtCore, QtGui, uic

# load the UI
form_class = uic.loadUiType("UIsummary.ui")[0]

host = "www.google.com.sg"
class UISummaryWindowClass(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		# setup stylesheet
		f = open('darkorange.stylesheet', 'r')
		self.styleData = f.read()
		f.close()

		# initialise actual GUI
		self.setupUi(self)
		self.setStyleSheet(self.styleData)

		# initialise menubar actions
		self.closeAction.setShortcut('Ctrl+Q')
		self.closeAction.setStatusTip('Close application')
		self.closeAction.triggered.connect(QtGui.qApp.quit)

		# initialise statuses
		self.connectionStatus.setText("Initialising...")
		self.pingStatus.setText("Initialising...")

		self.connectionStatusButton.setStyleSheet("background-color: red")
		self.allNodesOnlineStatusButton.setStyleSheet("background-color: red")

		# initialise table widget
		self.orderTableWidget.setColumnCount(5)
		self.orderTableWidget.setRowCount(20)
		self.orderTableWidget.setHorizontalHeaderLabels(['Table', 'Item(s)', 'Qty', 'Amount($)', 'Remarks'])

		self.connect(ping_thread, ping_thread.signal, self.updateUI)

	def updateUI(self, value):
		if value == "nan":
			self.connectionStatus.setText("Disconnected")
			self.pingStatus.setText("Disconnected")
			self.connectionStatusButton.setStyleSheet("background-color: red")
		else:
			self.connectionStatus.setText("Connected to Network")
			self.pingStatus.setText("Ping Time: " + str(value) + " ms")
			self.connectionStatusButton.setStyleSheet("background-color: green")

class PingThread(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self, parent=app)
		self.signal = QtCore.SIGNAL("ping_signal")

	def run(self):
		while True:
			pingval = ping.ping(host)
			self.emit(self.signal, str(round(float(pingval['avgping']), 2)))
			time.sleep(1)

def exit():
	sys.exit(0)

def signal_handler(signal, frame):
	sys.exit(0)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	app = QtGui.QApplication(sys.argv)
	app.setStyle(QtGui.QStyleFactory.create("macintosh"))

	ping_thread = PingThread()

	UIsummary = UISummaryWindowClass(None)

	UIsummary.show()
	ping_thread.start()
	sys.exit(app.exec_())