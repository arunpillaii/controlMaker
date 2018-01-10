from PySide2 import QtCore,QtWidgets
from controlMaker.src.ui import controlMakerWidget
reload(controlMakerWidget)

import controlMaker.src.manager as _manager
reload(_manager)
 

class ControlMainWindow(QtWidgets.QWidget):
 
	def __init__(self, parent=None):
 
		super(ControlMainWindow, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Tool)
		self.ui =  controlMakerWidget.Ui_ControlMakerWin()
		self.ui.setupUi(self)

		self.manager = _manager.ControlMaker()
		self._controlType = "2D"
		self._createGroup = True
		self.loadControlType()
		self._connectSignals()
	
	def _connectSignals(self):
		self.ui.type3D_RB.toggled.connect(self.loadType)
		self.ui.nameGroup_CB.toggled.connect(self.createGroup)
		self.ui.createControl_BN.clicked.connect(self.createControl)
		self.ui.translate_BN.clicked.connect(self.translate)
		self.ui.rotation_BN.clicked.connect(self.rotate)
		self.ui.scale_BN.clicked.connect(self.scale)
		self.ui.mirror_BN.clicked.connect(self.mirror)

	def loadControlType(self):
		self.manager.controlType = self._controlType
		subTypes = self.manager.getControls()
		self.ui.controlType_CB.clear()
		self.ui.controlType_CB.addItems(subTypes)

	def loadType(self, state):
		typeMap = {0: "2D",1: "3D"}
		self._controlType = typeMap.get(state)
		self.loadControlType()

	def createGroup(self, state):
		self._createGroup = state

	def createControl(self):
		name = str(self.ui.name_LE.text())
		self.manager.createGroup(self._createGroup)
		self.manager.setSubType(str(self.ui.controlType_CB.currentText()))
		self.manager.makeControl(name)

	def translate(self):
		self.manager.translateControl(
			str(self.ui.transAxis_CB.currentText()),
			str(self.ui.transOrientation_CB.currentText()),
			self.ui.transValue_DS.value(),
			self.ui.transReverse_CB.checkState()
		)

	def rotate(self):
		self.manager.rotateControl(
			str(self.ui.rotationAxis_CB.currentText()),
			str(self.ui.orientation_CB.currentText()),
			self.ui.rotationValue_DS.value(),
			str(self.ui.rotationPivot_CB.currentText()),
			self.ui.rotationReverse_CB.checkState()
		)

	def scale(self):
		axis = [
			int(self.ui.scaleX_CB.checkState()),
			int(self.ui.scaleY_CB.checkState()),
			int(self.ui.scaleZ_CB.checkState())
		]
		self.manager.scaleControl(
			axis,
			self.ui.scaleValue_DS.value(),
			str(self.ui.scalePivot_CB.currentText()),
			self.ui.scaleReverse_CB.checkState()
		)

	def mirror(self):
		self.manager.mirrorControl(
			str(self.ui.search_LE.text()),
			str(self.ui.replace_LE.text())
		)





