""" Manager to create/edit controls
"""

import json as _json
import os as _os
import logging as _logging

import maya.cmds as _cmds
import maya.mel as _mel

from controlMaker import config as _config

_log = _logging.getLogger()


class ControlMaker(object):
	"""
	"""
	def __init__(self):
		""" create/edit/mirror controls
		"""
		super(ControlMaker, self).__init__()
		self._config = self._getConfig()
		self._controlType = None
		self._controlSubType = None
		self._createGroup = True

	def _getConfig(self):
		""" get control config
		"""
		configPath = "%s/controls.json" % _os.path.dirname(_config.__file__)
		with open(configPath) as data_file:    
			data = _json.load(data_file)
		return data

	def getControlTypes(self):
		""" get control types from config
		"""
		return self._config.keys()


	def getControls(self):
		""" get control names from config
		"""
		return self._config.get(self._controlType, {}).keys()

	@property
	def controlType(self):
		""" getter for the control type
		"""
		return self._controlType

	@controlType.setter
	def controlType(self, controlType):
		""" setter for the control type
		"""
		self._controlType = controlType

	def setSubType(self, subType):
		""" set sub type control
		"""
		self._controlSubType = subType

	def createGroup(self, group):
		""" set the create group value
		"""
		self._createGroup = group

	@property
	def getControlData(self):
		""" get control data from config
		"""
		return self._config.get(self._controlType).get(self._controlSubType)


	def makeControl(self, name):
		""" create controls
		"""

		if not name:
			_log.error("Please enter a name to create the controls")
			return

		splitName=name.split('_')
		groupName='Grp_%s' % splitName[-1]

		if _cmds.objExists(name) or _cmds.objExists(groupName):
			_log.error("A control(%s) already exists with this name!!" % name)
			return
		
		transform=_cmds.group(n=name,em=1)
		curve=_cmds.createNode('nurbsCurve',n="%sShape" % name,p=transform)
		setCurve = "_cmds.setAttr('%s.cc',%s,type='nurbsCurve')" % (transform, self.getControlData)
		eval(setCurve)
		logMessage = "New control created as %s" % name
		_cmds.select(transform)

		if self._createGroup:
			splitName=name.split('_')
			groupName='Grp_%s' % splitName[-1]
			if not _cmds.objExists(groupName):
				_cmds.select(
					_cmds.group(transform,n=groupName)
				)
				logMessage = "New control %s is created under the %s" % (name, groupName)
		
		_log.info(logMessage)

	def getSelected(self):
		""" Return the murbscurve from selection
		"""
		selected = _cmds.ls(sl=1,dag=1,type="nurbsCurve")
		return selected

	def getCV(self, shape):
		""" Retrun the cv from shape node
		"""
 			spans=_cmds.getAttr('%s.spans' % shape)
 			degree=_cmds.getAttr('%s.degree'  % shape)
 			form=_cmds.getAttr('%s.form'  % shape)
 			CVs=spans+degree
 			if form:
 				CVs=spans
			
			return ["%s.cv[%d]" % (shape, cv) for cv in range(CVs)] 			

	def translateControl(self, axis, space, value, reverse):
		""" translate the controls
		"""
		axisDict = dict(zip(["X","Y","Z"],[0,0,0]))
		if reverse:
			value = value * -1
		axisDict[axis] = value
		spaceDict = dict(zip(["World","Object","Local"],[0,0,0]))
		spaceDict[space] = 1
		
		for selection in self.getSelected():
			_cmds.move(
				axisDict.get("X"),
				axisDict.get("Y") ,
				axisDict.get("Z") ,
				self.getCV(selection),
				r=True,
				ws=spaceDict.get("World"),
				os=spaceDict.get("Object"),
				ls=spaceDict.get("Local")
			)

	def rotateControl(self, axis, space, value, pivot, reverse):
		""" rotate the controls
		"""
		axisDict = dict(zip(["X","Y","Z"],[0,0,0]))
		if reverse:
			value = value * -1
		axisDict[axis] = value
		spaceDict = dict(zip(["World","Object"],[0,0]))
		spaceDict[space] = 1
		pivotDict = dict(zip(["Transform","Object"],[0,1]))
		
		for selection in self.getSelected():
			_cmds.rotate(
				axisDict.get("X"),
				axisDict.get("Y") ,
				axisDict.get("Z") ,
				self.getCV(selection),
				r=True,
				ws=spaceDict.get("World"),
				os=spaceDict.get("Object"),
				ocp=pivotDict[pivot]
			)

	def scaleControl(self, axis, value, pivot, reverse):
		""" scale the controls
		"""
		if reverse:
			value = value * -1
		axisValue = [1+value*ax for ax in axis]

		axisDict = dict(zip(["X","Y","Z"],axisValue))
		pivotDict = dict(zip(["Transform","Object"],[0,1]))
		for selection in self.getSelected():
			_cmds.scale(
				axisDict.get("X"),
				axisDict.get("Y"),
				axisDict.get("Z"),
				self.getCV(selection),
				r=True,
				ocp=pivotDict[pivot]
			)

	def mirrorControl(self, search, replace):
		""" function to mirror the nurbscurve
		"""
		if search and replace:
			for select in self.getSelected():
				if search in select:
					swapSide = select.replace(search, replace)
					if _cmds.objExists(swapSide):
						selectCV = self.getCV(select)
						swapCV = self.getCV(swapSide)
						_cmds.undoInfo(ock=True)
						for index in range(len(selectCV)):
							getPos = _cmds.xform(selectCV[index], t=True, q=1, ws=True)
							_cmds.xform(swapCV[index], ws=True, t=[getPos[0]*-1,getPos[1],getPos[2]])
						_cmds.undoInfo(cck=True)


