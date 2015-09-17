import sys, os, ping, time, signal
from PyQt4 import QtCore, QtGui, uic

# load the UI
form_class = uic.loadUiType("UIsummary.ui")[0]

host = "192.168.1.1"
class UISummaryWindowClass(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.connectionStatus.setText("Initialising...")
		self.pingStatus.setText("Initialising...")

		self.connect(ping_thread, ping_thread.signal, self.updateUI)

	def updateUI(self, value):
		if value == "nan":
			self.connectionStatus.setText("Disconnected")
			self.pingStatus.setText("Disconnected")
		else:
			self.connectionStatus.setText("Connected to Network")
			self.pingStatus.setText("Ping Time: " + str(value) + " ms")

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

	ping_thread = PingThread()

	UIsummary = UISummaryWindowClass(None)

	UIsummary.show()
	ping_thread.start()
	sys.exit(app.exec_())
